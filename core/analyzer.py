from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

try:
    import spaces
except ImportError:
    # Use a no-op GPU decorator during local development.
    class _LocalSpacesFallback:
        @staticmethod
        def GPU(
            duration: int = 30,
        ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
            def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
                return function

            return decorator

    spaces = _LocalSpacesFallback()

from core.inference import run_tutor_inference, transcribe_audio
from core.parser import parse_sections, stringify_content, validate_image_path
from env.config import MODEL_ID, PARAMETER_COUNT, QUESTION_LIMIT, TRANSCRIPT_LIMIT

# The tutor prompt keeps the app educational rather than answer-dumping.
TUTOR_SYSTEM_PROMPT = (
    "You are Pocket Tutor, a patient multimodal homework coach. "
    "Help the learner understand the problem without shaming them or simply dumping final answers. "
    "For math and science, show compact steps and check the answer. "
    "For writing or reading, explain the reasoning and offer a revision or clue. "
    "If the uploaded image is unclear, say what information is missing. "
    "Do not solve active graded tests, exams, or requests to cheat; offer study guidance instead."
)


@dataclass(frozen=True)
class TutorReport:
    """Structure containing the prompt context, execution logs, and parsed tutoring result."""

    student_context: str
    model_path: str
    problem: str
    knowns: str
    strategy: str
    steps: str
    check: str
    hint: str
    parent: str


def build_tutor_prompt(
    question: str,
    transcript: str,
    grade_band: str,
    help_mode: str,
    image_status: str,
) -> str:
    """Builds the multimodal tutoring prompt expected by the fine-tuned adapter."""
    combined_question = "\n".join(
        part for part in [question.strip(), transcript.strip()] if part
    ).strip()
    return f"""{TUTOR_SYSTEM_PROMPT}

Student grade band: {grade_band}
Help mode: {help_mode}
Image status: {image_status}

Return exactly these sections:

=== PROBLEM READ ===
[Briefly restate what the learner is asking.]

=== KNOWNS ===
- [List useful givens, facts, or constraints.]

=== STRATEGY ===
[Explain the plan in 2-4 sentences.]

=== WORKED STEPS ===
[Give concise step-by-step help. For hint mode, stop before the final answer.]

=== CHECK ===
[Check units, logic, or answer quality.]

=== NEXT HINT ===
[Ask one short follow-up question or give the smallest next hint.]

=== PARENT NOTE ===
[One sentence a parent/tutor can use to support the learner.]

Learner question:
{combined_question[:QUESTION_LIMIT] or "The learner uploaded an image and did not type a question."}
"""


def analyze_homework(
    image_file: object | None,
    question: Any,
    audio_path: object | None,
    grade_band: str,
    help_mode: str,
) -> TutorReport:
    """Orchestrates image validation, speech transcription, inference, and parsing."""
    # Convert text and microphone input before building the model prompt.
    typed_question = stringify_content(question)[:QUESTION_LIMIT]
    transcript, transcript_log = transcribe_audio(audio_path)
    transcript = transcript[:TRANSCRIPT_LIMIT]
    image_path, image_status = validate_image_path(image_file)

    # Build a traceable prompt that matches the Modal training format.
    prompt = build_tutor_prompt(
        typed_question,
        transcript,
        grade_band,
        help_mode,
        image_status,
    )
    response, inference_log = run_tutor_inference(prompt, image_path)
    sections = parse_sections(response)

    # Keep diagnostics clear but never hide whether fallback logic ran.
    model_path = "\n".join(
        [
            f"Primary model: {MODEL_ID}",
            f"Parameters: {PARAMETER_COUNT}",
            "Execution flow: local Space runtime; no external answer API",
            "---",
            image_status,
            transcript_log,
            inference_log,
        ]
    )
    student_context = "\n".join(
        part
        for part in [
            f"Grade band: {grade_band}",
            f"Help mode: {help_mode}",
            f"Typed question: {typed_question}" if typed_question else "",
            f"Voice transcript: {transcript}" if transcript else "",
            image_status,
        ]
        if part
    )
    return TutorReport(student_context, model_path, *sections)


@spaces.GPU(duration=45)
def analyze_homework_ui(
    image_file: object | None,
    question: Any,
    audio_path: object | None,
    grade_band: str,
    help_mode: str,
) -> tuple[str, str, str, str, str, str, str, str, str]:
    """Gradio-compatible GPU entry point for tutoring analysis."""
    # Convert the report into stable component outputs.
    report = analyze_homework(image_file, question, audio_path, grade_band, help_mode)
    return (
        report.student_context,
        report.model_path,
        report.problem,
        report.knowns,
        report.strategy,
        report.steps,
        report.check,
        report.hint,
        report.parent,
    )


def reset_outputs() -> tuple[str, str, str, str, str, str, str, str, str]:
    """Clears visible outputs before a fresh tutoring run."""
    # Keep click feedback immediate while the model loads.
    return (
        "Preparing tutoring context...",
        "Starting local model execution...",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
    )
