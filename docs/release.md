# リリース手順

`v*` タグを push するだけで GitHub Actions が自動的にビルド・リリースを行います。

---

## 手順

### 1. バージョンを更新

`Cargo.toml` の `version` を更新します。

```toml
# Cargo.toml
version = "0.2.0"
```

### 2. ビルド確認

```bash
./cargo-docker test
./cargo-docker clippy -- -D warnings
```

### 3. コミット → タグ → Push

```bash
git add Cargo.toml
git commit -m "chore: bump version to v0.2.0"

git tag v0.2.0
git push origin main
git push origin v0.2.0   # ← これが CI のトリガー
```

タグは必ず `v` プレフィックスをつける（`v0.2.0` ○ / `0.2.0` ×）。

---

## CI が行うこと

`.github/workflows/release.yml` が起動し、4プラットフォームを並列ビルドします。

| ターゲット | Runner | 成果物 |
|---|---|---|
| `aarch64-apple-darwin` | macos-latest | `vs-vX.X.X-aarch64-apple-darwin.tar.gz` |
| `x86_64-apple-darwin` | macos-latest | `vs-vX.X.X-x86_64-apple-darwin.tar.gz` |
| `x86_64-unknown-linux-gnu` | ubuntu-22.04 | `vs-vX.X.X-x86_64-unknown-linux-gnu.tar.gz` |
| `x86_64-pc-windows-msvc` | windows-latest | `vs-vX.X.X-x86_64-pc-windows-msvc.zip` |

ビルド完了後、GitHub Release が自動作成され各バイナリが添付されます。
リリースノートはコミット履歴から自動生成されます（`generate_release_notes: true`）。

---

## トラブルシューティング

**タグを打ち直したい場合（ローカルにのみタグを打った場合）:**

```bash
git tag -d v0.2.0
git tag v0.2.0
git push origin v0.2.0
```

**既に push したタグを修正したい場合（非推奨、注意して実施）:**

```bash
git tag -d v0.2.0
git push origin :refs/tags/v0.2.0   # リモートのタグを削除
git tag v0.2.0
git push origin v0.2.0
```

**CI のログを確認する場所:**

GitHub リポジトリ → Actions タブ → "Release" ワークフロー
