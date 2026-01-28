---
name: cloudrun-deploy-ja
description: GCP Cloud Run へのデプロイ/更新/設定/ロールバックを日本語で支援するスキル。gcloud CLI を使ったビルド（Dockerfile/Buildpacks）、Artifact Registry、環境変数/Secret Manager、IAM(公開/認証)、ログ確認と疎通確認が必要なときに使う。
---

# Cloud Run Deploy (JA)

## 目的
Cloud Run に安全にデプロイ/更新し、設定と検証まで行う。

## コミュニケーション
- ユーザー向けの確認・手順・結果は日本語で行う。

## ワークフロー（順序）
1) 入力を確認する
   - PROJECT_ID / REGION / SERVICE_NAME
   - デプロイ対象パス（リポジトリのどのサービスか）
   - 公開方針（公開 or 認証必須）
   - ポート、CPU/メモリ、同時実行数、最小/最大インスタンス
   - 環境変数と Secret Manager のキー
2) 前提を確認する
   - gcloud 認証済みか確認する
   - `gcloud config set project` が正しいか確認する
   - 必要 API を有効化する（Cloud Run / Artifact Registry / Cloud Build / Secret Manager）
3) ビルド方式を決める
   - Dockerfile がある場合: Artifact Registry に build/push する
   - Dockerfile がない場合: `gcloud run deploy --source` を使う
4) デプロイする
   - 既存サービス更新の場合は影響とロールバック方針を確認する
   - `gcloud run deploy` を実行し、環境変数/シークレットを反映する
5) 検証する
   - URL を取得して疎通する
   - ログでエラーがないか確認する
6) 仕上げ
   - 変更点・URL・今後の運用注意点を簡潔に共有する

## References
- 詳細コマンドと手順: references/workflow.md
- 典型的なエラー対応: references/troubleshooting.md
