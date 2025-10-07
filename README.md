# Trading Recommendations API

A simple Flask-based REST API for trading recommendations with cloud deployment support.

## Features

- RESTful API endpoints for trading recommendations
- Health check endpoint for monitoring
- Docker support for containerization
- Multiple cloud platform deployment options
- CI/CD pipeline with GitHub Actions

## Local Development

### Prerequisites

- Python 3.11 or higher
- Docker (optional, for containerized development)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mahersss024-oss/trading-recommendations.git
cd trading-recommendations
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Using Docker

1. Build the Docker image:
```bash
docker build -t trading-recommendations .
```

2. Run the container:
```bash
docker run -p 5000:5000 trading-recommendations
```

Or use Docker Compose:
```bash
docker-compose up
```

## API Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `GET /api/recommendations` - Get all trading recommendations
- `GET /api/recommendations/<id>` - Get a specific recommendation by ID

### Example Response

```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "symbol": "AAPL",
      "action": "BUY",
      "price": 175.50,
      "target": 185.00,
      "stop_loss": 170.00,
      "timestamp": "2024-01-01T12:00:00"
    }
  ]
}
```

## Cloud Deployment

This application can be deployed to various cloud platforms. Choose the one that best fits your needs:

### Quick Deploy Options

#### Heroku (Easiest)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

```bash
heroku create trading-recommendations-app
git push heroku main
```
See [deploy/HEROKU_DEPLOYMENT.md](deploy/HEROKU_DEPLOYMENT.md) for detailed instructions.

#### Google Cloud Platform
```bash
gcloud app deploy app.yaml
```
See [deploy/GCP_DEPLOYMENT.md](deploy/GCP_DEPLOYMENT.md) for detailed instructions.

#### AWS
```bash
eb init -p python-3.11 trading-recommendations
eb create trading-recommendations-env
```
See [deploy/AWS_DEPLOYMENT.md](deploy/AWS_DEPLOYMENT.md) for detailed instructions.

#### Azure
```bash
az webapp up --name trading-recommendations-app --runtime PYTHON:3.11
```
See [deploy/AZURE_DEPLOYMENT.md](deploy/AZURE_DEPLOYMENT.md) for detailed instructions.

#### DigitalOcean
Use the App Platform dashboard or:
```bash
doctl apps create --spec digitalocean-app.yaml
```
See [deploy/DIGITALOCEAN_DEPLOYMENT.md](deploy/DIGITALOCEAN_DEPLOYMENT.md) for detailed instructions.

### Deployment Guides

For detailed step-by-step deployment instructions for each platform, see the files in the `deploy/` directory:

- **Heroku**: [deploy/HEROKU_DEPLOYMENT.md](deploy/HEROKU_DEPLOYMENT.md)
- **AWS**: [deploy/AWS_DEPLOYMENT.md](deploy/AWS_DEPLOYMENT.md)
- **Google Cloud**: [deploy/GCP_DEPLOYMENT.md](deploy/GCP_DEPLOYMENT.md)
- **Azure**: [deploy/AZURE_DEPLOYMENT.md](deploy/AZURE_DEPLOYMENT.md)
- **DigitalOcean**: [deploy/DIGITALOCEAN_DEPLOYMENT.md](deploy/DIGITALOCEAN_DEPLOYMENT.md)

## CI/CD

This project includes a GitHub Actions workflow (`.github/workflows/ci-cd.yml`) that:
- Runs tests on every push and pull request
- Builds and tests the Docker image
- Can be extended to automatically deploy to your chosen cloud platform

## Configuration

### Environment Variables

- `PORT` - Port to run the application on (default: 5000)
- `FLASK_APP` - Flask application entry point (default: app.py)

## Project Structure

```
trading-recommendations/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── .dockerignore              # Docker ignore file
├── Procfile                   # Heroku process file
├── app.yaml                   # Google App Engine configuration
├── digitalocean-app.yaml      # DigitalOcean App Platform spec
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD pipeline
└── deploy/                    # Deployment guides
    ├── AWS_DEPLOYMENT.md
    ├── AZURE_DEPLOYMENT.md
    ├── GCP_DEPLOYMENT.md
    ├── HEROKU_DEPLOYMENT.md
    └── DIGITALOCEAN_DEPLOYMENT.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.

---

## نشر التطبيق سحابياً (Arabic Guide)

### خيارات النشر السريع

يمكن نشر هذا التطبيق على منصات سحابية متعددة. اختر المنصة التي تناسب احتياجاتك:

#### Heroku (الأسهل)
```bash
heroku create trading-recommendations-app
git push heroku main
```

#### Google Cloud
```bash
gcloud app deploy app.yaml
```

#### AWS
```bash
eb init -p python-3.11 trading-recommendations
eb create trading-recommendations-env
```

#### Azure
```bash
az webapp up --name trading-recommendations-app --runtime PYTHON:3.11
```

#### DigitalOcean
استخدم لوحة التحكم أو:
```bash
doctl apps create --spec digitalocean-app.yaml
```

لمزيد من التفاصيل، راجع ملفات الشرح في مجلد `deploy/`
