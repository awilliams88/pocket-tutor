from __future__ import annotations

from html import escape
import gradio as gr

# Examples cover math, science, reading, and writing support.
EXAMPLE_CARDS = [
    {
        "title": "Fraction Word Problem",
        "grade": "Middle school",
        "mode": "Coach me",
        "text": "A recipe uses 3/4 cup of flour for one batch. How much flour is needed for 2 1/2 batches?",
    },
    {
        "title": "Physics Units",
        "grade": "High school",
        "mode": "Step-by-step",
        "text": "If a bike travels 18 meters in 6 seconds, what is its average speed? I keep mixing up the units.",
    },
    {
        "title": "Reading Evidence",
        "grade": "Middle school",
        "mode": "Hint only",
        "text": "The question asks which sentence best shows the narrator is nervous. How do I choose evidence without guessing?",
    },
    {
        "title": "Essay Thesis",
        "grade": "High school",
        "mode": "Coach me",
        "text": "My essay is about whether school uniforms help students focus. My thesis sounds too broad.",
    },
]


def _example_card_html(title: str, grade: str, text: str) -> str:
    """Builds a compact example card with clear grade context."""
    return (
        '<div class="pt-example-copy">'
        '<div class="pt-example-head">'
        f"<span>{escape(title)}</span>"
        f"<strong>{escape(grade)}</strong>"
        "</div>"
        f"<p>{escape(text)}</p>"
        "</div>"
    )


def _select_example(
    text: str, grade: str, mode: str
) -> tuple[None, str, None, str, str]:
    """Populates the tutor form from an example card."""
    return None, text, None, grade, mode


def render_examples(
    image_input: gr.Image,
    question_input: gr.Textbox,
    audio_input: gr.Audio,
    grade_input: gr.Dropdown,
    mode_input: gr.Radio,
) -> gr.Column:
    """Renders examples and wires card buttons to the tutor form."""
    with gr.Column(elem_classes=["pt-examples-section"]) as section:
        gr.Markdown("## Try a Homework Scenario")
        with gr.Row(elem_classes=["pt-example-grid"]):
            for example in EXAMPLE_CARDS:
                with gr.Column(elem_classes=["pt-example-card"]):
                    gr.HTML(
                        _example_card_html(
                            str(example["title"]),
                            str(example["grade"]),
                            str(example["text"]),
                        )
                    )
                    use_example = gr.Button(
                        "Use example",
                        size="sm",
                        elem_classes=["pt-example-btn"],
                    )
                    use_example.click(
                        fn=lambda text=str(example["text"]), grade=str(example["grade"]), mode=str(example["mode"]): (
                            _select_example(text, grade, mode)
                        ),
                        inputs=[],
                        outputs=[
                            image_input,
                            question_input,
                            audio_input,
                            grade_input,
                            mode_input,
                        ],
                        queue=False,
                    )
    return section
