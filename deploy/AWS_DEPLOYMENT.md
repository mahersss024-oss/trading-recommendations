# AWS Deployment Configuration

## Prerequisites
- AWS account
- AWS CLI configured
- Docker installed

## Deployment Options

### Option 1: AWS Elastic Beanstalk

#### 1. Install EB CLI
```bash
pip install awsebcli
```

#### 2. Initialize Elastic Beanstalk
```bash
eb init -p python-3.11 trading-recommendations --region us-east-1
```

#### 3. Create Environment and Deploy
```bash
eb create trading-recommendations-env
eb deploy
```

#### 4. Open Application
```bash
eb open
```

### Option 2: AWS ECS (Elastic Container Service)

#### 1. Build and Push Docker Image to ECR
```bash
# Create ECR repository
aws ecr create-repository --repository-name trading-recommendations

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t trading-recommendations .

# Tag image
docker tag trading-recommendations:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/trading-recommendations:latest

# Push image
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/trading-recommendations:latest
```

#### 2. Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name trading-recommendations-cluster
```

#### 3. Create Task Definition
See `ecs-task-definition.json` for configuration

#### 4. Create Service
```bash
aws ecs create-service \
  --cluster trading-recommendations-cluster \
  --service-name trading-recommendations-service \
  --task-definition trading-recommendations:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### Option 3: AWS Lambda + API Gateway

For serverless deployment, use the Serverless Framework or AWS SAM.
