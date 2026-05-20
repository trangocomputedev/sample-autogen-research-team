import pytest
from pathlib import Path


@pytest.mark.asyncio
async def test_web_search_returns_string():
    from src.tools.web_search import web_search
    result = await web_search("quantum computing")
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_web_search_includes_query():
    from src.tools.web_search import web_search
    result = await web_search("battery technology")
    assert "battery technology" in result


@pytest.mark.asyncio
async def test_fetch_url_returns_string():
    from src.tools.web_search import fetch_url
    result = await fetch_url("https://example.com/article")
    assert isinstance(result, str)
    assert "example.com" in result


@pytest.mark.asyncio
async def test_save_and_read_report(tmp_path, monkeypatch):
    import src.tools.file_tools as ft
    monkeypatch.setattr(ft, "_OUTPUT_DIR", tmp_path)

    content = "# Test Report\n\nHello world."
    result = await ft.save_report("test_report", content)
    assert "test_report" in result

    read_back = await ft.read_report("test_report")
    assert read_back == content


@pytest.mark.asyncio
async def test_save_report_adds_md_extension(tmp_path, monkeypatch):
    import src.tools.file_tools as ft
    monkeypatch.setattr(ft, "_OUTPUT_DIR", tmp_path)

    await ft.save_report("no_extension", "content")
    assert (tmp_path / "no_extension.md").exists()


@pytest.mark.asyncio
async def test_read_nonexistent_report():
    from src.tools.file_tools import read_report
    result = await read_report("does_not_exist_xyz_abc")
    assert "No report found" in result
