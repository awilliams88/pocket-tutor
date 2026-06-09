from __future__ import annotations

from typing import Any
import gradio as gr
from gradio.themes import Soft

from core.analyzer import analyze_homework_ui, reset_outputs
from env.config import APP_DESCRIPTION, APP_TITLE, GITHUB_URL, SPACE_URL
from ui.examples import render_examples


def get_theme() -> Any:
    """Returns the custom soft theme configured for a blackboard tutoring palette."""
    # Pair the CSS with a teal classroom palette.
    return Soft(primary_hue="teal", secondary_hue="amber", neutral_hue="zinc")


def create_app() -> gr.Blocks:
    """Creates and lays out the Gradio interface for Pocket Tutor."""
    with gr.Blocks(title=APP_TITLE) as demo:
        # Header gives the product promise without a marketing page.
        gr.Markdown(f"# {APP_TITLE}\n{APP_DESCRIPTION}", elem_id="pt-header")
        gr.Markdown(
            "Point at the problem. Ask naturally. Learn the next step.",
            elem_id="pt-kicker",
        )

        with gr.Row(elem_classes=["pt-main-grid"]):
            with gr.Column(scale=1, elem_classes=["pt-input-panel"]):
                gr.Markdown("## Question and Inputs")
                question_input = gr.Textbox(
                    label="What should we work on?",
                    lines=8,
                    placeholder="Type the problem, paste the confusing line, or explain what you already tried.",
                    elem_id="pt-question-input",
                )
                image_input = gr.Image(
                    label="Upload or capture a worksheet/photo",
                    type="filepath",
                    sources=["upload", "webcam", "clipboard"],
                    elem_classes=["pt-image-input"],
                )
                audio_input = gr.Audio(
                    label="Ask with your microphone",
                    sources=["microphone", "upload"],
                    type="filepath",
                    elem_classes=["pt-audio-input"],
                )

            with gr.Column(scale=1, elem_classes=["pt-capture-panel"]):
                gr.Markdown("## Teaching Controls")
                with gr.Column(elem_classes=["pt-control-stack"]):
                    with gr.Column(elem_classes=["pt-control-card"]):
                        gr.Markdown("### Grade band")
                        grade_input = gr.Radio(
                            ["Elementary", "Middle school", "High school", "College"],
                            value="Middle school",
                            label="Pick the learner level",
                            elem_id="pt-grade-control",
                            elem_classes=["pt-grade-input"],
                        )
                    with gr.Column(elem_classes=["pt-control-card"]):
                        gr.Markdown("### Help mode")
                        mode_input = gr.Radio(
                            ["Coach me", "Hint only", "Step-by-step"],
                            value="Coach me",
                            label="Choose the help style",
                            elem_id="pt-mode-control",
                            elem_classes=["pt-mode-input"],
                        )
                    run_button = gr.Button(
                        "Teach Me",
                        variant="primary",
                        min_width=0,
                        elem_classes=["pt-run-btn", "pt-teach-btn"],
                    )

        with gr.Column(elem_classes=["pt-results-section"]):
            with gr.Column(elem_classes=["pt-analysis-section"]):
                gr.Markdown("## Tutoring Plan")
                with gr.Row(elem_classes=["pt-plan-grid"]):
                    problem_output = gr.Textbox(
                        label="Problem Read",
                        interactive=False,
                        elem_classes=["pt-output-card", "pt-problem-card"],
                    )
                    knowns_output = gr.Textbox(
                        label="Knowns",
                        interactive=False,
                        elem_classes=["pt-output-card", "pt-knowns-card"],
                    )
                    strategy_output = gr.Textbox(
                        label="Strategy",
                        interactive=False,
                        elem_classes=["pt-output-card", "pt-strategy-card"],
                    )
                gr.Markdown("## Workbench")
                with gr.Row(elem_classes=["pt-workbench-grid"]):
                    steps_output = gr.Textbox(
                        label="Worked Steps",
                        interactive=False,
                        elem_classes=["pt-output-card", "pt-steps-card"],
                    )
                    check_output = gr.Textbox(
                        label="Check",
                        interactive=False,
                        elem_classes=["pt-output-card", "pt-check-card"],
                    )
                with gr.Row(elem_classes=["pt-workbench-grid"]):
                    hint_output = gr.Textbox(
                        label="Next Hint",
                        interactive=False,
                        elem_classes=["pt-output-card", "pt-hint-card"],
                    )
                    parent_output = gr.Textbox(
                        label="Parent Note",
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

        with gr.Accordion(
            "Diagnostics & Local Execution Logs",
            open=False,
            elem_classes=["pt-diagnostics-section"],
        ):
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
            api_name="analyze_homework_ui",
        )

    return demo
