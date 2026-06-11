from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from env.config import SUPPORTED_IMAGE_SUFFIXES

# Match headings that the tutoring model is instructed to emit.
_SECTION_MARKER_PATTERN = re.compile(
    r"(?im)^[ \t]*(?:[-*][ \t]*)?(?:#{1,6}[ \t]*)?"
    r"(?:\*\*)?(?:={2,}[ \t]*)*"
    r"(?P<label>"
    r"problem read|knowns?|strategy|worked steps?|check|next hint|parent note"
    r")"
    r"\b"
    r"(?:[ \t]*={2,})*(?:\*\*)?[ \t]*(?::|-)?[ \t]*"
    r"(?P<trailing>[^\n]*)$"
)

_SECTION_ORDER = (
    "problem",
    "knowns",
    "strategy",
    "steps",
    "check",
    "hint",
    "parent",
)

_SECTION_DEFAULTS = {
    "problem": "Upload a homework image or type the question to begin.",
    "knowns": "- No givens identified yet.",
    "strategy": "No strategy generated yet.",
    "steps": "No worked steps generated yet.",
    "check": "No answer check generated yet.",
    "hint": "Ask for a hint after the first explanation.",
    "parent": "Parent support note will appear here.",
}


def resolve_path(file_input: object | None) -> Path | None:
    """Normalizes Gradio file payload variants into a local path."""
    # Empty upload components should let text or audio drive the request.
    if not file_input:
        return None
    if isinstance(file_input, (list, tuple)):
        for item in file_input:
            path = resolve_path(item)
            if path:
                return path
        return None
    if isinstance(file_input, dict):
        for key in ("path", "name", "orig_name"):
            value = file_input.get(key)
            if value:
                return Path(str(value))
        return None
    return Path(str(file_input))


def validate_image_path(file_input: object | None) -> tuple[str | None, str]:
    """Returns a usable image path and a short validation message."""
    # Accept common classroom photo formats only.
    path = resolve_path(file_input)
    if not path:
        return None, "No image uploaded."
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_IMAGE_SUFFIXES:
        return None, f"Unsupported image format: {suffix}."
    if not path.exists():
        return None, "Uploaded image was not found in the local runtime."
    return str(path), f"Image accepted: {path.name}"


def stringify_content(content: Any) -> str:
    """Converts Gradio text, audio transcripts, and message payloads into prompt-safe text."""
    # Plain textbox messages arrive as strings.
    if content is None:
        return ""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, (list, tuple)):
        parts = [stringify_content(item) for item in content]
        return " ".join(part for part in parts if part).strip()
    if isinstance(content, dict):
        for key in ("text", "value", "path", "url", "name", "alt_text"):
            value = content.get(key)
            if value:
                return stringify_content(value)
        return ""
    return str(content).strip()


def _canonical_section(label: str) -> str:
    """Maps model heading variants onto the app's fixed output cards."""
    normalized = re.sub(r"[^a-z]+", " ", label.lower()).strip()
    if "problem" in normalized:
        return "problem"
    if "known" in normalized:
        return "knowns"
    if "strategy" in normalized:
        return "strategy"
    if "worked" in normalized or "step" in normalized:
        return "steps"
    if "check" in normalized:
        return "check"
    if "hint" in normalized:
        return "hint"
    return "parent"


def parse_sections(response: str) -> tuple[str, str, str, str, str, str, str]:
    """Extracts tutoring sections from a structured model response."""
    # Find candidate headings and keep defaults when a section is absent.
    matches = list(_SECTION_MARKER_PATTERN.finditer(response))
    sections = dict(_SECTION_DEFAULTS)
    if not matches:
        return (
            sections["problem"],
            sections["knowns"],
            sections["strategy"],
            sections["steps"],
            sections["check"],
            sections["hint"],
            sections["parent"],
        )

    # Prefer the best ordered block of sections in the generation.
    best_values: dict[str, str] = {}
    best_count = -1
    for start_index, _ in enumerate(matches):
        values: dict[str, str] = {}
        last_order_index = -1
        for current_index in range(start_index, len(matches)):
            current = matches[current_index]
            section = _canonical_section(current.group("label"))
            order_index = _SECTION_ORDER.index(section)
            if order_index <= last_order_index:
                break
            next_start = (
                matches[current_index + 1].start()
                if current_index + 1 < len(matches)
                else len(response)
            )
            value = "\n".join(
                [current.group("trailing"), response[current.end() : next_start]]
            ).strip()
            if value:
                values[section] = value
            last_order_index = order_index
        if len(values) >= best_count:
            best_values = values
            best_count = len(values)

    # Merge extracted values over stable UI defaults.
    sections.update(best_values)
    return (
        sections["problem"],
        sections["knowns"],
        sections["strategy"],
        sections["steps"],
        sections["check"],
        sections["hint"],
        sections["parent"],
    )
