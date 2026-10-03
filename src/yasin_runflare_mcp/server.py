"""MCP server exposing only scoped Runflare operations."""

from mcp.server.fastmcp import FastMCP

from .cli import RunflareCLI

mcp = FastMCP("Yasin-Runflare-MCP")

def _format(result):
    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }

@mcp.tool()
def runflare_status() -> dict:
    """Inspect Runflare events without changing infrastructure."""
    return _format(RunflareCLI().status())

@mcp.tool()
def runflare_deploy() -> dict:
    """Deploy the explicitly configured Runflare project using the official CLI."""
    return _format(RunflareCLI().deploy())

@mcp.tool()
def runflare_logs(follow: bool = False) -> dict:
    """Read bounded and redacted Runflare logs."""
    return _format(RunflareCLI().logs(follow=follow))

@mcp.tool()
def runflare_events(follow: bool = False) -> dict:
    """Read bounded and redacted Runflare events."""
    return _format(RunflareCLI().events(follow=follow))

@mcp.tool()
def runflare_restart() -> dict:
    """Restart the explicitly configured Runflare project."""
    return _format(RunflareCLI().restart())

@mcp.tool()
def runflare_start() -> dict:
    """Start the explicitly configured Runflare project."""
    return _format(RunflareCLI().start())

@mcp.tool()
def runflare_deploy_and_verify() -> dict:
    """Deploy, then inspect events and logs to provide a bounded verification result."""
    cli = RunflareCLI()
    deploy = _format(cli.deploy())
    if not deploy["ok"]:
        return {"ok": False, "stage": "deploy", "deploy": deploy}
    events = _format(cli.events())
    logs = _format(cli.logs())
    verified = events["ok"] and logs["ok"]
    return {
        "ok": verified,
        "stage": "verification",
        "deploy": deploy,
        "events": events,
        "logs": logs,
    }

@mcp.tool()
def runflare_stop(confirmed: bool = False) -> dict:
    """Stop Runflare only when the caller explicitly confirms the destructive action."""
    if not confirmed:
        return {
            "ok": False,
            "requires_confirmation": True,
            "message": "Stopping Runflare requires explicit confirmation.",
        }
    raise PermissionError(
        "Production stop must be performed outside autonomous MCP execution."
    )

def main() -> None:
    mcp.run()
