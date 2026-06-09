#!/usr/bin/env bash
# run.sh — local dev utility for Pocket Tutor.
# Usage: ./run.sh [setup|verify|smoke|app]
set -euo pipefail

# Set ROOT_DIR
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Set PYTHON and TARGET
PYTHON=".venv/bin/python"
TARGET="${1:-app}"

# Create the virtual environment and install dependencies.
setup() {
  if [ ! -x "$PYTHON" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
  fi
  echo "Installing dependencies..."
  "$PYTHON" -m pip install --quiet --upgrade pip
  "$PYTHON" -m pip install --quiet -r requirements.txt
  echo "Setup complete."
}

# Abort early if the virtual environment is missing.
ensure_venv() {
  if [ ! -x "$PYTHON" ]; then
    echo "Error: run ./run.sh setup first."
    exit 1
  fi
}

case "$TARGET" in
  setup)
    setup
    ;;

  verify)
    [ ! -x "$PYTHON" ] && setup
    echo "-> format"
    "$PYTHON" -m ruff format app.py env/*.py core/*.py ui/*.py modal/*.py scripts/*.py
    echo "-> lint"
    "$PYTHON" -m ruff check --fix app.py env/*.py core/*.py ui/*.py modal/*.py scripts/*.py
    echo "-> types"
    "$PYTHON" -m pyright app.py env/*.py core/*.py ui/*.py modal/*.py scripts/*.py
    echo "-> compile"
    "$PYTHON" -m compileall -q app.py env/ core/ ui/ modal/ scripts/
    echo "All checks passed."
    ;;

  smoke)
    ensure_venv
    export SMOKE_QUESTION="${SMOKE_QUESTION:-Can you show me how to solve 3(2x - 5) = 21 without jumping straight to the answer?}"
    export SMOKE_GRADE="${SMOKE_GRADE:-High school}"
    export SMOKE_MODE="${SMOKE_MODE:-Step-by-step}"
    export SMOKE_IMAGE="${SMOKE_IMAGE:-}"
    export SMOKE_MAX_NEW_TOKENS="${SMOKE_MAX_NEW_TOKENS:-384}"
    "$PYTHON" - <<'PY'
from core.analyzer import build_tutor_prompt
from core.inference import run_tutor_inference_debug
from core.parser import parse_sections
from env.config import QUESTION_LIMIT
import os

question = os.environ.get("SMOKE_QUESTION", "").strip()[:QUESTION_LIMIT]
grade_band = os.environ.get("SMOKE_GRADE", "High school")
help_mode = os.environ.get("SMOKE_MODE", "Step-by-step")
image_path = os.environ.get("SMOKE_IMAGE") or None
max_new_tokens = int(os.environ.get("SMOKE_MAX_NEW_TOKENS", "32"))

prompt = build_tutor_prompt(
    question=question,
    transcript="",
    grade_band=grade_band,
    help_mode=help_mode,
    image_status="No image uploaded." if not image_path else f"Image path: {image_path}",
)
raw_response, cleaned_response, logs = run_tutor_inference_debug(
    prompt,
    image_path,
    max_new_tokens=max_new_tokens,
)
sections = parse_sections(cleaned_response)

print("=== PROMPT ===")
print(prompt)
print("=== RAW RESPONSE ===")
print(raw_response or "[empty]")
print("=== CLEANED RESPONSE ===")
print(cleaned_response or "[empty]")
print("=== PARSED SECTIONS ===")
for name, value in zip(
    ["problem", "knowns", "strategy", "steps", "check", "hint", "parent"],
    sections,
):
    print(f"[{name}]")
    print(value)
    print()
print("=== LOGS ===")
print(logs or "[empty]")
PY
    ;;

  app | run | *)
    ensure_venv
    "$PYTHON" app.py
    ;;
esac

# Remove Python and linter cache dirs on exit.
cleanup() {
  find "$ROOT_DIR" \
    -not -path "$ROOT_DIR/.git/*" \
    -not -path "$ROOT_DIR/.venv/*" \
    \( -type d -name "__pycache__" -o -type d -name ".ruff_cache" \) \
    -exec rm -rf {} + 2>/dev/null || true
}
trap cleanup EXIT
