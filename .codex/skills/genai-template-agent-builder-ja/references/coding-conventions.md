# コーディング規約（このリポジトリで絶対順守）

## Agents（DSPy）

- `src/agents/` 配下に置く
- ファイル名は `snake_case` で `*_agents.py`
- 1ファイルにつき `Agent` クラスを1つだけ公開
- 推奨構成:
  1) `dspy.Signature` を定義（InputField / OutputField を明示）
  2) `Agent.__init__` でLMとpredictorを構成
  3) `Agent.forward` で `dspy.settings.context(lm=...)` を使って実行
- 共有コンテキストは `utils.context_loader.build_context_bundle("system_prompt.md")` で読み込む
- 参考: `src/agents/README.md`

## API（FastAPI）

- ルータは `src/server/routers/` に作成し `APIRouter(tags=[...])` を使う
- 入出力は `pydantic.BaseModel` で定義し、`Field` で制約を付与
- エラーは `try/except` + `HTTPException` で統一
- エージェントは `lru_cache` で使い回す（既存実装に合わせる）
- 既存のAPI例を必ず参照: `src/server/routers/generate_api.py`
- 不要なフォールバックや余計な引数追加は行わない（現状の設計意図を崩さない）

## UI（HTML/CSS/JS）

- UIはルータ内に `HTML = """..."""` として定義し `HTMLResponse` を返す
- 既存UIのデザイン/構造を踏襲する（`generate_ui.py` / `image_ui.py`）
- JSは素のDOM操作で実装（外部フレームワークは使わない）
- セッションが必要なら `localStorage` を使用（既存UIの実装パターンを踏襲）
- 仕様にないフォールバック/オプション引数の追加は避ける

## ルータ登録・ドキュメント

- ルータ追加後、`src/server/main.py` に `app.include_router(...)` を追加
- READMEの `Endpoints` セクションを更新
