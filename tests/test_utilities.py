"""Tests for URL slug generation."""

from __future__ import annotations

from url_slug_maker.utilities import create_url_slug


def test_create_url_slug_converts_title_to_simple_slug() -> None:
    """Verify simple title words become a lowercase hyphenated slug."""
    slug = create_url_slug('This is the season\'s "new thing".')

    assert slug == "this-is-the-seasons-new-thing"
