# Azure Web App Deployment Configuration

## Prerequisites
- Azure account with active subscription
- Azure CLI installed

## Deployment Steps

### 1. Login to Azure
```bash
az login
```

### 2. Create Resource Group
```bash
az group create --name trading-recommendations-rg --location eastus
```

### 3. Create App Service Plan
```bash
az appservice plan create \
  --name trading-recommendations-plan \
  --resource-group trading-recommendations-rg \
  --sku B1 \
  --is-linux
```

### 4. Create Web App
```bash
az webapp create \
  --resource-group trading-recommendations-rg \
  --plan trading-recommendations-plan \
  --name trading-recommendations-app \
  --runtime "PYTHON:3.11" \
  --deployment-container-image-name trading-recommendations:latest
```

### 5. Configure App Settings
```bash
az webapp config appsettings set \
  --resource-group trading-recommendations-rg \
  --name trading-recommendations-app \
  --settings PORT=8000
```

### 6. Deploy from GitHub
```bash
az webapp deployment source config \
  --name trading-recommendations-app \
  --resource-group trading-recommendations-rg \
  --repo-url https://github.com/mahersss024-oss/trading-recommendations \
  --branch main \
  --manual-integration
```
