"""Command-line interface for Refactoring Coder."""

from __future__ import annotations

from refactoring_coder.agent import run_agent


def main() -> int:
    """Run the command-line interface."""
    description = run_agent()
    print(description)
    return 0
