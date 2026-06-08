from __future__ import annotations

import os
import re
from typing import Any

from env.config import ADAPTER_REPO_ID, MODEL_ID, SPEECH_MODEL_ID

# Keep model instances warm after first use.
_vl_model: Any = None
_vl_processor: Any = None
_speech_pipeline: Any = None

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
                generate_kwargs={
                    "task": "transcribe",
                    "language": "en",
                },
                clean_up_tokenization_spaces=False,
            )
        result = _speech_pipeline(str(audio_path))
        transcript = str(result.get("text", "")).strip()
        return transcript, f"Transcribed microphone input with {SPEECH_MODEL_ID}."
    except Exception as exc:
        return "", f"Speech transcription unavailable: {exc}"


def _load_multimodal_model(log_lines: list[str]) -> tuple[Any, Any]:
    """Loads the multimodal Pocket Tutor model and optional adapter."""
    global _vl_model, _vl_processor
    if _vl_model is None:
        import torch
        from peft import PeftModel
        from transformers import AutoModelForImageTextToText, AutoProcessor

        # Load the shared multimodal processor and model once.
        log_lines.append(f"Loading processor: {MODEL_ID}")
        _vl_processor = AutoProcessor.from_pretrained(
            MODEL_ID,
            trust_remote_code=True,
            token=os.environ.get("HF_TOKEN"),
        )
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        log_lines.append(f"Loading model: {MODEL_ID}")
        _vl_model = AutoModelForImageTextToText.from_pretrained(
            MODEL_ID,
            dtype=dtype,
            low_cpu_mem_usage=True,
            trust_remote_code=True,
            token=os.environ.get("HF_TOKEN"),
        )
        _vl_model.eval()
        try:
            log_lines.append(f"Loading LoRA adapter: {ADAPTER_REPO_ID}")
            _vl_model = PeftModel.from_pretrained(
                _vl_model,
                ADAPTER_REPO_ID,
                token=os.environ.get("HF_TOKEN"),
            )
            log_lines.append("LoRA adapter applied to multimodal model.")
        except Exception as exc:
            log_lines.append(f"Adapter unavailable for multimodal model: {exc}")
        if torch.cuda.is_available():
            _vl_model = _vl_model.to("cuda")
    else:
        log_lines.append("Using cached multimodal model.")
    return _vl_model, _vl_processor


def run_tutor_inference(prompt: str, image_path: str | None) -> tuple[str, str]:
    """Executes local tutoring inference with one multimodal model."""
    log_lines: list[str] = []
    try:
        response, logs = _run_model_inference(prompt, image_path)
        log_lines.append(logs)
        return response, "\n".join(log_lines)
    except Exception as exc:
        log_lines.append(f"Local model execution failed: {exc}")
        log_lines.append("Returning a deterministic tutoring scaffold.")
        return _fallback_tutoring_response(prompt), "\n".join(log_lines)


def _run_model_inference(prompt: str, image_path: str | None) -> tuple[str, str]:
    """Runs MiniCPM-V for either text-only or image-grounded tutoring."""
    global _vl_model, _vl_processor
    log_lines: list[str] = []
    try:
        import torch
        from PIL import Image

        model, processor = _load_multimodal_model(log_lines)
        if image_path:
            image = Image.open(image_path).convert("RGB")
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]
        else:
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
            output = model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=False,
                repetition_penalty=1.05,
            )
        response = processor.decode(
            output[0, inputs["input_ids"].shape[1] :],
            skip_special_tokens=True,
        )
        log_lines.append("Multimodal tutoring inference completed.")
        return clean_generated_text(str(response)), "\n".join(log_lines)
    except Exception as exc:
        log_lines.append(f"Model execution failed: {exc}")
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
