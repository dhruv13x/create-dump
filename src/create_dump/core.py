# src/create_dump/core.py
"""Core models and configuration.

Pydantic models for validation, config loading.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator

from .utils import logger

import toml

# Canonical pattern for dump artifacts (imported/used by modules)
DEFAULT_DUMP_PATTERN = r".*_all_create_dump_\d{8}_\d{6}\.(md(\.gz)?|sha256)$"  # NEW: Strict brandmark regex


class Config(BaseModel):
    """Validated config with env support."""

    default_includes: List[str] = Field(default_factory=list)
    default_excludes: List[str] = Field(default_factory=list)
    use_gitignore: bool = True
    git_meta: bool = True  # Added: Default enables Git metadata inclusion
    max_file_size_kb: Optional[int] = Field(None, ge=0)
    dest: Optional[Path] = Field(None, description="Default output destination (CLI --dest overrides)")
    dump_pattern: str = Field(DEFAULT_DUMP_PATTERN, description="Canonical regex for dump artifacts (enforces isolation)")  # NEW
    excluded_dirs: List[str] = Field(
        default_factory=lambda: [
            "__pycache__",
            ".git",
            ".venv",
            "venv",
            "myenv",
            ".mypy_cache",
            ".pytest_cache",
            ".idea",
            "node_modules",
            "build",
            "dist",
            "vendor",
            ".gradle",
            ".tox",
            "eggs",
            ".egg-info",
        ]
    )
    metrics_port: int = Field(8000, ge=1, le=65535)

    @field_validator("max_file_size_kb", mode="before")
    @classmethod
    def non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError("must be non-negative")
        return v

    @field_validator("dest", mode="before")
    @classmethod
    def validate_dest(cls, v):
        if v is not None:
            try:
                path = Path(v)
                if not path.name:  # Warn on empty
                    logger.warning("Empty dest path; defaulting to None.")
                    return None
                return path
            except Exception as e:
                logger.warning("Invalid dest path '%s': %s; defaulting to None.", v, e)
                return None
        return v

    @field_validator("dump_pattern", mode="after")
    @classmethod
    def validate_dump_pattern(cls, v):
        """Ensure pattern is non-empty and warn on loose matches."""
        if not v or not re.match(r'.*_all_create_dump_', v):  # Basic sanity
            logger.warning("Loose or invalid dump_pattern '%s'; enforcing default: %s", v, DEFAULT_DUMP_PATTERN)
            return DEFAULT_DUMP_PATTERN
        return v


class GitMeta(BaseModel):
    branch: Optional[str] = None
    commit: Optional[str] = None


class DumpFile(BaseModel):
    """Processed file metadata (no content for memory safety)."""

    path: str
    language: Optional[str] = None
    temp_path: Optional[Path] = None  # Temp content file
    error: Optional[str] = None


def load_config(path: Optional[Path] = None) -> Config:
    """
    >>> config = load_config()
    """
    config_data: Dict[str, Any] = {}
    possible_paths = (
        [path]
        if path
        else [
            Path.home() / ".create_dump.toml",
            Path.cwd() / ".create_dump.toml",
            Path("create_dump.toml"),
        ]
    )
    for conf_path in possible_paths:
        if conf_path.exists():
            try:
                full_data = toml.load(conf_path)
                # NEW: Load from [tool.create-dump] namespace
                config_data = full_data.get("tool", {}).get("create-dump", {})
                logger.debug("Config loaded", path=conf_path, keys=list(config_data.keys()))
                break
            except (toml.TomlDecodeError, OSError) as e:
                logger.warning("Config load failed", path=conf_path, error=str(e))
    # Fallback: CLI args (e.g., dest) override post-load in run_single/run_batch
    return Config(**config_data)