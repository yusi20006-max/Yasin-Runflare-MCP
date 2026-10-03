# Security and Permission Model

This project is deliberately scoped.

## Hard stops

Stop on unknown production targets, ambiguous projects, destructive commands, credential creation/rotation, force-push, command injection/path traversal risk, unexplained infrastructure changes, undocumented API requirements, or inability to determine impact.

## Credentials

Authentication belongs to the configured official Runflare CLI. The MCP server never accepts, returns, persists, copies, or prints credentials.

## Execution

No generic command-string tool exists. CLI arguments are passed as an argv array with `shell=False`, bounded output, timeout, and project-directory validation.

## Sensitive output

Logs/events are redacted and capped. Secrets, authorization headers, cookies, tokens, passwords, and API keys must not be persisted in issues, commits, CI artifacts, or releases.

## Production

Deploy/start/restart are available only for an explicitly configured project. Stop/delete/reset and other destructive production changes require explicit confirmation outside autonomous execution.

## Scope

Only this repository, explicitly configured local project directories, the explicitly configured Runflare project, and `yusi20006-max/hermes-runflare` integration validation are in scope.
