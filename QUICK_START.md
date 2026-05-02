# Process Doctor - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend (in new terminal)
cd frontend
npm install
```

### Step 2: Start the Backend

The backend is now configured with placeholder API keys and will start successfully:

```bash
cd backend
python run_dev.py
```

You should see:

```
============================================================
Starting ProcessDoctor Development Server
============================================================
Host: 0.0.0.0
Port: 8000
Debug: True
API Docs: http://0.0.0.0:8000/docs
============================================================

⚠️  WARNING: API keys not configured!
Please update backend/.env with your actual API keys
The server will start but API calls will fail without valid keys

INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Verify Backend is Running

Open your browser to:

- **API Documentation:** <http://localhost:8000/docs>
- **Health Check:** <http://localhost:8000/health>

You should see the Swagger UI with all endpoints documented.

### Step 4: Start the Frontend

```bash
cd frontend
npm run dev
```

Open <http://localhost:5173> in your browser.

## ✅ What Works Now

### Without API Keys (Development Mode)

- ✅ Backend server starts successfully
- ✅ All API endpoints are accessible
- ✅ API documentation available
- ✅ Health checks work
- ✅ Frontend loads
- ⚠️ Actual AI analysis will fail (needs real API keys)

### With API Keys (Full Functionality)

- ✅ Complete workflow analysis
- ✅ AI-powered optimization
- ✅ GitHub PR creation
- ✅ watsonx Orchestrate deployment

## 🔑 Adding Real API Keys

Edit `backend/.env` and replace placeholder values:

```env
# Replace these with your actual keys
GRANITE_API_KEY=your_actual_granite_key
BOB_API_KEY=your_actual_bob_key
WATSONX_ORCHESTRATE_API_KEY=your_actual_watsonx_key
GITHUB_TOKEN=your_actual_github_token
```

### Where to Get API Keys

1. **IBM Granite & Bob:** <https://watsonx.ai> → API Keys
2. **watsonx Orchestrate:** <https://watsonx.ibm.com/orchestrate> → Credentials
3. **GitHub Token:** <https://github.com/settings/tokens>
   - Scopes needed: `repo`, `workflow`

## 🧪 Testing the API

### Test Health Endpoint

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

### Test Analysis Endpoint (Will fail without API keys)

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_input": "name: CI\non: push\njobs:\n  test:\n    runs-on: ubuntu-latest",
    "source_type": "text"
  }'
```

## 📁 Project Structure

```
Process-Doctor/
├── backend/
│   ├── .env                    # ✅ Created with placeholders
│   ├── run_dev.py             # ✅ Development server runner
│   ├── app/
│   │   ├── main.py            # ✅ FastAPI application
│   │   ├── config.py          # ✅ Configuration (API keys optional)
│   │   ├── api/               # ✅ All endpoints implemented
│   │   ├── agents/            # ✅ LLM clients implemented
│   │   ├── orchestrate/       # ✅ watsonx Orchestrate client
│   │   └── github/            # ✅ GitHub integration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.ts      # ✅ Complete API client
│   │   ├── sections/          # ⚠️ Need API integration
│   │   └── components/
│   └── package.json
├── IMPLEMENTATION_STATUS.md    # ✅ Detailed progress
├── SETUP_GUIDE.md             # ✅ Comprehensive setup
└── QUICK_START.md             # ✅ This file
```

## 🎯 Current Status

**Overall Progress: ~60% Complete**

### ✅ Fully Implemented

- Backend core infrastructure
- All API endpoints
- LLM client integrations
- GitHub integration
- watsonx Orchestrate client
- Frontend API client

### ⚠️ Needs Work

- Agent response parsing (JSON/YAML extraction)
- Frontend section integration
- Pipeline components
- Testing suite
- Demo preparation

## 🔧 Troubleshooting

### "Module not found" errors

```bash
cd backend
pip install -r requirements.txt
```

### Port already in use

Edit `backend/.env`:

```env
BACKEND_PORT=8001
```

### Frontend won't start

```bash
cd frontend
rm -rf node_modules
npm install
```

### API calls fail

- Check backend is running on port 8000
- Verify `.env` file exists in backend/
- For full functionality, add real API keys

## 📚 Next Steps

1. **Immediate:** Test that both servers start
2. **Short-term:** Add real API keys for full functionality
3. **Medium-term:** Complete frontend integration
4. **Long-term:** Add tests and prepare demo

## 📖 Documentation

- [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) - Detailed progress tracking
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Comprehensive setup instructions
- [docs/implementation-roadmap.md](docs/implementation-roadmap.md) - Full roadmap
- [docs/api-integration-guide.md](docs/api-integration-guide.md) - API integration details

## 🆘 Need Help?

1. Check error messages in terminal
2. Verify all dependencies installed
3. Ensure `.env` file exists
4. Review documentation files
5. Check that ports 8000 and 5173 are available

---

**Made with Bob** 🤖
