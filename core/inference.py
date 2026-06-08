from __future__ import annotations

import os
import re
from typing import Any

from env.config import ADAPTER_REPO_ID, FALLBACK_MODEL_ID, MODEL_ID, SPEECH_MODEL_ID

# Keep model instances warm after first use.
_vl_model: Any = None
_vl_tokenizer: Any = None
_text_model: Any = None
_text_tokenizer: Any = None
_speech_pipeline: Any = None
_adapter_applied = False

_THINK_BLOCK_PATTERN = re.compile(r"<think>.*?</think>", re.IGNORECASE | re.DOTALL)
_THINK_START_PATTERN = re.compile(r"<think>.*", re.IGNORECASE | re.DOTALL)


def clean_generated_text(text: str) -> str:
    """Removes hidden reasoning and chat-template leftovers from model output."""
    # Prefer visible content after a completed thinking block.
    if "</think>" in text.lower():
        text = re.split(r"</think>", text, flags=re.IGNORECASE, maxsplit=1)[-1]
    text = _THINK_BLOCK_PATTERN.sub("", text)
    text = _THINK_START_PATTERN.sub("", text)
    for marker in ("<|im_end|>", "<|im_start|>", "\nUser:", "\nAssistant:"):
        if marker in text:
            text = text.split(marker, 1)[0]
    text = re.sub(r"[ \t]+", " ", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def _format_chat_prompt(tokenizer: Any, messages: list[dict[str, str]]) -> str:
    """Formats chat input while disabling hidden reasoning when supported."""
    try:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )


def transcribe_audio(audio_path: object | None) -> tuple[str, str]:
    """Transcribes optional microphone input using a local speech model when available."""
    global _speech_pipeline
    if not audio_path:
        return "", "No microphone input provided."
    try:
        from transformers import pipeline

        if _speech_pipeline is None:
            _speech_pipeline = pipeline(
                "automatic-speech-recognition",
                model=SPEECH_MODEL_ID,
                token=os.environ.get("HF_TOKEN"),
            )
        result = _speech_pipeline(str(audio_path))
        transcript = str(result.get("text", "")).strip()
        return transcript, f"Transcribed microphone input with {SPEECH_MODEL_ID}."
    except Exception as exc:
        return "", f"Speech transcription unavailable: {exc}"


def _load_text_model(log_lines: list[str]) -> tuple[Any, Any]:
    """Loads the compact fallback tutor model for text-only requests."""
    global _adapter_applied, _text_model, _text_tokenizer
    if _text_model is None:
        import torch
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer

        # Load tokenizer and base text model for local fallback tutoring.
        log_lines.append(f"Loading tokenizer: {FALLBACK_MODEL_ID}")
        _text_tokenizer = AutoTokenizer.from_pretrained(
            FALLBACK_MODEL_ID,
            trust_remote_code=True,
            token=os.environ.get("HF_TOKEN"),
        )
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        log_lines.append(f"Loading model: {FALLBACK_MODEL_ID}")
        _text_model = AutoModelForCausalLM.from_pretrained(
            FALLBACK_MODEL_ID,
            dtype=dtype,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            token=os.environ.get("HF_TOKEN"),
        )
        try:
            log_lines.append(f"Loading LoRA adapter: {ADAPTER_REPO_ID}")
            _text_model = PeftModel.from_pretrained(
                _text_model,
                ADAPTER_REPO_ID,
                token=os.environ.get("HF_TOKEN"),
            )
            _adapter_applied = True
            log_lines.append("LoRA adapter applied to fallback text model.")
        except Exception as exc:
            _adapter_applied = False
            log_lines.append(f"Adapter unavailable for fallback model: {exc}")
        if torch.cuda.is_available():
            _text_model = _text_model.to("cuda")
    else:
        adapter_status = "with LoRA adapter" if _adapter_applied else "without adapter"
        log_lines.append(f"Using cached fallback text model {adapter_status}.")
    return _text_model, _text_tokenizer


def run_tutor_inference(prompt: str, image_path: str | None) -> tuple[str, str]:
    """Executes local tutoring inference, preferring vision-language when an image exists."""
    log_lines: list[str] = []
    if image_path:
        response, logs = _run_vision_inference(prompt, image_path)
        if response:
            return response, logs
        log_lines.append(logs)

    # Text-only fallback keeps typed and transcribed questions usable.
    try:
        log_lines.append("Initializing text tutoring fallback...")
        model, tokenizer = _load_text_model(log_lines)
        device = str(model.device)
        messages = [{"role": "user", "content": prompt}]
        text = _format_chat_prompt(tokenizer, messages)
        model_inputs = tokenizer([text], return_tensors="pt").to(device)
        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=640,
            do_sample=False,
            repetition_penalty=1.08,
        )
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        log_lines.append("Text tutoring fallback completed.")
        return clean_generated_text(response), "\n".join(log_lines)
    except Exception as exc:
        log_lines.append(f"Local model execution failed: {exc}")
        log_lines.append("Returning a deterministic tutoring scaffold.")
        return _fallback_tutoring_response(prompt), "\n".join(log_lines)


def _run_vision_inference(prompt: str, image_path: str) -> tuple[str, str]:
    """Runs MiniCPM-V when the runtime supports its remote-code interface."""
    global _vl_model, _vl_tokenizer
    log_lines: list[str] = []
    try:
        import torch
        from PIL import Image
        from transformers import AutoModel, AutoTokenizer

        if _vl_model is None:
            # MiniCPM-V uses custom modeling code, so trust_remote_code is required.
            log_lines.append(f"Loading tokenizer: {MODEL_ID}")
            _vl_tokenizer = AutoTokenizer.from_pretrained(
                MODEL_ID,
                trust_remote_code=True,
                token=os.environ.get("HF_TOKEN"),
            )
            dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
            log_lines.append(f"Loading vision-language model: {MODEL_ID}")
            _vl_model = AutoModel.from_pretrained(
                MODEL_ID,
                trust_remote_code=True,
                dtype=dtype,
                low_cpu_mem_usage=True,
                token=os.environ.get("HF_TOKEN"),
            )
            if torch.cuda.is_available():
                _vl_model = _vl_model.to("cuda")
            _vl_model.eval()
        else:
            log_lines.append("Using cached vision-language model.")

        # Use the model's chat API when available.
        image = Image.open(image_path).convert("RGB")
        msgs = [{"role": "user", "content": [image, prompt]}]
        response = _vl_model.chat(image=None, msgs=msgs, tokenizer=_vl_tokenizer)
        log_lines.append("Vision tutoring inference completed.")
        return clean_generated_text(str(response)), "\n".join(log_lines)
    except Exception as exc:
        log_lines.append(f"Vision model execution failed: {exc}")
        return "", "\n".join(log_lines)


def _fallback_tutoring_response(prompt: str) -> str:
    """Returns a stable tutor-shaped response when local weights are unavailable."""
    return (
        "=== PROBLEM READ ===\n"
        "I can help, but the local model is still loading or unavailable. I will treat your typed question as the source.\n\n"
        "=== KNOWNS ===\n"
        f"- Student question: {prompt[:240] or 'No question text provided.'}\n\n"
        "=== STRATEGY ===\n"
        "Restate the problem in your own words, identify the given values, then choose the smallest rule or example that applies.\n\n"
        "=== WORKED STEPS ===\n"
        "1. Copy the exact problem statement.\n"
        "2. Underline what is being asked.\n"
        "3. List the givens and the unknown.\n"
        "4. Try one step, then check whether the units or logic still make sense.\n\n"
        "=== CHECK ===\n"
        "The answer should satisfy the original question, use the right units, and not contradict any given information.\n\n"
        "=== NEXT HINT ===\n"
        "Tell me which line confuses you most, and I will give only the next hint.\n\n"
        "=== PARENT NOTE ===\n"
        "Ask the learner to explain their first step out loud before correcting the answer."
    )
