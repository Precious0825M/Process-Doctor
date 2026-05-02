# ProcessDoctor Implementation Roadmap

## Overview

This roadmap outlines the complete implementation of ProcessDoctor with full IBM watsonx integration, following the architectural diagram requirements.

---

## Architecture Flow (As Required)

```
Developer Input (Text/Repo/Logs)
    ↓
IBM Bob: Workflow Parsing → Structured Workflow Graph (DAG + Metrics + Dependencies)
    ↓
IBM Granite LLM: Optimization Engine → Optimization Plan (Bottlenecks + Improvements)
    ↓
Action Planner: Convert Plan to Tasks → Generated Artifacts (CI/CD YAML, Scripts, IaC)
    ↓
IBM watsonx Orchestrate: Execution Engine → Tool Calls (GitHub API, CI/CD, Notifications)
    ↓
Observation Layer: Metrics + Results → CI Results + PR Feedback + Performance Metrics
    ↓
Re-Planning Loop: Re-optimize if needed ← (Closed loop optimization)
    ↑
Human Approval Gate (before execution)
```

---

## Phase 1: API Keys & Environment Setup

### Prerequisites

✅ **Required API Keys** (See `docs/api-integration-guide.md`):

1. IBM Granite API key (watsonx.ai)
2. IBM Bob API key
3. IBM watsonx Orchestrate API key
4. GitHub Personal Access Token

### Tasks

- [ ] Obtain all API keys from IBM Cloud
- [ ] Configure `.env` file with real credentials
- [ ] Test API connectivity for each service
- [ ] Set up error logging and monitoring

**Estimated Time**: 2-4 hours (depending on IBM account setup)

---

## Phase 2: IBM Bob Integration (Workflow Parsing)

### Objective

Implement IBM Bob to parse workflow descriptions and create structured workflow graphs.

### Files to Implement

1. **`backend/app/agents/llm_client.py`** - BobClient
2. **`backend/app/agents/diagnoser.py`** - DiagnoserAgent
3. **`backend/app/pipeline/ingestion.py`** - WorkflowIngestion

### Implementation Details

#### 2.1 Update BobClient (`llm_client.py`)

```python
class BobClient(LLMClient):
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Call IBM Bob API for workflow understanding"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "input": prompt,
            "parameters": {
                "temperature": 0.3,  # Lower for more deterministic parsing
                "max_new_tokens": 2000
            }
        }
        
        if system_prompt:
            payload["system_prompt"] = system_prompt
        
        try:
            response = await self.client.post(
                f"{self.api_url}/parse",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get("parsed_workflow", result.get("output", ""))
            
        except httpx.HTTPError as e:
            logger.error(f"Bob API error: {e}")
            raise
```

#### 2.2 Update DiagnoserAgent (`diagnoser.py`)

```python
async def diagnose(
    self,
    workflow_data: Dict[str, Any],
    static_results: Dict[str, Any]
) -> Dict[str, Any]:
    """Use IBM Bob to parse and diagnose workflow"""
    
    # Build structured prompt for Bob
    prompt = f"""
Analyze this workflow and provide structured output:

Workflow Content:
{workflow_data.get('content', '')}

Static Analysis:
{json.dumps(static_results, indent=2)}

Provide:
1. Workflow structure (jobs, dependencies, critical path)
2. Identified bottlenecks with severity
3. Performance metrics (current vs optimal duration)
4. Specific recommendations

Output as JSON.
"""
    
    # Call Bob API
    bob_response = await self.client.generate(
        prompt=prompt,
        system_prompt=self.system_prompt
    )
    
    # Parse Bob's structured response
    try:
        diagnosis = json.loads(bob_response)
    except json.JSONDecodeError:
        # Fallback: extract structured data from text
        diagnosis = self._extract_structured_data(bob_response)
    
    # Enhance with additional analysis
    diagnosis["reasoning_steps"] = self._extract_reasoning_steps(bob_response)
    
    return diagnosis
```

### Expected Output Format

```json
{
  "workflow_structure": {
    "name": "CI Pipeline",
    "jobs": [
      {
        "id": "lint",
        "name": "Lint Code",
        "dependencies": [],
        "estimated_duration": "2m",
        "parallelizable": true
      }
    ],
    "critical_path": ["lint", "test", "build", "deploy"]
  },
  "bottlenecks": [
    {
      "id": "bottleneck-1",
      "type": "sequential_execution",
      "severity": "high",
      "location": {"job": "test", "step": null},
      "description": "Tests run sequentially after lint completes",
      "impact": "Adds 15 minutes to total pipeline time",
      "recommendation": "Run lint and test in parallel"
    }
  ],
  "metrics": {
    "current_duration": "40m",
    "estimated_optimal": "15m",
    "efficiency_score": 45
  },
  "reasoning_steps": [
    {
      "step": 1,
      "action": "analyzing_structure",
      "reasoning": "Identified 4 jobs with sequential dependencies"
    }
  ]
}
```

### Tasks

- [ ] Implement BobClient with real API calls
- [ ] Update DiagnoserAgent to use Bob
- [ ] Add structured response parsing
- [ ] Add reasoning steps extraction
- [ ] Test with sample workflows
- [ ] Handle API errors gracefully

**Estimated Time**: 6-8 hours

---

## Phase 3: IBM Granite Integration (Optimization Engine)

### Objective

Use IBM Granite LLM to generate optimization recommendations and improved workflows.

### Files to Implement

1. **`backend/app/agents/llm_client.py`** - GraniteClient
2. **`backend/app/agents/fixer.py`** - FixerAgent
3. **`backend/app/agents/pr_writer.py`** - PRWriterAgent

### Implementation Details

#### 3.1 Update GraniteClient (`llm_client.py`)

```python
class GraniteClient(LLMClient):
    async def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Call IBM Granite API for optimization"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model_id": settings.granite_model,
            "input": prompt,
            "parameters": {
                "decoding_method": "greedy",
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "min_new_tokens": 1,
                "stop_sequences": ["</output>"]
            }
        }
        
        if system_prompt:
            payload["system_prompt"] = system_prompt
        
        try:
            response = await self.client.post(
                f"{self.api_url}/text/generation",
                headers=headers,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return result["results"][0]["generated_text"]
            
        except httpx.HTTPError as e:
            logger.error(f"Granite API error: {e}")
            raise
```

#### 3.2 Update FixerAgent (`fixer.py`)

```python
async def generate_fix(
    self,
    analysis_id: str,
    strategy: str = "balanced"
) -> Dict[str, Any]:
    """Generate optimized workflow using Granite"""
    
    # TODO: Retrieve analysis results from storage
    analysis = await self._get_analysis(analysis_id)
    
    # Build optimization prompt
    prompt = f"""
Given this workflow analysis, generate an optimized version:

Current Workflow:
{yaml.dump(analysis['workflow_structure'])}

Identified Bottlenecks:
{json.dumps(analysis['bottlenecks'], indent=2)}

Optimization Strategy: {strategy}

Generate:
1. Optimized workflow YAML
2. List of changes made with rationale
3. Expected performance improvements

Output format:
<optimized_workflow>
[YAML here]
</optimized_workflow>

<changes>
[JSON array of changes]
</changes>

<improvements>
[JSON object with metrics]
</improvements>
"""
    
    # Call Granite API
    granite_response = await self.client.generate(
        prompt=prompt,
        system_prompt=self.system_prompt,
        temperature=0.2  # Lower for more consistent code generation
    )
    
    # Parse response
    optimized_workflow = self._extract_yaml(granite_response)
    changes = self._extract_changes(granite_response)
    improvements = self._extract_improvements(granite_response)
    
    # Generate diff
    diff = self._generate_diff(
        analysis['workflow_structure'],
        optimized_workflow
    )
    
    return {
        "workflow": optimized_workflow,
        "yaml_formatted": yaml.dump(optimized_workflow, default_flow_style=False),
        "changes": changes,
        "time_saved": improvements.get("time_saved", "Unknown"),
        "efficiency_gain": improvements.get("efficiency_gain", "0%"),
        "diff": diff
    }
```

### Tasks

- [ ] Implement GraniteClient with real API calls
- [ ] Update FixerAgent to use Granite
- [ ] Add YAML parsing and validation
- [ ] Generate unified diffs
- [ ] Implement PRWriterAgent for descriptions
- [ ] Test optimization quality
- [ ] Add validation before returning

**Estimated Time**: 8-10 hours

---

## Phase 4: watsonx Orchestrate Integration (Execution Engine)

### Objective

Use IBM watsonx Orchestrate to execute multi-step workflows for PR creation and deployment.

### Files to Implement

1. **`backend/app/github/pr_creator.py`** - PRCreator with Orchestrate
2. **`backend/app/pipeline/orchestrator.py`** - Add orchestration logic

### Implementation Details

#### 4.1 Create Orchestrate Client

```python
# backend/app/orchestrate/client.py
class OrchestrationClient:
    def __init__(self):
        self.api_key = settings.watsonx_orchestrate_api_key
        self.api_url = settings.watsonx_orchestrate_url
        self.client = httpx.AsyncClient(timeout=300)
    
    async def execute_workflow(
        self,
        workflow_definition: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute workflow via watsonx Orchestrate"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        response = await self.client.post(
            f"{self.api_url}/workflows/execute",
            headers=headers,
            json=workflow_definition
        )
        
        response.raise_for_status()
        return response.json()
    
    async def get_execution_status(
        self,
        execution_id: str
    ) -> Dict[str, Any]:
        """Get workflow execution status"""
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        response = await self.client.get(
            f"{self.api_url}/workflows/executions/{execution_id}",
            headers=headers
        )
        
        response.raise_for_status()
        return response.json()
```

#### 4.2 Update PRCreator with Orchestrate

```python
async def create_pr(
    self,
    fix_id: str,
    repository: str,
    branch: str,
    title: str = None,
    description: str = None
) -> Dict[str, Any]:
    """Create PR using watsonx Orchestrate"""
    
    # Get fix data
    fix_data = await self._get_fix_data(fix_id)
    
    # Build orchestration workflow
    workflow = {
        "name": "create_workflow_optimization_pr",
        "description": "Create PR with optimized workflow",
        "steps": [
            {
                "id": "create_branch",
                "action": "github.create_branch",
                "parameters": {
                    "repository": repository,
                    "branch_name": branch,
                    "from_branch": "main"
                }
            },
            {
                "id": "commit_workflow",
                "action": "github.commit_file",
                "parameters": {
                    "repository": repository,
                    "branch": branch,
                    "file_path": ".github/workflows/ci.yml",
                    "content": fix_data["yaml_formatted"],
                    "message": "Optimize CI/CD workflow"
                },
                "depends_on": ["create_branch"]
            },
            {
                "id": "create_pr",
                "action": "github.create_pull_request",
                "parameters": {
                    "repository": repository,
                    "head": branch,
                    "base": "main",
                    "title": title or "Optimize CI/CD workflow for improved performance",
                    "body": description or fix_data.get("pr_description_preview", "")
                },
                "depends_on": ["commit_workflow"]
            },
            {
                "id": "notify_slack",
                "action": "slack.send_message",
                "parameters": {
                    "channel": "#deployments",
                    "message": f"PR created for workflow optimization: {repository}"
                },
                "depends_on": ["create_pr"],
                "optional": true
            }
        ],
        "on_failure": {
            "action": "slack.send_message",
            "parameters": {
                "channel": "#alerts",
                "message": "Failed to create workflow optimization PR"
            }
        }
    }
    
    # Execute via Orchestrate
    orchestrate_client = OrchestrationClient()
    execution = await orchestrate_client.execute_workflow(workflow)
    
    # Wait for completion (with timeout)
    execution_id = execution["execution_id"]
    status = await self._wait_for_completion(execution_id, timeout=300)
    
    if status["state"] == "completed":
        pr_result = status["steps"]["create_pr"]["output"]
        return {
            "pr_number": pr_result["number"],
            "pr_url": pr_result["html_url"],
            "branch": branch,
            "title": title
        }
    else:
        raise Exception(f"Orchestration failed: {status.get('error')}")
```

### Tasks

- [ ] Create OrchestrationClient
- [ ] Update PRCreator to use Orchestrate
- [ ] Implement workflow execution monitoring
- [ ] Add error handling and rollback
- [ ] Test multi-step workflows
- [ ] Add Slack/Jira notifications (optional)

**Estimated Time**: 10-12 hours

---

## Phase 5: Observation & Re-Planning Loop

### Objective

Monitor CI/CD execution results and feed back into optimization loop.

### Files to Implement

1. **`backend/app/github/runs.py`** - WorkflowRunsAnalyzer
2. **`backend/app/pipeline/orchestrator.py`** - Add feedback loop

### Implementation Details

#### 5.1 Implement Runs Analyzer

```python
async def analyze_runs(
    self,
    repository: str,
    workflow_id: str,
    pr_number: int = None
) -> Dict[str, Any]:
    """Analyze workflow run results"""
    
    repo = self.client.get_repository(repository)
    
    # Get recent runs
    if pr_number:
        # Get runs for specific PR
        runs = repo.get_workflow_runs(
            workflow_id=workflow_id,
            event="pull_request",
            branch=f"refs/pull/{pr_number}/merge"
        )
    else:
        runs = repo.get_workflow_runs(workflow_id=workflow_id)
    
    # Analyze performance
    run_data = []
    for run in runs[:10]:  # Last 10 runs
        run_data.append({
            "id": run.id,
            "status": run.status,
            "conclusion": run.conclusion,
            "duration": (run.updated_at - run.created_at).total_seconds(),
            "created_at": run.created_at.isoformat()
        })
    
    # Calculate metrics
    successful_runs = [r for r in run_data if r["conclusion"] == "success"]
    avg_duration = sum(r["duration"] for r in successful_runs) / len(successful_runs) if successful_runs else 0
    success_rate = len(successful_runs) / len(run_data) * 100 if run_data else 0
    
    return {
        "average_duration": f"{int(avg_duration / 60)}m",
        "success_rate": success_rate,
        "total_runs": len(run_data),
        "recent_runs": run_data,
        "improvement_detected": avg_duration < 900  # Less than 15 minutes
    }
```

#### 5.2 Add Re-Planning Loop

```python
async def re_optimize_if_needed(
    self,
    analysis_id: str,
    pr_number: int,
    repository: str
) -> Optional[Dict[str, Any]]:
    """Re-optimize workflow if performance doesn't meet expectations"""
    
    # Get actual performance metrics
    runs_analyzer = WorkflowRunsAnalyzer()
    actual_metrics = await runs_analyzer.analyze_runs(
        repository=repository,
        workflow_id="ci.yml",
        pr_number=pr_number
    )
    
    # Get expected metrics from original analysis
    original_analysis = await self._get_analysis(analysis_id)
    expected_duration = self._parse_duration(
        original_analysis["metrics"]["estimated_optimal"]
    )
    actual_duration = self._parse_duration(
        actual_metrics["average_duration"]
    )
    
    # Check if re-optimization needed
    if actual_duration > expected_duration * 1.2:  # 20% tolerance
        logger.info(f"Re-optimization needed: actual {actual_duration}s > expected {expected_duration}s")
        
        # Generate new optimization with more aggressive strategy
        new_fix = await self.generate_fix(
            analysis_id=analysis_id,
            optimization_strategy="aggressive"
        )
        
        return {
            "re_optimization_needed": True,
            "reason": "Actual performance below expectations",
            "new_fix_id": new_fix["fix_id"],
            "actual_duration": actual_metrics["average_duration"],
            "expected_duration": original_analysis["metrics"]["estimated_optimal"]
        }
    
    return {"re_optimization_needed": False}
```

### Tasks

- [ ] Implement WorkflowRunsAnalyzer
- [ ] Add performance metrics collection
- [ ] Implement re-planning logic
- [ ] Add feedback loop to orchestrator
- [ ] Test with real CI/CD runs
- [ ] Add alerting for performance issues

**Estimated Time**: 6-8 hours

---

## Phase 6: Human Approval Gate

### Objective

Add approval workflow before executing changes via Orchestrate.

### Files to Implement

1. **`backend/app/api/fix.py`** - Add approval endpoint
2. **`backend/app/schemas/api.py`** - Add approval schemas

### Implementation Details

#### 6.1 Add Approval Endpoint

```python
@router.post(
    "/fix/{fix_id}/approve",
    status_code=status.HTTP_200_OK,
    response_model=ApprovalResponse
)
async def approve_fix(
    fix_id: str,
    approval: ApprovalRequest
) -> ApprovalResponse:
    """Approve or reject a fix before deployment"""
    
    # Get fix data
    fix_data = await get_fix_data(fix_id)
    
    if approval.approved:
        # Mark as approved
        await mark_fix_approved(fix_id, approval.approver)
        
        # Optionally auto-create PR if requested
        if approval.auto_deploy:
            pr_result = await create_pr_via_orchestrate(
                fix_id=fix_id,
                repository=approval.repository,
                branch=approval.branch
            )
            
            return ApprovalResponse(
                fix_id=fix_id,
                approved=True,
                approver=approval.approver,
                pr_created=True,
                pr_url=pr_result["pr_url"]
            )
    else:
        # Mark as rejected
        await mark_fix_rejected(fix_id, approval.approver, approval.reason)
    
    return ApprovalResponse(
        fix_id=fix_id,
        approved=approval.approved,
        approver=approval.approver,
        pr_created=False
    )
```

### Tasks

- [ ] Add approval endpoints
- [ ] Create approval schemas
- [ ] Implement approval workflow
- [ ] Add approval UI in frontend
- [ ] Test approval flow
- [ ] Add audit logging

**Estimated Time**: 4-6 hours

---

## Phase 7: Frontend Integration

### Objective

Build React frontend that consumes backend APIs and displays results.

### Components to Build

1. **Input Phase**: RepoInput component
2. **Diagnose Phase**: DiagnosisCard, WorkflowGraph, ReasoningPanel
3. **Prescribe Phase**: DiffView, ApprovalModal
4. **Treat Phase**: DeploymentStatus, ResultsSummary

### Tasks

- [ ] Set up React + TypeScript + Vite
- [ ] Install IBM Carbon Design System
- [ ] Create API client with React Query
- [ ] Build phase components
- [ ] Implement accessibility features
- [ ] Add error handling
- [ ] Test with real backend

**Estimated Time**: 20-24 hours

---

## Phase 8: Testing & Optimization

### Tasks

- [ ] Unit tests for all modules
- [ ] Integration tests with real APIs
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Error handling improvements
- [ ] Documentation updates

**Estimated Time**: 12-16 hours

---

## Phase 9: Demo Preparation

### Tasks

- [ ] Prepare demo data
- [ ] Create demo script
- [ ] Test full workflow
- [ ] Prepare presentation
- [ ] Record backup video
- [ ] Practice demo timing (3 minutes)

**Estimated Time**: 6-8 hours

---

## Total Estimated Time

- **Phase 1**: 2-4 hours
- **Phase 2**: 6-8 hours
- **Phase 3**: 8-10 hours
- **Phase 4**: 10-12 hours
- **Phase 5**: 6-8 hours
- **Phase 6**: 4-6 hours
- **Phase 7**: 20-24 hours
- **Phase 8**: 12-16 hours
- **Phase 9**: 6-8 hours

**Total**: 74-96 hours (approximately 2-2.5 weeks of full-time work)

---

## Critical Path

1. ✅ Get API keys (blocking everything)
2. Implement Bob integration (blocking optimization)
3. Implement Granite integration (blocking PR creation)
4. Implement Orchestrate integration (blocking deployment)
5. Build frontend (can parallel with backend after APIs work)
6. Testing and demo prep

---

## Success Criteria

- [ ] All API integrations working with real IBM services
- [ ] Complete workflow: Input → Diagnose → Prescribe → Treat
- [ ] Human approval gate functional
- [ ] Re-planning loop operational
- [ ] Frontend accessible (WCAG 2.1 AA)
- [ ] Demo runs smoothly in under 3 minutes
- [ ] Documentation complete

---

**Next Immediate Steps**:

1. Obtain all API keys from IBM Cloud
2. Test API connectivity
3. Start Phase 2 (Bob integration)
