---
name: add-secret-command
description: Scaffold a new `vs` subcommand following the CLI design patterns in docs/cli.md. Invoke with the subcommand name as the argument.
disable-model-invocation: true
---

The user wants to add a new `vs` subcommand. The argument is: $ARGUMENTS

1. Read `docs/cli.md` to understand existing subcommand conventions.
2. Read `docs/design.md` for relevant architecture context.
3. Propose a plan for the new subcommand covering:
   - Subcommand name, description, and flags (following clap patterns)
   - Where it fits in the module structure (e.g., `src/commands/<name>.rs`)
   - Any interaction with inject/proxy/mask modes
   - Config or secret access patterns (only via `~/.vibesafe/secrets.json` references)
4. Wait for approval before writing any code.
5. After approval, scaffold the command with a `run()` function stub, register it in the clap app, and add a placeholder test.
