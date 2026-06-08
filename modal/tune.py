from __future__ import annotations

import os
from typing import Any

import modal

modal_any: Any = modal

# Modal app groups the remote fine-tuning job.
app = modal_any.App("pocket-tutor-tuner")

# Custom container image with the training stack and local dataset code.
image = (
    modal_any.Image.debian_slim()
    .pip_install(
        "torch",
        "transformers>=4.45.0",
        "peft",
        "trl",
        "accelerate",
        "bitsandbytes",
        "datasets",
        "huggingface_hub",
        "pillow",
    )
    .add_local_file(
        os.path.join(os.path.dirname(__file__), "dataset.py"),
        "/root/dataset.py",
    )
)

# Volume keeps checkpoints available across Modal runs.
volume = modal_any.Volume.from_name("pocket-tutor-checkpoints", create_if_missing=True)

# Base model remains under the hackathon parameter limit.
MODEL_ID = "openbmb/MiniCPM3-4B"
ADAPTER_REPO_ID = "build-small-hackathon/pocket-tutor-minicpmv-socratic"


@app.function(
    image=image,
    gpu="A10G",
    timeout=7200,
    volumes={"/checkpoints": volume},
    secrets=[modal_any.Secret.from_name("huggingface-secret")],
)
def train_lora(
    model_card_content: str,
    hf_token: str | None = None,
    repo_id: str | None = None,
):
    """Fine-tunes a compact MiniCPM tutor adapter on app-format Socratic examples."""
    # Remote-only imports are installed inside the Modal container.
    import io
    import os as remote_os

    import torch
    from datasets import Dataset
    from huggingface_hub import login, upload_file
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from trl import SFTConfig, SFTTrainer

    from dataset import (
        build_training_prompt,
        get_chat_training_examples,
        get_training_examples,
    )

    # Load tokenizer and prepare app-format conversations.
    print(f"Loading tokenizer for {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    formatted_dataset = []
    for item in get_training_examples():
        messages = [
            {
                "role": "user",
                "content": build_training_prompt(
                    str(item["question"]),
                    str(item["grade"]),
                    str(item["mode"]),
                ),
            },
            {"role": "assistant", "content": str(item["response"])},
        ]
        formatted_dataset.append(
            {"text": tokenizer.apply_chat_template(messages, tokenize=False)}
        )
    for messages in get_chat_training_examples():
        formatted_dataset.append(
            {"text": tokenizer.apply_chat_template(messages, tokenize=False)}
        )
    dataset = Dataset.from_list(formatted_dataset)
    print(f"Prepared {len(dataset)} tutoring conversations.")

    # QLoRA keeps adapter training feasible on a single A10G.
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.pad_token_id = tokenizer.eos_token_id
    model = prepare_model_for_kbit_training(model)

    # Target common attention projections for structured tutoring behavior.
    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

    # Train on the current production section format, not an earlier seed format.
    training_args = SFTConfig(
        output_dir="/checkpoints/pocket-tutor-lora",
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=8,
        max_steps=180,
        learning_rate=2e-4,
        bf16=True,
        logging_steps=5,
        save_strategy="steps",
        save_steps=45,
        save_total_limit=2,
        report_to="none",
        dataset_text_field="text",
        max_length=1536,
    )
    trainer = SFTTrainer(model=model, train_dataset=dataset, args=training_args)
    trainer.train()

    # Save the final adapter into the persistent Modal volume.
    model.save_pretrained("/checkpoints/pocket-tutor-final")
    tokenizer.save_pretrained("/checkpoints/pocket-tutor-final")
    volume.commit()

    # Publish the adapter and model card when credentials are available.
    hf_token = hf_token or remote_os.environ.get("HF_TOKEN")
    repo_id = repo_id or ADAPTER_REPO_ID
    if hf_token:
        login(token=hf_token)
        model.push_to_hub(repo_id)
        tokenizer.push_to_hub(repo_id)
        upload_file(
            path_or_fileobj=io.BytesIO(model_card_content.encode("utf-8")),
            path_in_repo="README.md",
            repo_id=repo_id,
            repo_type="model",
            commit_message="Update Pocket Tutor adapter model card",
        )
    else:
        print("HF_TOKEN not set. Skipping Hub publish.")


@app.local_entrypoint()
def main():
    # Read the model card at launch so edits are included in the run.
    meta_path = os.path.join(os.path.dirname(__file__), "CARD.md")
    with open(meta_path, encoding="utf-8") as f:
        model_card = f.read()
    train_lora.remote(model_card_content=model_card)
