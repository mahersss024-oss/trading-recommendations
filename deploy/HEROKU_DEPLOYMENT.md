# Heroku Deployment

## Prerequisites
- Heroku account
- Heroku CLI installed

## Deployment Steps

### 1. Login to Heroku
```bash
heroku login
```

### 2. Create Heroku App
```bash
heroku create trading-recommendations-app
```

### 3. Deploy Application
```bash
git push heroku main
```

### 4. Open Application
```bash
heroku open
```

### 5. View Logs
```bash
heroku logs --tail
```

## Alternative: Deploy with Docker

### 1. Login to Heroku Container Registry
```bash
heroku container:login
```

### 2. Push Docker Image
```bash
heroku container:push web -a trading-recommendations-app
```

### 3. Release the Image
```bash
heroku container:release web -a trading-recommendations-app
```

## Environment Variables

Set environment variables if needed:
```bash
heroku config:set VARIABLE_NAME=value -a trading-recommendations-app
```
