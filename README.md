# Yasin-Runflare-MCP

Scoped MCP operator for the official Runflare CLI.

## Architecture

ChatGPT → MCP → scoped Runflare CLI adapter → official `runflare` CLI → Runflare.

The server intentionally exposes narrowly scoped operations rather than arbitrary shell execution or an undocumented Runflare API.

## Tools

- `runflare_status` — non-destructive status/verification
- `runflare_deploy` — deploy current configured project
- `runflare_logs` — bounded, redacted logs
- `runflare_events` — bounded, redacted events
- `runflare_restart` — restart
- `runflare_start` — start
- `runflare_stop` — confirmation-gated destructive-ish operation

All CLI execution uses argument arrays, timeouts, bounded output, path validation, and credential redaction.

## Permission boundaries

Routine inspection, deployment, logs/events, tests, and normal GitHub lifecycle work are autonomous within this repository and an explicitly configured Runflare project.

Confirmation is required for production stop, deletion/reset, persistent-data removal, production secret changes, credential creation/rotation/revocation, DNS/billing/resource-plan changes, force-push/history rewriting, and other destructive or security-sensitive actions.

Credentials are never accepted as MCP arguments, returned by tools, persisted by this server, or printed.

## Configuration

Set the explicit project directory with `RUNFLARE_PROJECT_DIR`. The directory must be configured and must not escape its allowed root.

Optional:
- `RUNFLARE_BIN` (default: `runflare`)
- `RUNFLARE_TIMEOUT_SECONDS` (default: 120)
- `RUNFLARE_MAX_OUTPUT` (default: 12000)
- `RUNFLARE_ALLOWED_PROJECT_ROOT`

Authentication remains the responsibility of the official Runflare CLI environment.

## Development

```bash
python -m pip install -e '.[dev]'
pytest -q
```

No real Runflare credentials are required for tests.
