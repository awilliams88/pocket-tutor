from __future__ import annotations

import os
from env.runtime import patch_asyncio_cleanup_warning
from ui.layout import create_app, get_theme
from ui.styles import CUSTOM_CSS

# Keep Spaces startup predictable for this custom Gradio layout.
os.environ.setdefault("GRADIO_SSR_MODE", "false")

# Hide a harmless local Gradio teardown warning.
patch_asyncio_cleanup_warning()

# Build the app once for Hugging Face Spaces discovery.
demo = create_app()

if __name__ == "__main__":
    # Direct Python launch is used by run.sh and Spaces.
    demo.launch(theme=get_theme(), css=CUSTOM_CSS)
