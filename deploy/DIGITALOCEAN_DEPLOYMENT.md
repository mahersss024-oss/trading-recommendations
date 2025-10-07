# DigitalOcean App Platform Deployment

## Prerequisites
- DigitalOcean account
- doctl CLI installed (optional)

## Deployment Steps

### Option 1: Via DigitalOcean Dashboard

1. Login to DigitalOcean
2. Go to App Platform
3. Click "Create App"
4. Select GitHub repository: `mahersss024-oss/trading-recommendations`
5. Select branch: `main`
6. Configure the app:
   - **Name**: trading-recommendations
   - **Type**: Web Service
   - **Build Command**: (auto-detected)
   - **Run Command**: `gunicorn --bind :$PORT app:app`
   - **Port**: 5000
7. Choose a plan (Basic - $5/month recommended for testing)
8. Click "Create Resources"

### Option 2: Via doctl CLI

#### 1. Install doctl
```bash
# macOS
brew install doctl

# Linux
cd ~
wget https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz
tar xf ~/doctl-1.94.0-linux-amd64.tar.gz
sudo mv ~/doctl /usr/local/bin
```

#### 2. Authenticate
```bash
doctl auth init
```

#### 3. Create App Spec File
See `digitalocean-app.yaml` for configuration

#### 4. Deploy Application
```bash
doctl apps create --spec digitalocean-app.yaml
```

#### 5. Get App Info
```bash
doctl apps list
```

## Docker Container Deployment

DigitalOcean also supports direct Docker deployment from Docker Hub or DigitalOcean Container Registry.
