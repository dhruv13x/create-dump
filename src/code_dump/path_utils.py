# src/code_dump/path_utils.py
"""Shared utilities for path safety, discovery, and user confirmation."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import List

from .utils import logger  # For warnings

__all__ = ["safe_is_within", "find_matching_files", "confirm"]


def safe_is_within(path: Path, root: Path) -> bool:
    """Check if path is safely within root (relative/escape-proof)."""
    try:
        return path.resolve().is_relative_to(root.resolve())
    except AttributeError:
        return str(path.resolve()).startswith(str(root.resolve()) + "/")


def find_matching_files(root: Path, regex: str) -> List[Path]:
    """Glob files matching regex within root."""
    pattern = re.compile(regex)
    return [p for p in root.rglob("*") if pattern.search(p.name)]


def confirm(prompt: str) -> bool:
    """Prompt user for yes/no; handles interrupt gracefully."""
    try:
        ans = input(f"{prompt} [y/N]: ").strip().lower()
    except KeyboardInterrupt:
        print()
        return False
    return ans in ("y", "yes")
