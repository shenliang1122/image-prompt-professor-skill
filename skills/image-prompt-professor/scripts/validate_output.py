#!/usr/bin/env python3
"""Validate Image Prompt Professor JSON output without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


TOP_LEVEL = {
    "style_theme": {"primary_style", "mood", "theme", "visual_vibe"},
    "character_features": {"subject", "proportions", "pose", "facial_features", "clothing"},
    "scene_features": {"setting", "environment", "additional_details"},
    "color_palette": {"dominant_colors", "saturation", "contrast"},
    "composition_and_perspective": {
        "composition",
        "arrangement",
        "perspective",
        "depth_of_field",
        "framing",
    },
    "lighting_and_atmosphere": {"lighting", "shadows", "atmosphere"},
    "image_quality": {"resolution", "focus", "rendering_quality"},
    "typography_and_layout_potential": {"aesthetic_category", "text_space"},
}

HUMAN_RE = re.compile(r"\b(?:\d+\s*(?:girls?|boys?|women|woman|men|man|people|persons?|babies|baby|toddlers?)|crowd)\b", re.I)
FACE_TERMS = (r"\beyes?\b", r"\bnose\b", r"\blips?\b", r"\beyelashes?\b", r"\b(?:face|facial)\b")
PLACEHOLDERS = {"not applicable", "unknown"}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"Non-JSON numeric constant: {value}")


def load_document(path: str | None) -> Any:
    content = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    return json.loads(content, object_pairs_hook=unique_object, parse_constant=reject_constant)


def check_keys(value: Any, expected: set[str], location: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{location} must be an object")
        return
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{location} missing keys: {', '.join(missing)}")
    if extra:
        errors.append(f"{location} has extra keys: {', '.join(extra)}")


def check_text(value: Any, location: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        errors.append(f"{location} must be a string")
        return
    if not value.strip():
        errors.append(f"{location} must not be empty")
    if ":" in value or "." in value:
        errors.append(f"{location} contains a forbidden colon or period")
    if "\n" in value or "\r" in value:
        errors.append(f"{location} must be a single line")
    if any(ord(char) < 32 or ord(char) > 126 for char in value):
        errors.append(f"{location} must use English keywords with ASCII punctuation")
    if ";" in value:
        errors.append(f"{location} must use commas instead of semicolons")


def validate_object(document: Any, label: str) -> list[str]:
    errors: list[str] = []
    expected_top = set(TOP_LEVEL) | {"prompt"}
    check_keys(document, expected_top, label, errors)
    if not isinstance(document, dict):
        return errors

    for section, required_fields in TOP_LEVEL.items():
        section_value = document.get(section)
        check_keys(section_value, required_fields, f"{label}.{section}", errors)
        if isinstance(section_value, dict):
            for field in required_fields:
                if field in section_value:
                    check_text(section_value[field], f"{label}.{section}.{field}", errors)

    character = document.get("character_features")
    character = character if isinstance(character, dict) else {}
    subject = character.get("subject", "")
    face = character.get("facial_features", "")
    if isinstance(subject, str) and subject.strip().lower() in PLACEHOLDERS:
        errors.append(f"{label}.character_features.subject must describe the actual subject")

    scene = document.get("scene_features")
    detail_text = scene.get("additional_details", "") if isinstance(scene, dict) else ""
    details = [part.strip().lower() for part in detail_text.split(",")] if isinstance(detail_text, str) else []
    if len(set(details) - PLACEHOLDERS - {""}) < 5 or "" in details:
        errors.append(f"{label}.scene_features.additional_details needs at least five distinct details")

    prompt = document.get("prompt")
    check_text(prompt, f"{label}.prompt", errors)
    if isinstance(prompt, str):
        if not prompt.endswith(",") or prompt.endswith(",,"):
            errors.append(f"{label}.prompt must end with exactly one comma")
        if prompt[:-1].rstrip() != prompt[:-1]:
            errors.append(f"{label}.prompt has whitespace before its final comma")
        segments = [part.strip().lower() for part in prompt.removesuffix(",").split(",")]
        if "" in segments:
            errors.append(f"{label}.prompt contains an empty keyword segment")
        if len(set(segments)) != len(segments):
            errors.append(f"{label}.prompt contains duplicate keyword segments")
        if PLACEHOLDERS.intersection(segments):
            errors.append(f"{label}.prompt contains placeholder keywords")
        for detail in details:
            if detail and detail not in segments:
                errors.append(f"{label}.prompt missing detail: {detail}")

        human = isinstance(subject, str) and bool(HUMAN_RE.search(subject))
        human = human or (isinstance(face, str) and bool(face.strip()) and face.lower() not in PLACEHOLDERS)
        if human:
            for field, value in (("character_features.facial_features", face), ("prompt", prompt)):
                if isinstance(value, str):
                    for term in FACE_TERMS:
                        if not re.search(term, value, re.I):
                            errors.append(f"{label}.{field} missing human face category: {term}")

    return errors


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        document = load_document(path)
    except (OSError, ValueError) as exc:
        print(f"Invalid JSON input: {exc}", file=sys.stderr)
        return 1

    objects = document if isinstance(document, list) else [document]
    if not objects:
        print("JSON array must not be empty", file=sys.stderr)
        return 1

    errors: list[str] = []
    for index, item in enumerate(objects):
        label = f"$[{index}]" if isinstance(document, list) else "$"
        errors.extend(validate_object(item, label))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Valid Image Prompt Professor output: {len(objects)} object(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
