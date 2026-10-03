from yasin_runflare_mcp import server

class FakeResult:
    def __init__(self, returncode=0, stdout="ok", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr

class FakeCLI:
    def deploy(self):
        return FakeResult()
    def events(self, follow=False):
        return FakeResult(stdout="events")
    def logs(self, follow=False):
        return FakeResult(stdout="logs")

def test_deploy_and_verify(monkeypatch):
    monkeypatch.setattr(server, "RunflareCLI", FakeCLI)
    result = server.runflare_deploy_and_verify()
    assert result["ok"] is True
    assert result["stage"] == "verification"
    assert result["deploy"]["ok"] is True
    assert result["events"]["stdout"] == "events"
    assert result["logs"]["stdout"] == "logs"

class FailingCLI(FakeCLI):
    def deploy(self):
        return FakeResult(returncode=1, stderr="deploy failed")

def test_deploy_and_verify_stops_after_failed_deploy(monkeypatch):
    monkeypatch.setattr(server, "RunflareCLI", FailingCLI)
    result = server.runflare_deploy_and_verify()
    assert result["ok"] is False
    assert result["stage"] == "deploy"
    assert "events" not in result
