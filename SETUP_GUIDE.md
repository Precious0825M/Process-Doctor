# Process Doctor - Setup & Next Steps Guide

## 🚀 Quick Setup (5 Minutes)

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- IBM Cloud account (for API keys)
- GitHub account (for token)

### Step 1: Clone and Install

```bash
# Navigate to project directory
cd Process-Doctor

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### Step 2: Obtain API Keys

#### IBM Granite API Key

1. Visit <https://watsonx.ai>
2. Sign in with IBM Cloud account
3. Navigate to API Keys section
4. Create new API key for Granite
5. Copy the key

#### IBM Bob API Key

1. Visit IBM Bob portal
2. Sign in with credentials
3. Generate API key
4. Copy the key

#### IBM watsonx Orchestrate API Key

1. Visit <https://watsonx.ibm.com/orchestrate>
2. Sign in with IBM Cloud account
3. Navigate to API credentials
4. Create new API key
5. Copy the key

#### GitHub Personal Access Token

1. Visit <https://github.com/settings/tokens>
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
4. Generate and copy token

### Step 3: Configure Environment

```bash
# From project root
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

Update these values in `.env`:

```env
GRANITE_API_KEY=your_granite_api_key_here
BOB_API_KEY=your_bob_api_key_here
WATSONX_ORCHESTRATE_API_KEY=your_watsonx_api_key_here
GITHUB_TOKEN=your_github_token_here
```

### Step 4: Run Development Servers

```bash
# Terminal 1 - Backend
cd backend
python -m app.main

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Step 5: Verify Setup

1. Open <http://localhost:8000/docs> - Should see API documentation
2. Open <http://localhost:5173> - Should see frontend
3. Test health endpoint: <http://localhost:8000/health>

## 📋 Implementation Checklist

### Phase 1: Environment Setup ⚠️ CRITICAL

- [ ] Obtain IBM Granite API key
- [ ] Obtain IBM Bob API key
- [ ] Obtain watsonx Orchestrate API key
- [ ] Generate GitHub token
- [ ] Create `.env` file
- [ ] Test API connectivity

### Phase 2: Backend Core ✅ COMPLETE

- [x] FastAPI main application
- [x] Health endpoints
- [x] Analyze endpoint
- [x] Fix endpoint
- [x] PR endpoint
- [x] CORS middleware
- [x] Error handling

### Phase 3: IBM Bob Integration (80%)

- [x] BobClient with real API calls
- [x] DiagnoserAgent structure
- [ ] JSON response parsing
- [ ] Structured bottleneck extraction
- [ ] Reasoning steps extraction

### Phase 4: IBM Granite Integration (80%)

- [x] GraniteClient with real API calls
- [x] FixerAgent structure
- [ ] YAML parsing and validation
- [ ] Unified diff generation
- [ ] PRWriterAgent enhancement

### Phase 5: watsonx Orchestrate ✅ COMPLETE

- [x] OrchestrateClient
- [x] Multi-step execution
- [x] Rollback capabilities
- [x] Status monitoring
- [x] Deployment steps

### Phase 6: GitHub Integration ✅ COMPLETE

- [x] GitHub client
- [x] PR creator
- [x] Branch management
- [x] PR status monitoring
- [x] Check runs integration

### Phase 7: Frontend API Client ✅ COMPLETE

- [x] TypeScript API client
- [x] Type definitions
- [x] Error handling
- [x] React Query helpers

### Phase 8: Frontend Sections (20%)

- [ ] InputSection - API integration
- [ ] DiagnoseSection - Results display
- [ ] PrescribeSection - Diff viewer
- [ ] TreatSection - Deployment status
- [ ] Real-time updates
- [ ] Loading states

### Phase 9: Testing (0%)

- [ ] Unit tests for agents
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] API tests
- [ ] Frontend tests

### Phase 10: Demo Preparation (0%)

- [ ] Demo data creation
- [ ] Demo script
- [ ] Backup video
- [ ] Presentation materials

## 🔧 Development Workflow

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
ruff check .
mypy .

# Frontend linting
cd frontend
npm run lint
```

### Building for Production

```bash
# Backend
cd backend
docker build -t process-doctor-backend .

# Frontend
cd frontend
npm run build
```

## 🐛 Troubleshooting

### Backend Issues

**Import errors (httpx, fastapi, etc.)**

```bash
cd backend
pip install -r requirements.txt
```

**API key errors**

- Verify `.env` file exists
- Check API keys are correct
- Ensure no extra spaces in keys

**Port already in use**

```bash
# Change port in .env
BACKEND_PORT=8001
```

### Frontend Issues

**TypeScript errors**

```bash
cd frontend
npm install
```

**API connection errors**

- Verify backend is running
- Check VITE_API_URL in `.env`
- Verify CORS settings

**Build errors**

```bash
cd frontend
rm -rf node_modules
npm install
```

## 📊 Testing the Implementation

### 1. Test Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "ProcessDoctor",
  "version": "0.1.0",
  "timestamp": "2026-05-02T17:00:00.000Z",
  "environment": "development"
}
```

### 2. Test Workflow Analysis

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_input": "name: CI\non: push\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v2",
    "source_type": "text"
  }'
```

### 3. Test Frontend

1. Open <http://localhost:5173>
2. Enter workflow text or GitHub URL
3. Click "Diagnose"
4. Review analysis results
5. Click "Prescribe" for optimization
6. Review and approve changes
7. Click "Treat" to deploy

## 🎯 Next Immediate Steps

### Priority 1: API Keys (BLOCKING)

**Time:** 1-2 hours  
**Action:** Follow Step 2 above to obtain all API keys

### Priority 2: Enhanced Parsing

**Time:** 4-6 hours  
**Files:**

- `backend/app/agents/diagnoser.py` - Add JSON extraction
- `backend/app/agents/fixer.py` - Add YAML parsing
- `backend/app/agents/pr_writer.py` - Enhance descriptions

**Implementation:**

```python
# Example: JSON extraction in diagnoser.py
import json
import re

def _parse_response(self, response: str) -> Dict[str, Any]:
    # Extract JSON from markdown code blocks
    json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))
    
    # Try direct JSON parsing
    try:
        return json.loads(response)
    except:
        # Fallback to structured extraction
        return self._extract_structured_data(response)
```

### Priority 3: Pipeline Components

**Time:** 6-8 hours  
**Files:**

- `backend/app/pipeline/ingestion.py`
- `backend/app/pipeline/static_analysis.py`
- `backend/app/pipeline/validation.py`

### Priority 4: Frontend Integration

**Time:** 12-16 hours  
**Files:**

- All files in `frontend/src/sections/`

**Implementation:**

```typescript
// Example: InputSection integration
import { api } from '../api/client';

const handleAnalyze = async () => {
  try {
    setLoading(true);
    const result = await api.analyze.create({
      workflow_input: workflowText,
      source_type: 'text'
    });
    setAnalysisResult(result);
  } catch (error) {
    setError(error.message);
  } finally {
    setLoading(false);
  }
};
```

## 📚 Additional Resources

- [Implementation Status](IMPLEMENTATION_STATUS.md)
- [Implementation Roadmap](docs/implementation-roadmap.md)
- [API Integration Guide](docs/api-integration-guide.md)
- [Architecture Documentation](docs/architecture.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## 🤝 Getting Help

If you encounter issues:

1. Check this guide's troubleshooting section
2. Review error logs in terminal
3. Verify API keys are correct
4. Check network connectivity
5. Review implementation status document

## 🎉 Success Indicators

You'll know setup is successful when:

- ✅ Backend starts without errors
- ✅ Frontend loads in browser
- ✅ Health endpoint returns 200
- ✅ API documentation accessible
- ✅ No CORS errors in browser console

---

**Made with Bob** 🤖
