# ProcessDoctor API Integration Guide

## Required API Keys & Setup

This guide covers obtaining and configuring all required API keys for full ProcessDoctor implementation.

---

## Architecture Overview

```
Developer Input
    ↓
IBM Bob (Workflow Parsing)
    ↓
IBM Granite LLM (Optimization)
    ↓
Action Planner (Generate Artifacts)
    ↓
IBM watsonx Orchestrate (Execution)
    ↓
GitHub API / CI/CD Systems
    ↓
Observation & Re-planning Loop
```

---

## Required API Keys

### 1. IBM Granite LLM API

**Purpose**: AI-powered optimization engine for workflow analysis

**How to Obtain**:

1. Visit IBM watsonx.ai platform: <https://www.ibm.com/watsonx>
2. Sign up for IBM Cloud account (if not already registered)
3. Navigate to watsonx.ai service
4. Create a new project
5. Generate API key from IAM (Identity and Access Management)
6. Note your API endpoint URL

**Configuration**:

```bash
GRANITE_API_KEY=your_granite_api_key_here
GRANITE_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1
GRANITE_MODEL=ibm/granite-13b-chat-v2
```

**API Documentation**: <https://cloud.ibm.com/apidocs/watsonx-ai>

---

### 2. IBM Bob API

**Purpose**: Workflow parsing and understanding

**How to Obtain**:

1. Access IBM Bob platform (internal IBM tool or via IBM Cloud)
2. Register for Bob API access
3. Generate API credentials
4. Note your Bob API endpoint

**Configuration**:

```bash
BOB_API_KEY=your_bob_api_key_here
BOB_API_URL=https://api.bob.ibm.com/v1
```

**Note**: Bob may be accessed through IBM Cloud Functions or as a standalone service. Check with IBM for current access methods.

---

### 3. IBM watsonx Orchestrate API

**Purpose**: Execution engine for automated workflow deployment

**How to Obtain**:

1. Visit IBM watsonx Orchestrate: <https://www.ibm.com/products/watsonx-orchestrate>
2. Sign up or log in to IBM Cloud
3. Create watsonx Orchestrate instance
4. Generate API key from service credentials
5. Note your orchestration endpoint

**Configuration**:

```bash
WATSONX_ORCHESTRATE_API_KEY=your_watsonx_orchestrate_key_here
WATSONX_ORCHESTRATE_URL=https://api.watsonx.ibm.com/orchestrate/v1
```

**API Documentation**: <https://cloud.ibm.com/docs/watsonx-orchestrate>

---

### 4. GitHub Personal Access Token

**Purpose**: Create PRs, access workflows, trigger CI/CD

**How to Obtain**:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (full control of private repositories)
   - `workflow` (update GitHub Action workflows)
   - `read:org` (read org and team membership)
4. Generate and copy token immediately (shown only once)

**Configuration**:

```bash
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_API_URL=https://api.github.com
```

**Scopes Required**:

- ✅ `repo` - Access repositories
- ✅ `workflow` - Update workflows
- ✅ `read:org` - Read organization data

---

## Environment Setup

### 1. Create `.env` File

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### 2. Fill in API Keys

Edit `.env` with your actual keys:

```bash
# IBM Granite API
GRANITE_API_KEY=your_actual_granite_key
GRANITE_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1
GRANITE_MODEL=ibm/granite-13b-chat-v2

# IBM Bob API
BOB_API_KEY=your_actual_bob_key
BOB_API_URL=https://api.bob.ibm.com/v1

# IBM watsonx Orchestrate
WATSONX_ORCHESTRATE_API_KEY=your_actual_watsonx_key
WATSONX_ORCHESTRATE_URL=https://api.watsonx.ibm.com/orchestrate/v1

# GitHub
GITHUB_TOKEN=ghp_your_actual_github_token
GITHUB_API_URL=https://api.github.com

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
DEBUG=true
LOG_LEVEL=info

# Frontend Configuration
VITE_API_URL=http://localhost:8000

# Database (Optional)
DATABASE_URL=postgresql://user:password@localhost:5432/processdoctor
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Security
SECRET_KEY=your_secret_key_change_in_production
```

### 3. Verify Configuration

Test your API keys:

```bash
cd backend
python -c "from app.config import settings; print('Config loaded successfully')"
```

---

## Implementation Requirements

### Backend Implementation Checklist

#### 1. IBM Granite Integration (`app/agents/llm_client.py`)

```python
class GraniteClient(LLMClient):
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Call IBM Granite API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model_id": settings.granite_model,
            "input": prompt,
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 2000
            }
        }
        
        if system_prompt:
            payload["system_prompt"] = system_prompt
        
        response = await self.client.post(
            f"{self.api_url}/text/generation",
            headers=headers,
            json=payload
        )
        
        response.raise_for_status()
        return response.json()["results"][0]["generated_text"]
```

#### 2. IBM Bob Integration (`app/agents/diagnoser.py`)

```python
class DiagnoserAgent:
    async def diagnose(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use IBM Bob to parse and understand workflow"""
        
        # Call Bob API for workflow understanding
        bob_response = await self.client.generate(
            prompt=self._build_analysis_prompt(workflow_data),
            system_prompt=self.system_prompt
        )
        
        # Parse Bob's structured output
        diagnosis = self._parse_bob_response(bob_response)
        
        return diagnosis
```

#### 3. watsonx Orchestrate Integration (`app/github/pr_creator.py`)

```python
class PRCreator:
    async def create_pr_via_orchestrate(
        self,
        fix_data: Dict[str, Any],
        repository: str
    ) -> Dict[str, Any]:
        """Use watsonx Orchestrate to create PR"""
        
        # Build orchestration workflow
        workflow = {
            "name": "create_workflow_optimization_pr",
            "steps": [
                {
                    "action": "github.create_branch",
                    "params": {
                        "repository": repository,
                        "branch": "optimization/workflow-improvements"
                    }
                },
                {
                    "action": "github.commit_file",
                    "params": {
                        "repository": repository,
                        "path": ".github/workflows/ci.yml",
                        "content": fix_data["optimized_workflow"]
                    }
                },
                {
                    "action": "github.create_pr",
                    "params": {
                        "repository": repository,
                        "title": "Optimize CI/CD workflow",
                        "body": fix_data["pr_description"]
                    }
                }
            ]
        }
        
        # Execute via watsonx Orchestrate
        response = await self._execute_orchestration(workflow)
        return response
```

---

## API Integration Architecture

### Layer 1: Input Processing

**File**: `app/pipeline/ingestion.py`

- Parse text descriptions
- Fetch GitHub workflows
- Normalize input format

### Layer 2: IBM Bob - Workflow Understanding

**File**: `app/agents/diagnoser.py`

- Call Bob API with workflow data
- Parse structured workflow graph
- Identify dependencies and critical path

### Layer 3: IBM Granite - Optimization

**File**: `app/agents/fixer.py`

- Call Granite API with analysis results
- Generate optimization recommendations
- Create optimized workflow configuration

### Layer 4: Action Planning

**File**: `app/pipeline/orchestrator.py`

- Convert optimization plan to executable tasks
- Generate CI/CD YAML
- Prepare deployment artifacts

### Layer 5: watsonx Orchestrate - Execution

**File**: `app/github/pr_creator.py`

- Execute multi-step workflow via Orchestrate
- Create GitHub branches
- Commit changes
- Create pull requests
- Send notifications

### Layer 6: Observation & Feedback

**File**: `app/github/runs.py`

- Monitor CI/CD execution
- Collect performance metrics
- Feed back to re-planning loop

---

## API Rate Limits & Quotas

### IBM Granite

- **Rate Limit**: Varies by plan (typically 100 requests/minute)
- **Token Limit**: 4096 tokens per request
- **Recommendation**: Implement request queuing and retry logic

### IBM Bob

- **Rate Limit**: Check IBM documentation
- **Recommendation**: Cache parsed workflows

### watsonx Orchestrate

- **Rate Limit**: Varies by plan
- **Recommendation**: Batch operations where possible

### GitHub API

- **Rate Limit**: 5000 requests/hour (authenticated)
- **Recommendation**: Use conditional requests and ETags

---

## Error Handling

### API Key Validation

```python
async def validate_api_keys():
    """Validate all API keys on startup"""
    errors = []
    
    # Test Granite
    try:
        granite = GraniteClient()
        await granite.generate("test", max_tokens=10)
    except Exception as e:
        errors.append(f"Granite API: {e}")
    
    # Test Bob
    try:
        bob = BobClient()
        await bob.generate("test", max_tokens=10)
    except Exception as e:
        errors.append(f"Bob API: {e}")
    
    # Test GitHub
    try:
        github = GitHubClient()
        github.client.get_user()
    except Exception as e:
        errors.append(f"GitHub API: {e}")
    
    if errors:
        raise ValueError(f"API validation failed: {', '.join(errors)}")
```

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def call_api_with_retry(client, prompt):
    """Retry API calls with exponential backoff"""
    return await client.generate(prompt)
```

---

## Security Best Practices

### 1. Never Commit API Keys

- ✅ Use `.env` files (in `.gitignore`)
- ✅ Use environment variables in production
- ✅ Use secret management services (AWS Secrets Manager, Azure Key Vault)

### 2. Rotate Keys Regularly

- Set calendar reminders to rotate keys every 90 days
- Use different keys for dev/staging/production

### 3. Principle of Least Privilege

- Only grant necessary scopes
- Use read-only keys where possible

### 4. Monitor API Usage

- Set up alerts for unusual activity
- Track API costs and usage patterns

---

## Testing with Real APIs

### Unit Tests with API Mocking

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_granite_integration():
    with patch('app.agents.llm_client.httpx.AsyncClient') as mock_client:
        mock_client.return_value.post = AsyncMock(
            return_value=MockResponse({"results": [{"generated_text": "test"}]})
        )
        
        client = GraniteClient()
        result = await client.generate("test prompt")
        
        assert result == "test"
```

### Integration Tests (Requires Real Keys)

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_workflow_analysis():
    """Test with real API keys (slow, costs money)"""
    orchestrator = WorkflowOrchestrator()
    
    result = await orchestrator.analyze_workflow(
        workflow_input="sample workflow",
        source_type="text",
        analysis_id="test-123"
    )
    
    assert "bottlenecks" in result
    assert "recommendations" in result
```

Run integration tests:

```bash
pytest -m integration  # Only run integration tests
pytest -m "not integration"  # Skip integration tests
```

---

## Cost Estimation

### IBM watsonx.ai (Granite)

- **Pricing**: ~$0.002 per 1K tokens
- **Estimated Usage**: 50K tokens per workflow analysis
- **Cost per Analysis**: ~$0.10

### IBM watsonx Orchestrate

- **Pricing**: Varies by plan (typically per execution)
- **Estimated Cost**: $0.05 - $0.20 per workflow deployment

### GitHub API

- **Free**: Up to 5000 requests/hour
- **Cost**: $0 (within limits)

### Total Estimated Cost

- **Per Workflow Optimization**: $0.15 - $0.30
- **100 Workflows**: $15 - $30
- **Demo/Testing**: Budget $50-100 for development

---

## Troubleshooting

### "Invalid API Key" Error

1. Verify key is correctly copied (no extra spaces)
2. Check key hasn't expired
3. Verify correct API endpoint URL
4. Test key with curl:

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
     https://api.endpoint.com/health
```

### "Rate Limit Exceeded"

1. Implement exponential backoff
2. Add request queuing
3. Cache responses where possible
4. Upgrade API plan if needed

### "Connection Timeout"

1. Check network connectivity
2. Verify firewall rules
3. Increase timeout settings
4. Use retry logic

---

## Next Steps

1. **Obtain API Keys**: Follow guides above to get all required keys
2. **Configure Environment**: Set up `.env` file with real keys
3. **Implement API Clients**: Complete the TODO sections in LLM clients
4. **Test Integration**: Run integration tests with real APIs
5. **Monitor Usage**: Set up logging and monitoring for API calls
6. **Optimize Costs**: Implement caching and request batching

---

## Support Resources

- **IBM watsonx.ai**: <https://cloud.ibm.com/docs/watsonx>
- **IBM Bob**: Contact IBM support or check internal documentation
- **watsonx Orchestrate**: <https://www.ibm.com/docs/en/watsonx-orchestrate>
- **GitHub API**: <https://docs.github.com/en/rest>

---

**Last Updated**: 2024-01-15
**Status**: Ready for Implementation
