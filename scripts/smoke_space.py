from __future__ import annotations
# ruff: noqa: E402

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.analyzer import build_tutor_prompt
from env.config import QUESTION_LIMIT, SPACE_URL

DEFAULT_QUESTION = "Can you show me how to solve 3(2x - 5) = 21 without jumping straight to the answer?"
DEFAULT_GRADE = "High school"
DEFAULT_MODE = "Step-by-step"
DEFAULT_PROBLEM = "Upload a homework image or type the question to begin."
DEFAULT_KNOWNS = "- No givens identified yet."
DEFAULT_STRATEGY = "No strategy generated yet."
DEFAULT_STEPS = "No worked steps generated yet."
DEFAULT_CHECK = "No answer check generated yet."
DEFAULT_HINT = "Ask for a hint after the first explanation."
DEFAULT_PARENT = "Parent support note will appear here."


def _derive_space_base_url(space_url: str) -> str:
    """Converts the human Space URL into the hf.space API host."""
    parts = [part for part in space_url.rstrip("/").split("/") if part]
    if len(parts) < 2:
        raise ValueError(f"Could not derive a Space host from {space_url!r}.")
    namespace, repo_name = parts[-2], parts[-1]
    return f"https://{namespace}-{repo_name}.hf.space"


def _request_json(
    url: str,
    payload: dict[str, Any] | None = None,
    token: str | None = None,
) -> Any:
    """Sends a JSON request and returns the decoded payload."""
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.loads(response.read().decode("utf-8"))


def _stream_completion(url: str, token: str | None = None) -> list[Any]:
    """Reads the final SSE completion event from a Gradio queue stream."""
    headers = {"Accept": "text/event-stream"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers, method="GET")
    event_name = ""
    pending_data: list[str] = []
    with urllib.request.urlopen(request, timeout=600) as response:
        for raw_line in response:
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            if line.startswith("event:"):
                event_name = line.split(":", 1)[1].strip()
                pending_data = []
                continue
            if line.startswith("data:"):
                pending_data.append(line.split(":", 1)[1].lstrip())
                if event_name == "complete":
                    return json.loads("\n".join(pending_data))
    raise RuntimeError("Space stream ended before a completion event was received.")


def _run_space_smoke(
    space_base_url: str,
    question: str,
    grade_band: str,
    help_mode: str,
    token: str | None,
) -> list[Any]:
    """Submits a text-only tutoring request to the live Space."""
    submit_url = f"{space_base_url}/gradio_api/call/v2/analyze_homework_ui"
    result_url = f"{space_base_url}/gradio_api/call/analyze_homework_ui"
    payload = {
        "image_file": None,
        "question": question,
        "audio_path": None,
        "grade_band": grade_band,
        "help_mode": help_mode,
    }
    response = _request_json(submit_url, payload=payload, token=token)
    event_id = response.get("event_id")
    if not event_id:
        raise RuntimeError(f"Space response did not include an event_id: {response!r}")
    return _stream_completion(f"{result_url}/{event_id}", token=token)


def main() -> int:
    """Validates the deployed Space response contract."""
    parser = argparse.ArgumentParser(
        description="Smoke test the Pocket Tutor Space API."
    )
    parser.add_argument(
        "--space-url",
        default=_derive_space_base_url(SPACE_URL),
        help="Base hf.space URL for the deployed Space.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("HF_TOKEN"),
        help="Optional Hugging Face token for authenticated requests.",
    )
    parser.add_argument(
        "--question",
        default=DEFAULT_QUESTION,
        help="Text-only homework prompt used for the smoke test.",
    )
    parser.add_argument(
        "--grade",
        default=DEFAULT_GRADE,
        help="Learner level used for the smoke test.",
    )
    parser.add_argument(
        "--mode",
        default=DEFAULT_MODE,
        help="Help mode used for the smoke test.",
    )
    args = parser.parse_args()

    prompt = build_tutor_prompt(
        question=args.question[:QUESTION_LIMIT],
        transcript="",
        grade_band=args.grade,
        help_mode=args.mode,
        image_status="No image uploaded.",
    )
    print(f"[smoke-space] Calling {args.space_url}")
    print(f"[smoke-space] Question: {args.question}")
    print(f"[smoke-space] Grade: {args.grade} | Mode: {args.mode}")
    print(f"[smoke-space] Prompt chars: {len(prompt)}")

    try:
        outputs = _run_space_smoke(
            args.space_url,
            question=args.question[:QUESTION_LIMIT],
            grade_band=args.grade,
            help_mode=args.mode,
            token=args.token,
        )
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        RuntimeError,
        json.JSONDecodeError,
    ) as exc:
        print(f"[smoke-space] Smoke test failed: {exc}", file=sys.stderr)
        return 1

    if len(outputs) != 9:
        print(f"[smoke-space] Unexpected output count: {len(outputs)}", file=sys.stderr)
        print(outputs, file=sys.stderr)
        return 1

    labels = [
        "student_context",
        "model_output",
        "problem",
        "knowns",
        "strategy",
        "steps",
        "check",
        "hint",
        "parent",
    ]
    named_outputs = dict(zip(labels, outputs, strict=True))
    for label, value in named_outputs.items():
        print(f"[{label}]")
        print(value)
        print()

    failures = [
        label
        for label, default in (
            ("problem", DEFAULT_PROBLEM),
            ("knowns", DEFAULT_KNOWNS),
            ("strategy", DEFAULT_STRATEGY),
            ("steps", DEFAULT_STEPS),
            ("check", DEFAULT_CHECK),
            ("hint", DEFAULT_HINT),
            ("parent", DEFAULT_PARENT),
        )
        if str(named_outputs[label]).strip() in {"", default}
    ]
    if failures:
        print(
            "[smoke-space] Missing expected model sections: " + ", ".join(failures),
            file=sys.stderr,
        )
        return 1

    print("[smoke-space] Space smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
