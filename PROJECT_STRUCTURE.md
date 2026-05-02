# ProcessDoctor - Complete Project Structure

This document provides a complete overview of the ProcessDoctor project file structure.

```
processdoctor/
├── README.md                           # Project overview and getting started
├── PROJECT_STRUCTURE.md                # This file - complete structure reference
├── .gitignore                          # Git ignore patterns
├── .env.example                        # Environment variables template
├── docker-compose.yml                  # Docker orchestration configuration
│
├── docs/                               # Documentation
│   ├── architecture.md                 # System architecture documentation
│   ├── demo-script.md                  # 3-minute demo script
│   ├── prompts.md                      # AI agent prompts documentation
│   └── frontend-backend-integration-plan.md  # UX-Backend mapping plan
│
├── backend/                            # Python FastAPI backend
│   ├── README.md                       # Backend-specific documentation
│   ├── pyproject.toml                  # Poetry dependencies and config
│   ├── requirements.txt                # Pip requirements (generated from poetry)
│   ├── .python-version                 # Python version specification (3.11.0)
│   ├── Dockerfile                      # Backend container configuration
│   │
│   ├── app/                            # Main application package
│   │   ├── __init__.py                 # Package initialization
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── config.py                   # Configuration management (Pydantic settings)
│   │   │
│   │   ├── api/                        # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py              # POST /api/analyze - Workflow analysis
│   │   │   ├── fix.py                  # POST /api/fix - Generate optimizations
│   │   │   ├── pr.py                   # POST /api/pr - Create pull request
│   │   │   └── health.py               # GET /health - Health check
│   │   │
│   │   ├── pipeline/                   # Processing pipeline
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py         # Main workflow orchestration
│   │   │   ├── ingestion.py            # Input processing (text/github/file)
│   │   │   ├── static_analysis.py      # Static workflow analysis
│   │   │   └── validation.py           # Workflow validation
│   │   │
│   │   ├── agents/                     # AI agents
│   │   │   ├── __init__.py
│   │   │   ├── llm_client.py           # LLM client wrapper (Granite/Bob)
│   │   │   ├── diagnoser.py            # Diagnostic agent (IBM Bob)
│   │   │   ├── fixer.py                # Optimization agent (IBM Granite)
│   │   │   └── pr_writer.py            # PR description generator
│   │   │
│   │   ├── github/                     # GitHub integration
│   │   │   ├── __init__.py
│   │   │   ├── client.py               # GitHub API client wrapper
│   │   │   ├── workflows.py            # Workflow operations
│   │   │   ├── runs.py                 # Workflow run analysis
│   │   │   └── pr_creator.py           # PR creation logic
│   │   │
│   │   ├── schemas/                    # Pydantic data models
│   │   │   ├── __init__.py
│   │   │   ├── workflow.py             # Workflow structure schemas
│   │   │   ├── analysis.py             # Analysis result schemas
│   │   │   ├── fix.py                  # Fix/optimization schemas
│   │   │   └── api.py                  # API request/response schemas
│   │   │
│   │   └── prompts/                    # AI system prompts
│   │       ├── diagnoser_system.md     # Diagnoser agent prompt
│   │       ├── fixer_system.md         # Fixer agent prompt
│   │       └── pr_writer_system.md     # PR writer agent prompt
│   │
│   ├── data/                           # Static data files
│   │   └── action_versions.json        # GitHub Actions version data
│   │
│   └── tests/                          # Test suite
│       ├── __init__.py
│       ├── test_static_analysis.py     # Static analysis tests
│       ├── test_orchestrator.py        # Orchestrator tests
│       └── fixtures/                   # Test fixtures
│           └── sample_workflow.yml     # Sample workflow for testing
│
├── frontend/                           # React + TypeScript frontend
│   ├── package.json                    # NPM dependencies and scripts
│   ├── vite.config.ts                  # Vite build configuration
│   ├── tsconfig.json                   # TypeScript configuration
│   ├── index.html                      # HTML entry point
│   ├── .env.example                    # Frontend environment variables
│   ├── Dockerfile                      # Frontend container configuration
│   │
│   ├── public/                         # Static assets
│   │   └── favicon.svg                 # App favicon
│   │
│   └── src/                            # Source code
│       ├── main.tsx                    # React entry point
│       ├── App.tsx                     # Root component
│       │
│       ├── api/                        # API client
│       │   ├── client.ts               # HTTP client (axios/fetch)
│       │   └── types.ts                # TypeScript API types
│       │
│       ├── components/                 # React components
│       │   ├── RepoInput.tsx           # Workflow input form
│       │   ├── DiagnosisCard.tsx       # Analysis results display
│       │   ├── DiffView.tsx            # Code diff viewer
│       │   ├── WorkflowGraph.tsx       # Workflow visualization
│       │   ├── PRPreview.tsx           # PR preview component
│       │   └── ProgressIndicator.tsx   # Loading/progress states
│       │
│       ├── pages/                      # Page components
│       │   ├── HomePage.tsx            # Landing/input page
│       │   └── ResultsPage.tsx         # Results dashboard (phases)
│       │
│       ├── hooks/                      # Custom React hooks
│       │   ├── useAnalysis.ts          # Analysis API hook
│       │   └── useDemoExamples.ts      # Demo data hook
│       │
│       ├── styles/                     # Stylesheets
│       │   └── globals.css             # Global styles (Carbon theme)
│       │
│       └── utils/                      # Utility functions
│           ├── yamlDiff.ts             # YAML diff utilities
│           └── formatTime.ts           # Time formatting helpers
│
├── examples/                           # Example workflows for demo
│   ├── express-api/                    # Express.js API example
│   │   └── .github/
│   │       └── workflows/
│   │           └── ci.yml              # Sample CI workflow
│   │
│   ├── flask-app/                      # Flask app example
│   │   └── .github/
│   │       └── workflows/
│   │           └── ci.yml              # Sample CI workflow
│   │
│   └── monorepo-sample/                # Monorepo example
│       └── .github/
│           └── workflows/
│               └── ci.yml              # Sample CI workflow
│
└── scripts/                            # Utility scripts
    ├── seed_demo_data.py               # Seed demo data for testing
    └── run_local.sh                    # Local development startup script
```

## Key Files Description

### Root Level
- **README.md**: Project overview, features, and quick start guide
- **.env.example**: Template for environment variables (API keys, URLs)
- **docker-compose.yml**: Orchestrates backend, frontend, PostgreSQL, and Redis
- **.gitignore**: Excludes node_modules, __pycache__, .env, etc.

### Backend (`/backend`)
- **app/main.py**: FastAPI app initialization, CORS, middleware, route registration
- **app/config.py**: Centralized configuration using Pydantic Settings
- **app/api/**: RESTful API endpoints for analyze, fix, PR creation
- **app/pipeline/**: Core processing logic (ingestion → analysis → optimization)
- **app/agents/**: AI agents using IBM Granite and Bob
- **app/github/**: GitHub API integration for workflows and PRs
- **app/schemas/**: Pydantic models for request/response validation
- **app/prompts/**: System prompts for AI agents (markdown files)

### Frontend (`/frontend`)
- **src/main.tsx**: React app entry point with React Query provider
- **src/App.tsx**: Root component with routing and layout
- **src/api/**: API client for backend communication
- **src/components/**: Reusable UI components (Carbon-based)
- **src/pages/**: Page-level components (HomePage, ResultsPage)
- **src/hooks/**: Custom React hooks for data fetching
- **src/styles/**: Global styles and Carbon theme customization

### Documentation (`/docs`)
- **architecture.md**: System architecture, data flow, tech stack
- **demo-script.md**: 3-minute demo walkthrough with talking points
- **prompts.md**: Detailed AI prompt documentation and examples
- **frontend-backend-integration-plan.md**: UX-to-API mapping and gaps

### Examples (`/examples`)
Sample workflows demonstrating common CI/CD patterns:
- Express.js API with sequential jobs
- Flask app with testing and deployment
- Monorepo with multiple workflows

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AI Models**: IBM Granite, IBM Bob
- **Orchestration**: IBM watsonx Orchestrate
- **Database**: PostgreSQL (optional)
- **Cache**: Redis (optional)
- **Testing**: pytest, pytest-asyncio

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: IBM Carbon Design System
- **State Management**: React Query (TanStack Query)
- **Visualization**: React Flow (workflow graphs)
- **Styling**: Tailwind CSS + Carbon tokens

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **API Documentation**: OpenAPI/Swagger (auto-generated)

## Development Workflow

### Backend Development
```bash
cd backend
poetry install
poetry shell
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Full Stack (Docker)
```bash
docker-compose up
```

## API Endpoints

### Health
- `GET /health` - Health check
- `GET /ready` - Readiness check

### Workflow Analysis
- `POST /api/analyze` - Analyze workflow
- `GET /api/analyze/{analysis_id}` - Get analysis results

### Optimization
- `POST /api/fix` - Generate optimized workflow
- `GET /api/fix/{fix_id}` - Get optimization results

### Pull Requests
- `POST /api/pr` - Create pull request
- `GET /api/pr/{repository}/{pr_number}` - Get PR status

## Environment Variables

### Backend (.env)
```
GRANITE_API_KEY=your_granite_api_key
BOB_API_KEY=your_bob_api_key
WATSONX_ORCHESTRATE_API_KEY=your_watsonx_key
GITHUB_TOKEN=your_github_token
DATABASE_URL=postgresql://user:pass@localhost:5432/processdoctor
REDIS_URL=redis://localhost:6379/0
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=ProcessDoctor
```

## Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Deployment

### Production Build
```bash
# Backend
cd backend
docker build -t processdoctor-backend .

# Frontend
cd frontend
npm run build
docker build -t processdoctor-frontend .
```

### Docker Compose (Production)
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Accessibility Compliance

All frontend components follow WCAG 2.1 Level AA standards:
- Keyboard navigation support
- Screen reader compatibility
- Color contrast compliance (4.5:1 for text)
- Focus indicators (3:1 contrast)
- Semantic HTML structure
- ARIA labels and live regions
- Motion reduction support

## License

MIT License (or as specified)

---

**Last Updated**: 2024-01-15
**Version**: 0.1.0
**Status**: MVP Development