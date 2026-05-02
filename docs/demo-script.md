# ProcessDoctor Demo Script

## Demo Duration: 3 Minutes

## Setup (Before Demo)

- [ ] Backend running on <http://localhost:8000>
- [ ] Frontend running on <http://localhost:5173>
- [ ] Sample workflows loaded
- [ ] GitHub token configured (if showing PR creation)

---

## Demo Flow

### 1. Introduction (30 seconds)

**Script:**
> "ProcessDoctor is an AI-powered workflow optimization system that helps developers analyze, optimize, and automate their CI/CD pipelines in minutes."

**Show:**

- Landing page with tagline
- Quick overview of the 3-step process: Diagnose → Prescribe → Treat

---

### 2. Input Workflow (30 seconds)

**Script:**
> "Let's start with a real-world scenario. We have a CI pipeline that's taking 40 minutes to run, with sequential jobs and manual approvals."

**Action:**

- Paste sample workflow description OR
- Connect to sample GitHub repository
- Click "Analyze Workflow"

**Example Input:**

```
Our CI pipeline for a Node.js API takes 40 minutes:
- Runs tests sequentially
- Builds Docker image after tests complete
- Requires manual approval for deployment
- No caching configured
- Runs on every commit
```

---

### 3. Analysis Results (45 seconds)

**Script:**
> "ProcessDoctor uses IBM Bob to understand the workflow structure and IBM Granite to identify bottlenecks."

**Show:**

- Workflow visualization graph
- Identified bottlenecks (highlighted in red):
  - Sequential execution
  - No caching
  - Manual approval delays
  - Redundant steps
- Performance metrics:
  - Current duration: 40 minutes
  - Estimated optimized: 15 minutes
  - Efficiency gain: 62.5%

---

### 4. Optimization Recommendations (45 seconds)

**Script:**
> "Here are the AI-generated optimizations. Notice how it parallelizes jobs, adds caching, and automates approvals."

**Show:**

- Side-by-side comparison:
  - **Before**: Sequential workflow diagram
  - **After**: Parallel workflow diagram
- Key improvements highlighted:
  - ✅ Parallel test execution
  - ✅ Dependency caching
  - ✅ Automated approvals for non-prod
  - ✅ Conditional job execution
- Generated GitHub Actions YAML preview

---

### 5. Deployment (30 seconds)

**Script:**
> "With one click, ProcessDoctor can create a pull request with all the improvements, ready for review and deployment."

**Action:**

- Click "Create Pull Request"
- Show PR preview with:
  - Optimized workflow file
  - Detailed description of changes
  - Expected performance improvements

**Show:**

- PR creation confirmation
- Link to GitHub PR (if live demo)
- Summary of changes

---

## Key Talking Points

### Innovation

- **End-to-end automation**: From analysis to deployment
- **AI-powered insights**: Not just rule-based, but intelligent optimization
- **Production-ready**: Generates actual deployable code

### Business Value

- **Time savings**: 50-70% reduction in pipeline duration
- **Developer productivity**: Less time debugging, more time building
- **Cost reduction**: Fewer compute resources, faster feedback

### Technical Highlights

- **IBM Bob**: Workflow understanding and parsing
- **IBM Granite**: Intelligent optimization recommendations
- **IBM watsonx Orchestrate**: Automated deployment and execution

---

## Backup Scenarios

### If Live Demo Fails

- Use pre-recorded video
- Show static screenshots
- Walk through code examples

### If Questions About Specific Features

- **"Can it handle complex monorepos?"**
  - Yes, show example with multiple workflows
- **"Does it work with other CI/CD systems?"**
  - Currently GitHub Actions, extensible to others
- **"How does it ensure security?"**
  - No code execution, only analysis and generation
  - User reviews all changes before deployment

---

## Demo Variations

### Quick Version (1 minute)

1. Show problem (slow pipeline)
2. Show solution (optimized pipeline)
3. Show results (62% faster)

### Extended Version (5 minutes)

- Include code walkthrough
- Show multiple workflow examples
- Demonstrate customization options
- Show metrics dashboard

---

## Post-Demo Q&A Prep

**Common Questions:**

1. **"How accurate are the optimizations?"**
   - Based on industry best practices and AI analysis
   - User reviews before deployment
   - Continuous learning from feedback

2. **"Can it optimize existing workflows?"**
   - Yes, analyzes current workflows and suggests improvements
   - Preserves critical logic while optimizing structure

3. **"What about testing the optimized workflows?"**
   - Generates test scenarios
   - Recommends gradual rollout
   - Includes rollback procedures

4. **"Pricing/Licensing?"**
   - Currently proof-of-concept
   - Future: SaaS model or enterprise licensing

---

## Success Metrics to Highlight

- ⏱️ **< 2 minutes** from input to optimization
- 📈 **50-70%** workflow efficiency improvement
- 🤖 **100%** automated artifact generation
- ✅ **Production-ready** code output

---

## Demo Environment URLs

- **Frontend**: <http://localhost:5173>
- **Backend API**: <http://localhost:8000>
- **API Docs**: <http://localhost:8000/docs>
- **Health Check**: <http://localhost:8000/health>

---

## Troubleshooting

### Backend Not Responding

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend Not Loading

```bash
cd frontend
npm run dev
```

### API Keys Not Working

- Check `.env` file
- Verify API key validity
- Check network connectivity

---

## Demo Checklist

**Before Starting:**

- [ ] All services running
- [ ] Sample data loaded
- [ ] Browser tabs prepared
- [ ] Backup slides ready
- [ ] Timer set for 3 minutes

**During Demo:**

- [ ] Speak clearly and confidently
- [ ] Highlight key innovations
- [ ] Show real-world value
- [ ] Keep to time limit

**After Demo:**

- [ ] Answer questions
- [ ] Share GitHub repo link
- [ ] Collect feedback
- [ ] Follow up on interest
