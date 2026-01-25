# Cloud Run デプロイ手順 (gcloud CLI)

## 事前に決める値
```
PROJECT_ID=your-project-id
REGION=asia-northeast1
SERVICE_NAME=your-service
IMAGE_REPO=your-repo
IMAGE_NAME=your-image
IMAGE_URI=${REGION}-docker.pkg.dev/${PROJECT_ID}/${IMAGE_REPO}/${IMAGE_NAME}:v1
ALLOW_UNAUTH=--allow-unauthenticated  # 認証必須なら --no-allow-unauthenticated
```

## 必要 API を有効化する
```
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com secretmanager.googleapis.com --project ${PROJECT_ID}
```

## Dockerfile がある場合 (Artifact Registry + Docker)
1) Artifact Registry を作成する
```
gcloud artifacts repositories create ${IMAGE_REPO} --repository-format=docker --location=${REGION} --project ${PROJECT_ID}
```
2) Docker 認証を設定する
```
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```
3) ビルドして push する
```
docker build -t ${IMAGE_URI} .
docker push ${IMAGE_URI}
```

## Dockerfile がない場合 (Buildpacks)
```
gcloud run deploy ${SERVICE_NAME} --source . --region ${REGION} --project ${PROJECT_ID} ${ALLOW_UNAUTH}
```

## デプロイ (共通)
```
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_URI} \
  --region ${REGION} \
  --project ${PROJECT_ID} \
  ${ALLOW_UNAUTH}
```

### 追加オプション (必要なものだけ使う)
```
--port 8080
--cpu 1
--memory 512Mi
--concurrency 80
--min-instances 0
--max-instances 5
--set-env-vars KEY=VALUE,KEY2=VALUE2
--set-secrets KEY=SECRET_NAME:latest
--service-account runtime-sa@${PROJECT_ID}.iam.gserviceaccount.com
```

## Secret Manager (必要な場合)
```
gcloud secrets create SECRET_NAME --replication-policy=automatic --project ${PROJECT_ID}
echo -n "secret-value" | gcloud secrets versions add SECRET_NAME --data-file=- --project ${PROJECT_ID}
```

## URL 取得と疎通確認
```
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --project ${PROJECT_ID} --format "value(status.url)")

echo ${SERVICE_URL}
curl -i ${SERVICE_URL}
```

## ログ確認
```
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=${SERVICE_NAME}" --project ${PROJECT_ID} --limit 50
```

## ロールバック
1) 直近のリビジョンを確認する
```
gcloud run revisions list --service ${SERVICE_NAME} --region ${REGION} --project ${PROJECT_ID}
```
2) トラフィックを戻す
```
gcloud run services update-traffic ${SERVICE_NAME} --region ${REGION} --project ${PROJECT_ID} --to-revisions REVISION_NAME=100
```
