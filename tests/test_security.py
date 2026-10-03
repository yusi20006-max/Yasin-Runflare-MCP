import pytest

from yasin_runflare_mcp.cli import RunflareCLI
from yasin_runflare_mcp.security import redact, validate_project_dir

def test_redacts_common_secrets():
    value = "token=abc authorization: Bearer xyz password=secret"
    output = redact(value, 1000)
    assert "abc" not in output
    assert "xyz" not in output
    assert "secret" not in output
    assert "[REDACTED]" in output

def test_rejects_missing_project(monkeypatch):
    monkeypatch.delenv("RUNFLARE_PROJECT_DIR", raising=False)
    with pytest.raises(ValueError):
        validate_project_dir("")

def test_project_root_boundary(tmp_path, monkeypatch):
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    project = allowed / "project"
    project.mkdir()
    monkeypatch.setenv("RUNFLARE_ALLOWED_PROJECT_ROOT", str(allowed))
    assert validate_project_dir(str(project)) == project.resolve()
    with pytest.raises(ValueError):
        validate_project_dir(str(tmp_path / "outside"))

def test_no_shell_execution(monkeypatch, tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("RUNFLARE_PROJECT_DIR", str(project))
    monkeypatch.setenv("RUNFLARE_BIN", "definitely-missing-runflare")
    with pytest.raises(RuntimeError):
        RunflareCLI().run("events", "-y")

def test_argument_null_rejected(monkeypatch, tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setenv("RUNFLARE_PROJECT_DIR", str(project))
    cli = RunflareCLI()
    with pytest.raises(ValueError):
        cli.run("events", "bad\x00arg")
