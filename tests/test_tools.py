import pytest
from mini_claude.tools.file_read import FileReadTool


@pytest.fixture
def tmp_file(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("line one\nline two\nline three\n")
    return str(f)


def test_file_read_returns_numbered_content(tmp_file):
    result = FileReadTool().execute(file_path=tmp_file)
    assert not result.is_error
    assert "1\tline one" in result.content
    assert "2\tline two" in result.content


def test_file_read_respects_offset_and_limit(tmp_file):
    result = FileReadTool().execute(file_path=tmp_file, offset=1, limit=1)
    assert not result.is_error
    assert "line two" in result.content
    assert "line one" not in result.content


def test_file_read_missing_file():
    result = FileReadTool().execute(file_path="/nonexistent/path/file.txt")
    assert result.is_error
    assert "not found" in result.content.lower() or "no such" in result.content.lower()


def test_file_read_is_read_only():
    assert FileReadTool().is_read_only() is True
