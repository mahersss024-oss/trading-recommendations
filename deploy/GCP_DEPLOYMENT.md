# Google Cloud Platform Deployment

## Prerequisites
- Google Cloud account
- gcloud CLI installed

## Deployment Steps

### Option 1: Google App Engine

#### 1. Initialize gcloud
```bash
gcloud init
```

#### 2. Create a new project (or select existing)
```bash
gcloud projects create trading-recommendations-project
gcloud config set project trading-recommendations-project
```

#### 3. Enable App Engine
```bash
gcloud app create --region=us-central
```

#### 4. Deploy Application
```bash
gcloud app deploy app.yaml
```

#### 5. View Application
```bash
gcloud app browse
```

### Option 2: Google Cloud Run

#### 1. Build and Deploy with Cloud Build
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/trading-recommendations
```

#### 2. Deploy to Cloud Run
```bash
gcloud run deploy trading-recommendations \
  --image gcr.io/PROJECT_ID/trading-recommendations \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: Google Kubernetes Engine (GKE)

#### 1. Create GKE Cluster
```bash
gcloud container clusters create trading-recommendations-cluster \
  --num-nodes=2 \
  --zone=us-central1-a
```

#### 2. Build and Push Image
```bash
docker build -t gcr.io/PROJECT_ID/trading-recommendations:latest .
docker push gcr.io/PROJECT_ID/trading-recommendations:latest
```

#### 3. Deploy to GKE
```bash
kubectl create deployment trading-recommendations \
  --image=gcr.io/PROJECT_ID/trading-recommendations:latest

kubectl expose deployment trading-recommendations \
  --type=LoadBalancer \
  --port=80 \
  --target-port=5000
```

#### 4. Get External IP
```bash
kubectl get services trading-recommendations
```
