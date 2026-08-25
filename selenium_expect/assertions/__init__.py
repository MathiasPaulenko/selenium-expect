"""Assertion class registry for selenium-expect."""

from __future__ import annotations

import importlib
from typing import Any

ASSERTION_REGISTRY: dict[str, type[Any]] = {}


def register(type_name: str, cls: type[Any]) -> None:
    """Register an assertion class for a target type name."""
    ASSERTION_REGISTRY[type_name] = cls


# Import all assertion modules to trigger their register() calls.
# Done via importlib to avoid issues with `list` being a Python builtin.
for _module_name in (
    "alert",
    "cookie",
    "driver",
    "element",
    "iframe",
    "js",
    "list",
    "select",
    "shadow",
    "window",
):
    importlib.import_module(f"selenium_expect.assertions.{_module_name}")
