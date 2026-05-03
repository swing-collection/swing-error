# -*- coding: utf-8 -*-

"""Renderer registry for structured error responses."""

from __future__ import annotations

# Import | Standard Library
import json
from collections.abc import Callable
from html import escape
from typing import Any, TypeAlias

RendererFunc: TypeAlias = Callable[[dict[str, Any], int], tuple[str, str]]


def _to_xml(value: Any, tag_name: str) -> str:
    """Serialize a basic Python value tree into simple XML."""
    if isinstance(value, dict):
        children = "".join(_to_xml(item, key) for key, item in value.items())
        return f"<{tag_name}>{children}</{tag_name}>"
    if isinstance(value, list):
        children = "".join(_to_xml(item, "item") for item in value)
        return f"<{tag_name}>{children}</{tag_name}>"
    if value is None:
        return f"<{tag_name}></{tag_name}>"
    return f"<{tag_name}>{escape(str(value))}</{tag_name}>"


def _to_yaml_lines(value: Any, indent: int = 0) -> list[str]:
    """Serialize a basic Python value tree into a small YAML subset."""
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(_to_yaml_lines(item, indent + 2))
            else:
                rendered = json.dumps(item) if isinstance(item, str) else str(item)
                lines.append(f"{prefix}{key}: {rendered}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(_to_yaml_lines(item, indent + 2))
            else:
                rendered = json.dumps(item) if isinstance(item, str) else str(item)
                lines.append(f"{prefix}- {rendered}")
        return lines
    rendered = json.dumps(value) if isinstance(value, str) else str(value)
    return [f"{prefix}{rendered}"]


def render_json(payload: dict[str, Any], status_code: int) -> tuple[str, str]:
    """Render the payload as JSON."""
    del status_code
    return json.dumps(payload), "application/json"


def render_problem_json(
    payload: dict[str, Any],
    status_code: int,
) -> tuple[str, str]:
    """Render the payload as RFC 7807 problem details JSON."""
    details = payload.get("details", "No additional details provided.")
    if isinstance(details, str):
        detail_text = details
        extra_details: dict[str, Any] = {}
    else:
        detail_text = payload.get("error", "Error")
        extra_details = {"errors": details}

    problem_payload: dict[str, Any] = {
        "type": payload.get("type", "about:blank"),
        "title": payload.get("error", "Error"),
        "status": status_code,
        "detail": detail_text,
    }
    problem_payload.update(extra_details)
    if "code" in payload:
        problem_payload["code"] = payload["code"]
    if "debug" in payload:
        problem_payload["debug"] = payload["debug"]
    if "instance" in payload:
        problem_payload["instance"] = payload["instance"]
    return json.dumps(problem_payload), "application/problem+json"


def render_xml(payload: dict[str, Any], status_code: int) -> tuple[str, str]:
    """Render the payload as XML."""
    del status_code
    return _to_xml(payload, "error"), "application/xml"


def render_yaml(payload: dict[str, Any], status_code: int) -> tuple[str, str]:
    """Render the payload as YAML."""
    del status_code
    return "\n".join(_to_yaml_lines(payload)) + "\n", "application/yaml"


RENDERERS: dict[str, RendererFunc] = {
    "json": render_json,
    "problem+json": render_problem_json,
    "xml": render_xml,
    "yaml": render_yaml,
}

MIME_TYPE_TO_RENDERER: dict[str, str] = {
    "application/json": "json",
    "application/problem+json": "problem+json",
    "application/xml": "xml",
    "text/xml": "xml",
    "application/yaml": "yaml",
    "application/x-yaml": "yaml",
    "text/yaml": "yaml",
}


def register_renderer(name: str, renderer: RendererFunc) -> None:
    """Register or override an error renderer."""
    RENDERERS[name] = renderer


def get_renderer(name: str) -> RendererFunc:
    """Return a renderer by registry name."""
    return RENDERERS[name]


def negotiate_renderer(accept_header: str, fallback: str = "json") -> str:
    """Return the preferred renderer name for the request accept header."""
    lowered = accept_header.lower()
    for mime_type, renderer_name in MIME_TYPE_TO_RENDERER.items():
        if mime_type in lowered:
            return renderer_name
    return fallback


__all__: list[str] = [
    "MIME_TYPE_TO_RENDERER",
    "RENDERERS",
    "RendererFunc",
    "get_renderer",
    "negotiate_renderer",
    "register_renderer",
    "render_json",
    "render_problem_json",
    "render_xml",
    "render_yaml",
]