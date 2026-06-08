from __future__ import annotations

import os
from env.runtime import patch_asyncio_cleanup_warning
from ui.layout import create_app, get_theme
from ui.styles import CUSTOM_CSS

# Keep Spaces startup predictable for this custom Gradio layout.
os.environ.setdefault("GRADIO_SSR_MODE", "false")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

# Quiet noisy Transformers warnings during normal app use.
try:
    from transformers.utils import logging as hf_logging

    hf_logging.set_verbosity_error()
    if hasattr(hf_logging, "disable_progress_bar"):
        hf_logging.disable_progress_bar()
except Exception:
    pass

# Hide a harmless local Gradio teardown warning.
patch_asyncio_cleanup_warning()

# Build the app once for Hugging Face Spaces discovery.
demo = create_app()

if __name__ == "__main__":
    # Direct Python launch is used by run.sh and Spaces.
    demo.launch(theme=get_theme(), css=CUSTOM_CSS)
