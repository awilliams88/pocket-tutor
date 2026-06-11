from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import modal

modal_any: Any = modal

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

app = modal_any.App("pocket-tutor-smoke")

image = modal_any.Image.debian_slim().pip_install(
    "torch",
    "torchvision",
    "transformers[torch]>=5.7.0",
    "peft",
    "accelerate",
    "huggingface_hub",
    "pillow",
)

MODEL_ID = "openbmb/MiniCPM-V-4.6"
ADAPTER_REPO_ID = "build-small-hackathon/pocket-tutor-minicpmv-socratic"

DEFAULT_QUESTION = "Can you show me how to solve 3(2x - 5) = 21 without jumping straight to the answer?"
DEFAULT_GRADE = "High school"
DEFAULT_MODE = "Step-by-step"
DEFAULT_MAX_NEW_TOKENS = 384


def _build_prompt(question: str, grade_band: str, help_mode: str) -> str:
    """Builds the exact tutoring prompt used by the production Space."""
    from core.analyzer import build_tutor_prompt

    return build_tutor_prompt(
        question=question,
        transcript="",
        grade_band=grade_band,
        help_mode=help_mode,
        image_status="No image uploaded.",
    )


def _validate_sections(sections: tuple[str, str, str, str, str, str, str]) -> list[str]:
    """Returns missing section names when the model output falls back."""
    section_names = (
        "problem",
        "knowns",
        "strategy",
        "steps",
        "check",
        "hint",
        "parent",
    )
    defaults = {
        "problem": "Upload a homework image or type the question to begin.",
        "knowns": "- No givens identified yet.",
        "strategy": "No strategy generated yet.",
        "steps": "No worked steps generated yet.",
        "check": "No answer check generated yet.",
        "hint": "Ask for a hint after the first explanation.",
        "parent": "Parent support note will appear here.",
    }
    return [
        name
        for name, value in zip(section_names, sections, strict=True)
        if name in defaults and str(value).strip() in {"", defaults[name]}
    ]


def _iter_smoke_cases() -> list[dict[str, str]]:
    """Collects the structured training examples and follow-up chat examples."""
    from dataset import get_chat_training_examples, get_training_examples

    cases: list[dict[str, str]] = []
    for item in get_training_examples():
        cases.append(
            {
                "kind": "training",
                "grade": str(item["grade"]),
                "mode": str(item["mode"]),
                "question": str(item["question"]),
            }
        )
    for index, messages in enumerate(get_chat_training_examples(), start=1):
        user_message = next(
            (message for message in messages if message.get("role") == "user"),
            None,
        )
        if not user_message:
            continue
        cases.append(
            {
                "kind": f"chat-{index}",
                "grade": DEFAULT_GRADE,
                "mode": DEFAULT_MODE,
                "question": str(user_message.get("content", "")),
            }
        )
    return cases


@app.function(
    image=image,
    gpu="A10G",
    timeout=3600,
    secrets=[modal_any.Secret.from_name("huggingface-secret")],
)
def generate_response(
    prompt: str, max_new_tokens: int = DEFAULT_MAX_NEW_TOKENS
) -> dict[str, str]:
    """Loads the production model and returns the raw generated response."""
    import torch
    from peft import PeftModel
    from transformers import AutoModelForImageTextToText, AutoProcessor

    log_lines: list[str] = []
    hf_token = os.environ.get("HF_TOKEN")
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

    log_lines.append(f"Loading processor: {MODEL_ID}")
    print(log_lines[-1])
    processor = AutoProcessor.from_pretrained(
        MODEL_ID,
        trust_remote_code=True,
        token=hf_token,
    )
    log_lines.append(f"Loading model: {MODEL_ID}")
    print(log_lines[-1])
    model = AutoModelForImageTextToText.from_pretrained(
        MODEL_ID,
        dtype=dtype,
        low_cpu_mem_usage=True,
        trust_remote_code=True,
        token=hf_token,
    )
    model.eval()
    log_lines.append(f"Loading LoRA adapter: {ADAPTER_REPO_ID}")
    print(log_lines[-1])
    model = PeftModel.from_pretrained(
        model,
        ADAPTER_REPO_ID,
        token=hf_token,
    )
    log_lines.append("LoRA adapter applied to multimodal model.")
    print(log_lines[-1])
    if torch.cuda.is_available():
        model = model.to("cuda")

    messages = [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}],
        }
    ]
    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
        enable_thinking=False,
    ).to(model.device)

    with torch.inference_mode():
        pad_token_id = getattr(processor.tokenizer, "pad_token_id", None)
        eos_token_id = getattr(processor.tokenizer, "eos_token_id", None)
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.05,
            pad_token_id=pad_token_id if pad_token_id is not None else eos_token_id,
            eos_token_id=eos_token_id,
        )

    raw_response = processor.decode(
        output[0, inputs["input_ids"].shape[1] :],
        skip_special_tokens=True,
    )
    log_lines.append("Model generation finished.")
    print(log_lines[-1])
    return {
        "raw_response": str(raw_response),
        "logs": "\n".join(log_lines),
    }


@app.local_entrypoint()
def main() -> None:
    """Runs remote smoke tests across every training example."""
    from core.inference import clean_generated_text
    from core.parser import parse_sections

    question = os.environ.get("SMOKE_QUESTION", DEFAULT_QUESTION).strip()
    grade_band = os.environ.get("SMOKE_GRADE", DEFAULT_GRADE)
    help_mode = os.environ.get("SMOKE_MODE", DEFAULT_MODE)
    max_new_tokens = int(
        os.environ.get("SMOKE_MAX_NEW_TOKENS", str(DEFAULT_MAX_NEW_TOKENS))
    )
    smoke_all = os.environ.get("SMOKE_ALL_EXAMPLES", "1").strip().lower() not in {
        "0",
        "false",
        "no",
    }

    section_names = (
        "problem",
        "knowns",
        "strategy",
        "steps",
        "check",
        "hint",
        "parent",
    )

    cases = (
        _iter_smoke_cases()
        if smoke_all
        else [
            {
                "kind": "single",
                "grade": grade_band,
                "mode": help_mode,
                "question": question,
            }
        ]
    )
    failures: list[str] = []
    for index, case in enumerate(cases, start=1):
        prompt = _build_prompt(
            question=case["question"],
            grade_band=case["grade"],
            help_mode=case["mode"],
        )
        print(f"=== CASE {index}/{len(cases)} :: {case['kind']} ===")
        print(f"Grade: {case['grade']} | Mode: {case['mode']}")
        print(f"Question: {case['question']}")
        result = generate_response.remote(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
        )
        raw_response = str(result["raw_response"])
        cleaned_response = clean_generated_text(raw_response)
        sections = parse_sections(cleaned_response)

        print("=== RAW RESPONSE ===")
        print(raw_response or "[empty]")
        print("=== CLEANED RESPONSE ===")
        print(cleaned_response or "[empty]")
        print("=== PARSED SECTIONS ===")
        for name, value in zip(section_names, sections, strict=True):
            print(f"[{name}]")
            print(value)
            print()
        print("=== LOGS ===")
        print(result["logs"] or "[empty]")

        missing = _validate_sections(sections)
        if missing:
            failure = f"{case['kind']}: missing {', '.join(missing)}"
            failures.append(failure)
            print(f"[smoke] {failure}", file=sys.stderr)

    if failures:
        raise SystemExit(
            "Pocket Tutor Modal smoke failed for examples: " + "; ".join(failures)
        )

    print("Pocket Tutor Modal smoke test passed for all examples.")
