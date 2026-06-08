from __future__ import annotations

# App copy shown in the Gradio header.
APP_TITLE = "Pocket Tutor"
APP_DESCRIPTION = "Photo-first homework coaching for students and parents."

# Input limits keep local prompts compact and predictable.
QUESTION_LIMIT = 3000
TRANSCRIPT_LIMIT = 1200
SUPPORTED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}

# Public links shown in the Space footer.
GITHUB_URL = "https://github.com/awilliams88/pocket-tutor"
SPACE_URL = "https://huggingface.co/spaces/build-small-hackathon/pocket-tutor"

# Model metadata keeps docs, logs, and UI aligned.
MODEL_ID = "openbmb/MiniCPM-V-4.6"
FALLBACK_MODEL_ID = "openbmb/MiniCPM3-4B"
SPEECH_MODEL_ID = "openai/whisper-small"
ADAPTER_REPO_ID = "build-small-hackathon/pocket-tutor-minicpmv-socratic"
SPONSOR_NAME = "OpenBMB"
PARAMETER_COUNT = "~1B vision-language"
