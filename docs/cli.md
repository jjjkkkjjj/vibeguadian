## 1. CLIコマンド体系（`clap` インターフェース）

普段の開発で使うのは実質 `vs run` だけになるよう、極力シンプルに保ちます。

### 基本コマンドツリー

```bash
vg [OPTIONS] <COMMAND>

Commands:
  run     [主機能] 指定したコマンドをVibeguard環境下（注入・プロキシ・マスク有効）で実行する
  init    現在のディレクトリに vibeguard.toml を生成する
  set     グローバル領域（~/.vibeguard）にシークレットを安全に登録する
  status  現在のディレクトリのプロキシ稼働状況や注入予定のキー一覧（マスク済）を確認する
```

### `vg run` の設計（コア機能）

`clap` で実装する場合、アプリの実行コマンド（`npm run dev` など）を残りの引数として丸ごと受け取るために `TrailingVarArg` パターンを使います。

```rust
// 内部的なclapの構造イメージ
#[derive(Parser)]
struct RunArgs {
    /// 使用する環境プロファイル（デフォルト: "dev"）
    #[arg(short, long, default_value = "dev")]
    profile: String,

    /// ログマスク機能を無効化する（非推奨）
    #[arg(long)]
    no_mask: bool,

    /// プロキシサーバーを起動しない
    #[arg(long)]
    no_proxy: bool,

    /// 実行するコマンド（例: npm run dev）
    #[arg(trailing_var_arg = true, required = true)]
    command: Vec<String>,
}
```

**実際の使用感:**
```bash
$ vg run -- npm run dev
[Vibeguard] 🚀 Proxy started at localhost:8080
[Vibeguard] 💉 Injected 3 env vars (Profile: dev)
[Vibeguard] 🛡️ Log masking enabled
> next dev
...
```

---

## 2. `vibeguard.toml` の設計（プロジェクト設定）

このファイルはプロジェクトルートに置き、**Gitにコミットしても、CursorなどのAIに読み込ませても100%安全**な設計にします。実際のキー（値）は一切持たず、「どのキーをどこに差し込むか」という**ポインタ（参照）**だけを記述します。

### 設定ファイルの実例

```toml
# vibeguard.toml
[project]
name = "my-awesome-app"
default_profile = "dev"

# --------------------------------------------------------
# 1. Inject Mode（環境変数のメモリ注入）の設定
# --------------------------------------------------------
[env.dev]
# 左辺がアプリから見える環境変数名。右辺がグローバル領域のシークレット参照パス
DATABASE_URL = "secret://global/supabase/dev_db_url"
NEXT_PUBLIC_API_URL = "http://localhost:8080/proxy/api" # プロキシを通すため平文でOK

[env.prod]
DATABASE_URL = "secret://global/supabase/prod_db_url"

# --------------------------------------------------------
# 2. Proxy Mode（ローカルAPIプロキシ）の設定
# --------------------------------------------------------
[[proxy.routes]]
path = "/proxy/stripe"
target = "https://api.stripe.com"
# ヘッダーにシークレットを動的に合成して付与
inject_headers = { Authorization = "Bearer ${secret://global/stripe/secret_key}" }

[[proxy.routes]]
path = "/proxy/openai"
target = "https://api.openai.com/v1"
inject_headers = { Authorization = "Bearer ${secret://global/openai/api_key}" }
```

### なぜこれがAI対策として完璧なのか？

AIエージェントがこの `vibeguard.toml` を読み込むと、以下のように振る舞います。

* **AIの思考:** 「なるほど、このプロジェクトはDBに繋ぐために `DATABASE_URL` が必要なんだな。そしてStripe APIを叩く時は `http://localhost:8080/proxy/stripe` にリクエストを送ればいいんだな。よし、その通りにコードを書こう！」
* **結果:** AIは自律的に正しいコード（Prismaのスキーマ設定や、fetchの宛先など）を書き上げます。しかし、AI自身は `secret://global/stripe/secret_key` の中身（本当のAPIキー）を知らないため、外部への情報漏洩や、ターミナルログからのキー流出は物理的に起こり得ません。

