# ProcessDoctor Frontend-Backend Integration Plan

## Overview

This document maps the UX flow (Input → Diagnose → Prescribe → Treat) to existing backend APIs, identifies required data fields, component needs, and gaps between backend logic and UX deliverables.

---

## UX Flow Phases

### Phase 1: INPUT

**User Action**: Enter workflow description or connect GitHub repo

#### Backend API Mapping

- **Endpoint**: `POST /api/analyze`
- **Request Schema**: `AnalyzeRequest`

  ```typescript
  {
    workflow_input: string;  // Text description or GitHub URL
    source_type: "text" | "github" | "file";
  }
  ```

#### Frontend Components Needed

1. **RepoInput Component**
   - Text area for workflow description
   - GitHub URL input field
   - File upload option
   - Source type selector (radio buttons)
   - Submit button with loading state
   - Validation feedback

2. **Accessibility Requirements**
   - All inputs have visible, persistent labels
   - Helper text for each input type
   - Error messages associated via `aria-describedby`
   - Submit button has loading state announced to screen readers
   - Form validation errors announced via `aria-live="polite"`

#### Data Flow

```
User Input → RepoInput Component → POST /api/analyze → Backend Processing
```

#### Gaps Identified

- ✅ Backend supports all three input types
- ⚠️ Need file upload handling in backend (currently stub)
- ⚠️ Need GitHub OAuth flow for private repos (future enhancement)

---

### Phase 2: DIAGNOSE

**User Action**: View workflow analysis and identified bottlenecks

#### Backend API Response

- **Endpoint**: `POST /api/analyze` (returns immediately)
- **Response Schema**: `AnalyzeResponse`

  ```typescript
  {
    analysis_id: string;
    status: "completed" | "processing" | "failed";
    workflow_structure: {
      name: string;
      triggers: string[];
      jobs: Array<{
        name: string;
        steps: string[];
        dependencies: string[];
        estimated_duration: string;
        parallelizable: boolean;
      }>;
      overall_structure: "sequential" | "parallel" | "mixed";
      critical_path: string[];
    };
    bottlenecks: Array<{
      type: string;
      severity: "critical" | "high" | "medium" | "low";
      description: string;
      location: string;
      impact: string;
    }>;
    metrics: {
      current_duration: string;
      estimated_optimal: string;
      efficiency_score: number; // 0-100
      total_jobs: number;
      total_steps: number;
    };
    recommendations: string[];
    estimated_improvement: string; // e.g., "62%"
  }
  ```

#### Frontend Components Needed

1. **DiagnosisCard Component**
   - Display bottlenecks with severity indicators
   - Show metrics in accessible format
   - List recommendations
   - Visual severity badges (color + icon + text)

2. **WorkflowGraph Component**
   - Visual representation of workflow structure
   - Highlight bottlenecks in red
   - Show critical path
   - Keyboard navigable nodes
   - `role="img"` with descriptive `aria-label`

3. **ProgressIndicator Component**
   - Show current phase (Diagnose)
   - Use `aria-current="step"` on active phase
   - Carbon Tabs for phase navigation

4. **Accessibility Requirements**
   - Bottlenecks: red border + warning icon + "Bottleneck" label (not color alone)
   - Severity levels announced: `<span class="pd-sr-only">Severity: </span>critical`
   - Workflow graph has descriptive `aria-label`: "Workflow diagram showing 4 jobs with 2 bottlenecks identified"
   - Metrics table uses proper `<table>` with `<th>` headers
   - Recommendations list uses semantic `<ul>`

#### Data Flow

```
Backend Response → DiagnosisCard + WorkflowGraph → User Reviews Analysis
```

#### Gaps Identified

- ✅ Backend provides all required data
- ⚠️ Need to enhance `workflow_structure` with node positions for graph layout
- ⚠️ Need to add `reasoning_steps` array for Bob's "thinking" process (for reasoning panel)
- ⚠️ Backend should return `bottleneck_locations` with specific job/step references

#### Required Backend Enhancement

Add to `AnalyzeResponse`:

```typescript
reasoning_steps: Array<{
  step: number;
  timestamp: string;
  action: string;
  reasoning: string;
}>;
```

---

### Phase 3: PRESCRIBE

**User Action**: Review optimized workflow and approve changes

#### Backend API Mapping

- **Endpoint**: `POST /api/fix`
- **Request Schema**: `FixRequest`

  ```typescript
  {
    analysis_id: string;
    optimization_strategy: "aggressive" | "balanced" | "conservative";
  }
  ```

- **Response Schema**: `FixResponse`

  ```typescript
  {
    fix_id: string;
    analysis_id: string;
    status: "completed" | "processing" | "failed";
    optimized_workflow: object; // YAML as object
    changes: Array<{
      type: string;
      description: string;
      before: string;
      after: string;
      impact: string;
    }>;
    improvements: {
      time_saved: string;
      efficiency_gain: string;
      optimizations_applied: number;
      cost_reduction: string;
    };
    diff: string; // Unified diff format
  }
  ```

#### Frontend Components Needed

1. **DiffView Component**
   - Side-by-side or unified diff view
   - Syntax highlighting for YAML
   - Line numbers
   - Keyboard navigable
   - Carbon CodeSnippet for copy functionality

2. **PRPreview Component**
   - Show generated PR description
   - List of changes with impact
   - Improvements summary
   - Approval gate (modal)

3. **Approval Modal**
   - Review changes before deployment
   - Confirm/Cancel buttons
   - Focus trap while open
   - Escape key closes
   - Focus returns to trigger button on close
   - Carbon Modal component

4. **Accessibility Requirements**
   - Code diff uses Carbon's CodeSnippet (keyboard accessible)
   - Copy button is keyboard reachable with `aria-label="Copy code"`
   - Changes list uses semantic `<ul>` with proper headings
   - Approval modal:
     - Focus traps inside modal
     - Escape key closes
     - Focus returns to trigger button
     - Modal title is `<h2>` (proper heading hierarchy)
   - Success indicators: green + checkmark icon + "Optimized" label

#### Data Flow

```
User Selects Strategy → POST /api/fix → Backend Generates Fix → 
DiffView + PRPreview → User Approves → POST /api/pr
```

#### Gaps Identified

- ✅ Backend provides optimized workflow and diff
- ⚠️ Need to add `yaml_formatted` string to response for display
- ⚠️ Need to add `pr_description` preview to response
- ⚠️ Backend should validate workflow before returning

#### Required Backend Enhancement

Add to `FixResponse`:

```typescript
yaml_formatted: string; // Pretty-printed YAML for display
pr_description_preview: string; // Generated PR description
validation_status: {
  valid: boolean;
  errors: string[];
  warnings: string[];
};
```

---

### Phase 4: TREAT

**User Action**: Deploy optimized workflow via PR

#### Backend API Mapping

- **Endpoint**: `POST /api/pr`
- **Request Schema**: `PRRequest`

  ```typescript
  {
    fix_id: string;
    repository: string; // "owner/repo"
    branch: string; // Default: "optimization/workflow-improvements"
    title?: string;
    description?: string;
  }
  ```

- **Response Schema**: `PRResponse`

  ```typescript
  {
    pr_number: number;
    pr_url: string;
    branch: string;
    status: "created" | "failed";
    message: string;
  }
  ```

#### Frontend Components Needed

1. **DeploymentStatus Component**
   - Show PR creation progress
   - Display PR link when created
   - Success/error states
   - Next steps guidance

2. **ResultsSummary Component**
   - Before/after comparison
   - Time saved
   - Efficiency gain
   - Link to GitHub PR

3. **Accessibility Requirements**
   - Success state: green + checkmark icon + "PR Created Successfully" text
   - PR link is real `<a href>` with descriptive text: "View Pull Request #123 on GitHub"
   - Error states: red + error icon + descriptive error message
   - Loading state announced via `aria-live="polite"`
   - Results summary uses proper heading hierarchy

#### Data Flow

```
User Confirms → POST /api/pr → GitHub PR Created → 
DeploymentStatus → ResultsSummary → User Views PR
```

#### Gaps Identified

- ✅ Backend creates PR and returns URL
- ⚠️ Need to add deployment status polling endpoint
- ⚠️ Need to add PR status check endpoint (already exists: `GET /api/pr/{repository}/{pr_number}`)
- ⚠️ Need to handle GitHub authentication errors gracefully

---

## Cross-Cutting Concerns

### 1. Reasoning Panel (Bob's "Thinking")

**Purpose**: Show AI reasoning steps in real-time

#### Required Backend Enhancement

Add WebSocket or Server-Sent Events endpoint:

- **Endpoint**: `GET /api/analyze/{analysis_id}/stream` (SSE)
- **Response**: Stream of reasoning steps

  ```typescript
  {
    step: number;
    timestamp: string;
    action: "analyzing_structure" | "identifying_bottlenecks" | "calculating_metrics";
    reasoning: string;
    progress: number; // 0-100
  }
  ```

#### Frontend Component

- **ReasoningPanel Component**
  - Display reasoning steps as they arrive
  - Use `aria-live="polite"` for screen reader announcements
  - Auto-scroll to latest step
  - Collapsible/expandable

#### Accessibility

- `aria-live="polite"` so new steps are announced without interrupting
- Each step has timestamp for context
- Visual progress indicator with text alternative

---

### 2. Phase Navigation

**Component**: Stage Indicator / Phase Tabs

#### Implementation

- Use Carbon Tabs component
- Phases: Input → Diagnose → Prescribe → Treat
- Active phase uses `aria-current="step"`
- Keyboard navigation: arrow keys to move between tabs
- Disabled tabs for incomplete phases

#### Accessibility

- Proper heading hierarchy: `<h1>` for app title, `<h2>` for phase titles
- Tab panel content has `role="tabpanel"`
- Active tab has `aria-selected="true"`

---

### 3. Error Handling

#### Backend Error Responses

All endpoints should return consistent error format:

```typescript
{
  error: string;
  detail: string;
  status_code: number;
}
```

#### Frontend Error Display

- Use Carbon InlineNotification or ToastNotification
- Error messages are descriptive and actionable
- Errors announced via `aria-live="assertive"`
- Retry buttons where appropriate

---

## Data Structure Gaps & Required Backend Changes

### 1. Analysis Response Enhancement

**Current**: Basic bottleneck info
**Needed**:

```typescript
bottlenecks: Array<{
  id: string; // For referencing in graph
  type: string;
  severity: "critical" | "high" | "medium" | "low";
  description: string;
  location: {
    job: string;
    step?: string;
    line_number?: number;
  };
  impact: string;
  recommendation: string; // Specific fix for this bottleneck
}>;
```

### 2. Workflow Structure Enhancement

**Current**: Basic job list
**Needed**:

```typescript
workflow_structure: {
  name: string;
  triggers: string[];
  jobs: Array<{
    id: string; // For graph nodes
    name: string;
    steps: Array<{
      name: string;
      command: string;
      estimated_duration: string;
    }>;
    dependencies: string[]; // Job IDs
    estimated_duration: string;
    parallelizable: boolean;
    position?: { x: number; y: number }; // For graph layout
  }>;
  overall_structure: "sequential" | "parallel" | "mixed";
  critical_path: string[]; // Job IDs
};
```

### 3. Fix Response Enhancement

**Current**: Basic diff
**Needed**:

```typescript
{
  fix_id: string;
  analysis_id: string;
  status: "completed";
  optimized_workflow: object;
  yaml_formatted: string; // For display
  changes: Array<{
    id: string;
    type: "parallelization" | "caching" | "conditional" | "optimization";
    description: string;
    before: string;
    after: string;
    impact: string;
    affected_jobs: string[];
  }>;
  improvements: {
    time_saved: string;
    efficiency_gain: string;
    optimizations_applied: number;
    cost_reduction: string;
    before_duration: string;
    after_duration: string;
  };
  diff: string;
  pr_description_preview: string;
  validation_status: {
    valid: boolean;
    errors: string[];
    warnings: string[];
  };
}
```

---

## Component Architecture

### Page Components

1. **HomePage** (`src/pages/HomePage.tsx`)
   - RepoInput component
   - Demo examples selector
   - Getting started guide

2. **ResultsPage** (`src/pages/ResultsPage.tsx`)
   - Phase tabs (Diagnose, Prescribe, Treat)
   - Phase-specific content
   - Reasoning panel (sidebar)
   - Progress indicator

### Shared Components

1. **DashboardHeader** - App header with branding
2. **StageIndicator** - Phase navigation tabs
3. **ReasoningPanel** - Bob's thinking process
4. **ProgressIndicator** - Loading states
5. **ErrorBoundary** - Error handling

### Phase-Specific Components

**Diagnose Phase**:

- DiagnosisCard
- WorkflowGraph
- MetricsTable
- BottlenecksList

**Prescribe Phase**:

- DiffView
- ChangesList
- ImprovementsSummary
- ApprovalModal

**Treat Phase**:

- DeploymentStatus
- PRPreview
- ResultsSummary

---

## API Client Structure

### `src/api/client.ts`

```typescript
class ProcessDoctorAPI {
  async analyzeWorkflow(input: AnalyzeRequest): Promise<AnalyzeResponse>
  async generateFix(request: FixRequest): Promise<FixResponse>
  async createPR(request: PRRequest): Promise<PRResponse>
  async getPRStatus(repo: string, prNumber: number): Promise<PRStatus>
  async streamReasoning(analysisId: string): EventSource // SSE
}
```

### `src/api/types.ts`

- All TypeScript interfaces matching backend schemas
- Enhanced with frontend-specific fields

---

## State Management

### React Query Setup

```typescript
// Queries
useAnalyzeWorkflow()
useGenerateFix()
useCreatePR()
usePRStatus()

// Mutations
useAnalyzeMutation()
useFixMutation()
usePRMutation()
```

### Local State

- Current phase
- Analysis ID
- Fix ID
- User selections (strategy, repository)

---

## Accessibility Implementation Checklist

### Global

- [x] Skip-to-main-content link
- [x] Semantic HTML structure
- [x] Proper heading hierarchy
- [x] Focus management
- [x] Keyboard navigation
- [x] Color contrast (4.5:1 for text, 3:1 for UI)
- [x] `prefers-reduced-motion` support

### Per Component

- [x] All interactive elements keyboard accessible
- [x] Focus indicators visible (3:1 contrast)
- [x] ARIA labels on icon-only buttons
- [x] `aria-live` regions for dynamic content
- [x] Form labels and error associations
- [x] Modal focus traps
- [x] Screen reader text for visual-only info

---

## IBM Carbon Integration

### Components to Use

1. **Form Elements**: TextInput, TextArea, Select, Button
2. **Navigation**: Tabs, Breadcrumb
3. **Feedback**: InlineNotification, ToastNotification, Loading
4. **Data Display**: DataTable, Tag, CodeSnippet
5. **Overlays**: Modal, Tooltip
6. **Layout**: Grid, Column

### Theme

- Use Carbon Gray 100 theme (dark mode)
- Custom tokens for ProcessDoctor brand colors
- Maintain Carbon spacing and typography scales

---

## Demo Data Structure

### Sample Workflow Input

```yaml
name: CI Pipeline
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm run lint
  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm test
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm run build
```

### Expected Analysis Output

- **Bottlenecks**: Sequential execution, no caching, redundant checkouts
- **Current Duration**: 40 minutes
- **Optimal Duration**: 15 minutes
- **Improvement**: 62%

---

## Implementation Priority

### Phase 1 (MVP)

1. ✅ Backend API structure complete
2. Frontend setup (Vite, React, Carbon)
3. RepoInput component
4. DiagnosisCard component
5. Basic workflow graph
6. DiffView component
7. PR creation flow

### Phase 2 (Enhancement)

1. Reasoning panel with SSE
2. Interactive workflow graph
3. Advanced diff view
4. Approval modal
5. Error handling
6. Loading states

### Phase 3 (Polish)

1. Accessibility audit and fixes
2. Animation and transitions
3. Demo mode with sample data
4. Documentation
5. Performance optimization

---

## Testing Strategy

### Accessibility Testing

1. Keyboard navigation test (unplug mouse)
2. Screen reader test (VoiceOver/NVDA)
3. Color contrast check (WebAIM)
4. Zoom test (200%)
5. Lighthouse accessibility audit (95+ score)
6. axe DevTools scan

### Functional Testing

1. End-to-end flow test
2. API integration tests
3. Component unit tests
4. Error scenario tests

---

## Conclusion

This plan provides a complete mapping between the UX flow and backend APIs. Key gaps identified:

1. Need reasoning steps streaming (SSE)
2. Need enhanced workflow structure with graph positions
3. Need PR description preview in fix response
4. Need validation status in responses

All components will use IBM Carbon for consistency and built-in accessibility. The implementation will follow WCAG 2.1 Level AA standards throughout.
