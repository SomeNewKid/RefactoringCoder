"""Command-line interface for Refactoring Coder."""

from __future__ import annotations

import sys

from url_slug_maker.utilities import create_url_slug


def main(argv: list[str] | None = None) -> int:
    """Run the command-line interface."""
    prompt = _get_prompt(argv)
    if not prompt:
        example = "This title is to become a slug"
        raise SystemExit(f'Usage: python -m url_slug_maker "{example}"')
    slug = create_url_slug(prompt)
    print("URL slug:", slug)
    return 0


def _get_prompt(argv: list[str] | None = None) -> str:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        return ""

    return " ".join(args)
