from __future__ import annotations

from typing import Any
import gradio as gr
from gradio.themes import Soft

from core.analyzer import analyze_homework_ui, reset_outputs
from env.config import APP_DESCRIPTION, APP_TITLE, GITHUB_URL, SPACE_URL
from ui.examples import render_examples


def get_theme() -> Any:
    """Returns the custom soft theme configured for chalkboard teal styling."""
    # Pair the CSS with a calm tutoring palette.
    return Soft(primary_hue="teal", secondary_hue="amber", neutral_hue="slate")


def create_app() -> gr.Blocks:
    """Creates and lays out the Gradio interface for Pocket Tutor."""
    with gr.Blocks(title=APP_TITLE) as demo:
        # Header gives the product promise without a marketing page.
        gr.Markdown(f"# {APP_TITLE}\n{APP_DESCRIPTION}", elem_id="pt-header")
        gr.Markdown(
            "Snap a worksheet, ask by voice, or type the confusing line. The tutor explains the next useful step.",
            elem_id="pt-kicker",
        )

        with gr.Row(elem_classes=["pt-main-grid"]):
            # Left column collects multimodal homework context.
            with gr.Column(scale=1, elem_classes=["pt-input-panel"]):
                gr.Markdown("## Homework Input")
                image_input = gr.Image(
                    label="Upload or capture a worksheet/photo",
                    type="filepath",
                    sources=["upload", "webcam", "clipboard"],
                    elem_classes=["pt-image-input"],
                )
                question_input = gr.Textbox(
                    label="What should we work on?",
                    lines=5,
                    placeholder="Type the problem, the line that confused you, or what you already tried.",
                    elem_id="pt-question-input",
                )
                audio_input = gr.Audio(
                    label="Ask with your microphone",
                    sources=["microphone", "upload"],
                    type="filepath",
                    elem_classes=["pt-audio-input"],
                )
                with gr.Row(elem_classes=["pt-control-row"]):
                    grade_input = gr.Dropdown(
                        ["Elementary", "Middle school", "High school", "College"],
                        value="Middle school",
                        label="Grade band",
                    )
                    mode_input = gr.Radio(
                        ["Coach me", "Hint only", "Step-by-step"],
                        value="Coach me",
                        label="Help mode",
                    )
                run_button = gr.Button(
                    "Tutor This",
                    variant="primary",
                    elem_classes=["pt-run-btn"],
                )

            # Right column gives the step-by-step tutoring answer.
            with gr.Column(scale=1, elem_classes=["pt-output-panel"]):
                gr.Markdown("## Tutoring Plan")
                problem_output = gr.Textbox(
                    label="Problem Read",
                    lines=4,
                    interactive=False,
                    elem_classes=["pt-output-card", "pt-problem-card"],
                )
                knowns_output = gr.Textbox(
                    label="Knowns",
                    lines=4,
                    interactive=False,
                    elem_classes=["pt-output-card", "pt-knowns-card"],
                )
                strategy_output = gr.Textbox(
                    label="Strategy",
                    lines=5,
                    interactive=False,
                    elem_classes=["pt-output-card", "pt-strategy-card"],
                )

        with gr.Column(elem_classes=["pt-analysis-section"]):
            gr.Markdown("## Workbench")
            with gr.Row(elem_classes=["pt-card-grid"]):
                steps_output = gr.Textbox(
                    label="Worked Steps",
                    lines=7,
                    interactive=False,
                    elem_classes=["pt-output-card", "pt-steps-card"],
                )
                check_output = gr.Textbox(
                    label="Check",
                    lines=7,
                    interactive=False,
                    elem_classes=["pt-output-card", "pt-check-card"],
                )
            with gr.Row(elem_classes=["pt-card-grid"]):
                hint_output = gr.Textbox(
                    label="Next Hint",
                    lines=5,
                    interactive=False,
                    elem_classes=["pt-output-card", "pt-hint-card"],
                )
                parent_output = gr.Textbox(
                    label="Parent Note",
                    lines=5,
                    interactive=False,
                    elem_classes=["pt-output-card", "pt-parent-card"],
                )

        render_examples(
            image_input,
            question_input,
            audio_input,
            grade_input,
            mode_input,
        )

        gr.Markdown(
            f"[GitHub repo]({GITHUB_URL}) | [Hugging Face Space]({SPACE_URL})",
            elem_id="pt-links",
        )

        with gr.Accordion("Diagnostics & Local Execution Logs", open=False):
            context_output = gr.Textbox(
                label="Student context",
                lines=4,
                interactive=False,
                elem_classes=["pt-log-box"],
            )
            model_output = gr.Textbox(
                label="System execution logs",
                lines=5,
                interactive=False,
                elem_classes=["pt-log-box"],
            )

        # Reset outputs immediately, then run the GPU-backed tutoring function.
        reset_event = run_button.click(
            fn=reset_outputs,
            inputs=[],
            outputs=[
                context_output,
                model_output,
                problem_output,
                knowns_output,
                strategy_output,
                steps_output,
                check_output,
                hint_output,
                parent_output,
            ],
            queue=False,
        )
        reset_event.then(
            fn=analyze_homework_ui,
            inputs=[
                image_input,
                question_input,
                audio_input,
                grade_input,
                mode_input,
            ],
            outputs=[
                context_output,
                model_output,
                problem_output,
                knowns_output,
                strategy_output,
                steps_output,
                check_output,
                hint_output,
                parent_output,
            ],
        )

    return demo
