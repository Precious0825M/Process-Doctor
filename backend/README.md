# ProcessDoctor Backend

FastAPI-based backend service for ProcessDoctor workflow optimization system.

## Features

- **Workflow Analysis**: Parse and analyze CI/CD workflows
- **AI-Powered Optimization**: Generate optimized workflow configurations
- **GitHub Integration**: Create PRs with improvements
- **RESTful API**: Clean, documented API endpoints
- **Async Processing**: Non-blocking workflow analysis

## Tech Stack

- **Framework**: FastAPI
- **Python**: 3.11+
- **AI Models**: IBM Granite, IBM Bob
- **Orchestration**: IBM watsonx Orchestrate
- **Database**: PostgreSQL (optional)
- **Cache**: Redis (optional)

## Setup

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip
- Redis (optional)
- PostgreSQL (optional)

### Installation

#### Using Poetry (Recommended)

```bash
cd backend
poetry install
poetry shell
```

#### Using pip

```bash
cd backend
pip install -r requirements.txt
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp ../.env.example .env
```

Required variables:

- `GRANITE_API_KEY`: IBM Granite API key
- `BOB_API_KEY`: IBM Bob API key
- `WATSONX_ORCHESTRATE_API_KEY`: watsonx Orchestrate API key
- `GITHUB_TOKEN`: GitHub personal access token

### Running the Server

#### Development

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Production

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Using Docker

```bash
docker build -t processdoctor-backend .
docker run -p 8000:8000 --env-file .env processdoctor-backend
```

## API Documentation

Once running, visit:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **OpenAPI JSON**: <http://localhost:8000/openapi.json>

## API Endpoints

### Health Check

```
GET /health
```

### Analyze Workflow

```
POST /api/analyze
Body: {
  "workflow_input": "string",
  "source_type": "text|github|file"
}
```

### Generate Fix

```
POST /api/fix
Body: {
  "analysis_id": "string",
  "optimization_strategy": "aggressive|balanced|conservative"
}
```

### Create Pull Request

```
POST /api/pr
Body: {
  "fix_id": "string",
  "repository": "owner/repo",
  "branch": "optimization/workflow-improvements"
}
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   │
│   ├── api/                 # API endpoints
│   │   ├── analyze.py       # Workflow analysis endpoint
│   │   ├── fix.py           # Optimization endpoint
│   │   ├── pr.py            # PR creation endpoint
│   │   └── health.py        # Health check endpoint
│   │
│   ├── pipeline/            # Processing pipeline
│   │   ├── orchestrator.py  # Main orchestration logic
│   │   ├── ingestion.py     # Input processing
│   │   ├── static_analysis.py # Static workflow analysis
│   │   └── validation.py    # Validation logic
│   │
│   ├── agents/              # AI agents
│   │   ├── llm_client.py    # LLM client wrapper
│   │   ├── diagnoser.py     # Diagnostic agent
│   │   ├── fixer.py         # Optimization agent
│   │   └── pr_writer.py     # PR description generator
│   │
│   ├── github/              # GitHub integration
│   │   ├── client.py        # GitHub API client
│   │   ├── workflows.py     # Workflow operations
│   │   ├── runs.py          # Workflow run analysis
│   │   └── pr_creator.py    # PR creation logic
│   │
│   ├── schemas/             # Pydantic models
│   │   ├── workflow.py      # Workflow schemas
│   │   ├── analysis.py      # Analysis schemas
│   │   ├── fix.py           # Fix schemas
│   │   └── api.py           # API request/response schemas
│   │
│   └── prompts/             # AI prompts
│       ├── diagnoser_system.md
│       ├── fixer_system.md
│       └── pr_writer_system.md
│
├── data/                    # Static data
│   └── action_versions.json
│
├── tests/                   # Test suite
│   ├── test_static_analysis.py
│   ├── test_orchestrator.py
│   └── fixtures/
│       └── sample_workflow.yml
│
├── pyproject.toml           # Poetry configuration
├── requirements.txt         # Pip requirements
├── .python-version          # Python version
├── Dockerfile               # Docker configuration
└── README.md                # This file
```

## Development

### Running Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=app --cov-report=html
```

### Code Formatting

```bash
black app/
```

### Linting

```bash
ruff check app/
```

### Type Checking

```bash
mypy app/
```

## Configuration

### Config File: `app/config.py`

Configuration is managed through environment variables and Pydantic settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    granite_api_key: str
    bob_api_key: str
    github_token: str
    # ... more settings
```

## Database (Optional)

### Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Deployment

### Docker

```bash
docker build -t processdoctor-backend .
docker run -p 8000:8000 processdoctor-backend
```

### Docker Compose

```bash
docker-compose up backend
```

### Environment-Specific Configs

- **Development**: `.env.development`
- **Staging**: `.env.staging`
- **Production**: `.env.production`

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Metrics

Available at `/metrics` (if enabled)

### Logs

Structured JSON logging to stdout:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "message": "Workflow analyzed",
  "workflow_id": "abc123"
}
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Run `poetry install` or `pip install -r requirements.txt`

2. **API Key Errors**
   - Verify `.env` file exists and contains valid keys
   - Check key permissions and quotas

3. **Port Already in Use**
   - Change port: `uvicorn app.main:app --port 8001`
   - Kill existing process: `lsof -ti:8000 | xargs kill`

## Contributing

1. Create feature branch
2. Make changes
3. Run tests and linting
4. Submit pull request

## License

MIT
