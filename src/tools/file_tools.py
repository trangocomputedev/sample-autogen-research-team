from pathlib import Path

_OUTPUT_DIR = Path("outputs")


async def save_report(filename: str, content: str) -> str:
    """Save a report or article to the outputs directory as a Markdown file."""
    _OUTPUT_DIR.mkdir(exist_ok=True)
    if not filename.endswith(".md"):
        filename = filename + ".md"
    path = _OUTPUT_DIR / filename
    path.write_text(content, encoding="utf-8")
    return f"Report saved to {path}"


async def read_report(filename: str) -> str:
    """Read a previously saved report from the outputs directory."""
    if not filename.endswith(".md"):
        filename = filename + ".md"
    path = _OUTPUT_DIR / filename
    if not path.exists():
        return f"No report found at {path}"
    return path.read_text(encoding="utf-8")
