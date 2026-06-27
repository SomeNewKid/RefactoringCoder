"""Tools for the Refactoring Coder project."""

from __future__ import annotations

import subprocess
from pathlib import Path

CODE_FILE_PATH = "src/url_slug_maker/utilities.py"
TEST_FILE_PATH = "tests/test_utilities.py"
SCRIPT_FILE_PATH = "scripts/check.ps1"

VERBOSE_LOGGING = True


def read_code_file() -> str:
    """
    Returns the content of the code file.

    Returns:
        (str) : the content of the code file
    """
    if VERBOSE_LOGGING:
        print("Tool called: read_code_file")

    return _read_file(CODE_FILE_PATH)


def read_test_file() -> str:
    """
    Returns the content of the unit test file.

    Returns:
        (str) : the content of the unit test file
    """
    if VERBOSE_LOGGING:
        print("Tool called: read_test_file")

    return _read_file(TEST_FILE_PATH)


def save_code_file(content: str) -> None:
    """
    Replaces the content of the code file.

    Args:
        content (str) : the new code

    Returns:
        None
    """
    if VERBOSE_LOGGING:
        print("Tool called: save_code_file")

    _save_file(CODE_FILE_PATH, content)


def save_test_file(content: str) -> None:
    """
    Replaces the content of the unit test file.

    Args:
        content (str) : the new unit test code

    Returns:
        None
    """
    if VERBOSE_LOGGING:
        print("Tool called: save_test_file")

    _save_file(TEST_FILE_PATH, content)


def run_project_checks() -> str:
    """
    Run the project check script and return its output.

    Returns:
        (str) : the output of the check script
    """
    if VERBOSE_LOGGING:
        print("Tool called: run_project_checks")

    cwd = Path.cwd()
    script_location = cwd / SCRIPT_FILE_PATH

    if not script_location.exists() or not script_location.is_file():
        raise ValueError("The script does not exist.")

    completed_process = subprocess.run(
        [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(script_location),
        ],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )

    if completed_process.returncode == 0:
        status = "PASSED"
    else:
        status = "FAILED"

    output_parts = []

    output_parts.append(status)
    output_parts.append(f"Exit code: {completed_process.returncode}")
    output_parts.append("")

    if completed_process.stdout:
        output_parts.append("STDOUT:")
        output_parts.append(completed_process.stdout.rstrip())

    if completed_process.stderr:
        output_parts.append("STDERR:")
        output_parts.append(completed_process.stderr.rstrip())

    return "\n".join(output_parts)


def _read_file(file_path: str) -> str:
    cwd = Path.cwd()
    file_location = cwd / file_path

    if not file_location.exists() or not file_location.is_file():
        raise ValueError("The file does not exist.")

    return file_location.read_text(encoding="utf-8")


def _save_file(file_path: str, content: str) -> None:
    cwd = Path.cwd()
    file_location = cwd / file_path

    file_location.write_text(content, encoding="utf-8")
