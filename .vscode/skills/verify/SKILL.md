---
name: verify
description: Build, lint, and test the vibesafer codebase. Run after making changes to confirm nothing is broken.
---

Run the following in sequence from the project root and report the results:

```
cargo build
cargo clippy -- -D warnings
cargo test
```

If any step fails, show the error output and suggest a fix. Only report success if all three pass.
