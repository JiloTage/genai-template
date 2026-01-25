---
name: genai-template-agent-builder-ja
description: GenAI Template（DSPy + FastAPI）で新しいAgent/API/UIを追加・変更する作業向けの日本語スキル。エージェント作成、ルータ追加、UIページ作成、main.py登録、README更新などが必要なときに使う。要件ヒアリングから設計・実装・確認まで一貫して進める。
---

# GenAI Template Agent Builder (JA)

## Overview

このリポジトリの構成・規約に厳密に従い、ユーザー要件をヒアリングしてAgent/API/UIを実装する。

## 必読リソース

- `references/repo-structure.md`
- `references/coding-conventions.md`

## ワークフロー

### 1) 要件ヒアリング（最小限で確実に）

- 目的と期待する出力
- エンドポイントのパスとリクエスト/レスポンス形
- 使用モデル/外部API/環境変数
- UIの入力・表示・状態管理（セッション有無）
- 既存機能に影響を与えない前提の確認

### 2) 設計合意

- 変更対象ファイルと新規追加ファイルを列挙し合意する
- 既存パターン（API/ UI/ Agent）を踏襲する方針を明示する
- 依存パッケージやENV追加の有無を確認する

### 3) 実装（規約絶対順守）

- Agents
  - `src/agents/` に `*_agents.py` を作成し `Agent` を1つだけ定義
  - `context/system_prompt.md` を読み込む
- API
  - `src/server/routers/` にルータを追加
  - `pydantic` の request/response を定義
  - `HTTPException` とログでエラー処理
- UI
  - `src/server/routers/` にHTMLResponseのUIを追加
  - 既存UIのデザイン/構造を踏襲（`generate_ui.py`/`image_ui.py`）
- ルータ登録
  - `src/server/main.py` に `app.include_router(...)` を追加
- ドキュメント
  - `README.md` の `Endpoints` を更新
- 禁止事項
  - 仕様にないフォールバックを追加しない
  - 不要な引数・オプションを勝手に増やさない
  - 既存の設計意図を変える改変はしない

### 4) 動作確認

- 可能なら `uv run uvicorn server.main:app --reload` で起動確認
- UIはブラウザで表示し、最低1つの正常系を確認
- 実行できない場合は理由と代替の確認手順を提示する

## 重要な姿勢

- 仕様に忠実に実装し、余計なフォールバック/引数追加はしない
- 情報不足や曖昧さがある場合は短く確認してから進める
- 既存の動作を壊さない前提を優先する
