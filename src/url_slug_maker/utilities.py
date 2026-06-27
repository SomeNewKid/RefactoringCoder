"""Utilities for the URL slug maker."""

from __future__ import annotations

import unicodedata


def create_url_slug(title: str) -> str:
    """Create a URL slug from a title."""
    lower_case_title = title.lower()

    accented_characters_normalized = unicodedata.normalize("NFKD", lower_case_title)

    ascii_bytes = accented_characters_normalized.encode("ascii", "ignore")

    ascii_title = ascii_bytes.decode("ascii")

    apostrophe_characters_removed = ""
    for character in ascii_title:
        if character == "'":
            continue

        apostrophe_characters_removed += character

    whitespace_normalized = ""
    previous_character_was_whitespace = False
    for character in apostrophe_characters_removed:
        if character.isspace():
            if previous_character_was_whitespace:
                continue

            whitespace_normalized += " "
            previous_character_was_whitespace = True
            continue

        whitespace_normalized += character
        previous_character_was_whitespace = False

    punctuation_replaced_with_hyphens = ""
    previous_character_was_hyphen = False
    for character in whitespace_normalized:
        if character.isascii() and character.isalnum():
            punctuation_replaced_with_hyphens += character
            previous_character_was_hyphen = False
            continue

        if previous_character_was_hyphen:
            continue

        punctuation_replaced_with_hyphens += "-"
        previous_character_was_hyphen = True

    slug_without_outer_hyphens = punctuation_replaced_with_hyphens.strip("-")

    words = []
    current_word = ""
    for character in slug_without_outer_hyphens:
        if character == "-":
            if current_word:
                words.append(current_word)

            current_word = ""
            continue

        current_word += character

    if current_word:
        words.append(current_word)

    maximum_slug_length = 100
    final_slug = ""
    for word in words:
        if not final_slug:
            candidate_slug = word
        else:
            candidate_slug = final_slug + "-" + word

        if len(candidate_slug) > maximum_slug_length:
            break

        final_slug = candidate_slug

    return final_slug
