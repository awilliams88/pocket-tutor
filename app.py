from __future__ import annotations

import logging
import os
import warnings
from env.runtime import patch_asyncio_cleanup_warning
from ui.layout import create_app, get_theme
from ui.styles import CUSTOM_CSS

# Keep Spaces startup predictable for this custom Gradio layout.
os.environ.setdefault("GRADIO_SSR_MODE", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

# Quiet noisy Transformers warnings during normal app use.
try:
    from transformers.utils import logging as hf_logging

    hf_logging.set_verbosity_error()
    if hasattr(hf_logging, "disable_progress_bar"):
        hf_logging.disable_progress_bar()
except Exception:
    pass

warnings.filterwarnings("ignore", message=r".*forced_decoder_ids.*")
warnings.filterwarnings("ignore", message=r".*multilingual Whisper.*")
warnings.filterwarnings("ignore", message=r".*SuppressTokensLogitsProcessor.*")
warnings.filterwarnings("ignore", message=r".*SuppressTokensAtBeginLogitsProcessor.*")
warnings.filterwarnings("ignore", message=r".*clean_up_tokenization_spaces.*")
warnings.filterwarnings("ignore", message=r".*pad_token_id to `eos_token_id`.*")


class _SuppressKnownTransformersNoise(logging.Filter):
    """Drops repeated non-actionable transformer startup noise."""

    _blocked_fragments = (
        "`loss` is part of Qwen3_5CausalLMOutputWithPast.__init__'s signature",
        "`logits` is part of Qwen3_5CausalLMOutputWithPast.__init__'s signature",
        "forced_decoder_ids",
        "multilingual Whisper",
        "SuppressTokensLogitsProcessor",
        "SuppressTokensAtBeginLogitsProcessor",
        "clean_up_tokenization_spaces",
        "pad_token_id to `eos_token_id`",
        "The fast path is not available because one of the required library is not installed",
    )

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(fragment in message for fragment in self._blocked_fragments)


_transformers_noise_filter = _SuppressKnownTransformersNoise()
for logger_name in ("", "transformers", "transformers.generation", "transformers.models.whisper", "transformers.models.qwen3_5"):
    logging.getLogger(logger_name).addFilter(_transformers_noise_filter)

for logger_name in (
    "transformers",
    "transformers.generation",
    "transformers.models.whisper",
    "transformers.models.qwen3_5",
):
    logging.getLogger(logger_name).setLevel(logging.CRITICAL)

# Hide a harmless local Gradio teardown warning.
patch_asyncio_cleanup_warning()

# Build the app once for Hugging Face Spaces discovery.
demo = create_app()

if __name__ == "__main__":
    # Direct Python launch is used by run.sh and Spaces.
    demo.launch(theme=get_theme(), css=CUSTOM_CSS)
