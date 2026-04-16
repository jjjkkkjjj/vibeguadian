---
name: design-review
description: Review proposed or recently written code against the vibesafer design spec. Use before finalizing any implementation.
---

1. Read `docs/design.md` and `docs/cli.md` in full.
2. Review the code or proposal under discussion.
3. Check for alignment on:
   - CLI interface (subcommands, flags, `TrailingVarArg` pattern for `vs run`)
   - Secret isolation guarantees (no secrets on disk, no secrets in `vibesafe.toml`)
   - The three core mechanisms: inject mode, proxy mode, log mask mode
   - Configuration model (`vibesafe.toml` for project config, `~/.vibesafe/secrets.json` for actual secrets)
   - Technology choices (clap, tokio, axum/hyper+reqwest, aho-corasick, serde)
4. Report any deviations from the design with specific references to the relevant section.
5. If everything aligns, confirm with a brief summary of what was checked.
