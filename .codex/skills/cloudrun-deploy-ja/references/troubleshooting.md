# トラブルシューティング (Cloud Run)

## 403 / 401 が返る
- `--allow-unauthenticated` を使ったか確認する。
- 認証必須の場合は `gcloud run services add-iam-policy-binding` で `roles/run.invoker` を付与する。

## デプロイが失敗する / 権限エラー
- `gcloud config get-value project` が正しいか確認する。
- Artifact Registry を使う場合は `roles/artifactregistry.writer` が必要。
- `gcloud auth configure-docker` を実行したか確認する。

## 起動失敗 / ヘルスチェック失敗
- アプリが `PORT` 環境変数のポートで待ち受けているか確認する。
- `--port` を指定している場合はアプリ側も一致させる。
- ログを読んでスタックトレースを確認する。

## Buildpacks で失敗する
- 言語/ランタイムが自動検出できる構成か確認する。
- Dockerfile でのデプロイに切り替える。

## 画像の push に失敗する
- `IMAGE_URI` のリージョンと `REGION` が一致しているか確認する。
- Artifact Registry のリポジトリが存在するか確認する。

## ロールバックしても直らない
- 直近の正常リビジョン名を再確認する。
- 依存する Secret/環境変数の変更が原因でないか確認する。
