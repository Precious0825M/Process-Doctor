# Backend Integration Guide

## Overview

The frontend is now fully integrated with the backend API. The "Diagnose Workflow" button triggers actual API calls to analyze workflows, generate optimizations, and create pull requests.

## Architecture

### API Service Layer
- **Location**: `frontend/src/services/api.ts`
- **Purpose**: Centralized API communication layer
- **Features**:
  - Type-safe API calls with TypeScript interfaces
  - Error handling with custom `APIError` class
  - Configurable API base URL via environment variables

### Data Flow

```
User Input → InputSection → App State → DiagnoseSection → Backend API
                                              ↓
                                        Analysis Results
                                              ↓
                                      PrescribeSection → Backend API
                                              ↓
                                        Fix Generation
                                              ↓
                                       TreatSection → Backend API
                                              ↓
                                         PR Creation
```

## API Endpoints Used

### 1. Analyze Workflow
- **Endpoint**: `POST /api/analyze`
- **Triggered by**: DiagnoseSection on mount
- **Request**:
  ```typescript
  {
    workflow_input: string,
    source_type: 'text' | 'github' | 'file'
  }
  ```
- **Response**:
  ```typescript
  {
    analysis_id: string,
    status: string,
    bottlenecks: Bottleneck[],
    metrics: { current_duration, estimated_optimal, efficiency_score },
    recommendations: string[],
    estimated_improvement: string
  }
  ```

### 2. Generate Fix
- **Endpoint**: `POST /api/fix`
- **Triggered by**: PrescribeSection on mount
- **Request**:
  ```typescript
  {
    analysis_id: string,
    optimization_strategy: 'aggressive' | 'balanced' | 'conservative'
  }
  ```
- **Response**:
  ```typescript
  {
    fix_id: string,
    optimized_workflow: object,
    changes: Change[],
    improvements: { time_saved, efficiency_gain, optimizations_applied },
    diff: string
  }
  ```

### 3. Create Pull Request
- **Endpoint**: `POST /api/pr`
- **Triggered by**: TreatSection on user approval
- **Request**:
  ```typescript
  {
    fix_id: string,
    repository: string,
    branch: string,
    title: string,
    description: string
  }
  ```
- **Response**:
  ```typescript
  {
    pr_number: number,
    pr_url: string,
    branch: string,
    status: string,
    message: string
  }
  ```

## Component Updates

### App.tsx
- Manages global state for analysis, fix, and PR data
- Passes data and callbacks to child components
- Handles phase transitions

### InputSection
- Updated to pass input type ('text' or 'github') to parent
- Triggers analysis on "Diagnose workflow" button click

### DiagnoseSection
- Calls `/api/analyze` on mount if no analysis data exists
- Shows loading state during API call
- Displays real bottlenecks and metrics from API response
- Falls back to demo data if API fails

### PrescribeSection
- Calls `/api/fix` on mount if analysis data exists but no fix data
- Shows loading state during optimization generation
- Displays real improvements from API response
- Falls back to demo data if API fails

### TreatSection
- Calls `/api/pr` when user approves the treatment
- Shows loading state during PR creation
- Displays real PR details from API response
- Shows error messages if PR creation fails

## Loading States

Each section implements loading states:
- **DiagnoseSection**: "Bob is analyzing your workflow..."
- **PrescribeSection**: "Bob is optimizing your workflow..."
- **TreatSection**: "Creating pull request..."

## Error Handling

All sections implement error handling:
- Display error messages to users
- Provide "Retry" buttons for failed operations
- Log errors to console for debugging
- Graceful fallback to demo data when appropriate

## Environment Configuration

### Frontend (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
```

### Backend (.env)
```bash
# Backend configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# API Keys (if needed)
GITHUB_TOKEN=your_github_token
OPENAI_API_KEY=your_openai_key
```

## Testing the Integration

### 1. Start Backend
```bash
cd backend
source venv/bin/activate
python run_dev.py
```

### 2. Start Frontend
```bash
cd frontend
npm start
```

### 3. Test Flow
1. Enter a workflow description or GitHub URL
2. Click "Diagnose workflow"
3. Wait for analysis to complete (loading state)
4. Review bottlenecks and metrics
5. Click "See prescription"
6. Wait for optimization generation (loading state)
7. Review before/after comparison
8. Click "Review and approve treatment"
9. Review generated YAML and PR preview
10. Click "Approve and deploy"
11. Confirm in modal
12. Wait for PR creation (loading state)
13. View success message with PR link

## Fallback Behavior

The integration is designed to gracefully handle backend unavailability:
- If backend is down, sections will show error messages
- Demo data is used as fallback in some cases
- Users can retry failed operations
- Clear error messages guide users on what went wrong

## Future Enhancements

1. **Caching**: Store analysis results to avoid re-fetching
2. **Polling**: Check PR status after creation
3. **Webhooks**: Real-time updates on workflow execution
4. **Repository Detection**: Auto-extract repository from GitHub URLs
5. **Batch Operations**: Analyze multiple workflows at once
6. **History**: View past analyses and optimizations

## Troubleshooting

### Backend Not Responding
- Check if backend is running: `curl http://localhost:8000/health`
- Verify CORS settings in backend `.env`
- Check browser console for CORS errors

### API Errors
- Check backend logs for detailed error messages
- Verify API keys are configured correctly
- Ensure database/dependencies are running

### Type Errors
- Run `npm run build` to check for TypeScript errors
- Verify API response matches TypeScript interfaces
- Update interfaces in `frontend/src/services/api.ts` if needed

## Summary

The frontend now uses real backend APIs instead of dummy data:
- ✅ Analysis endpoint integrated
- ✅ Fix generation endpoint integrated  
- ✅ PR creation endpoint integrated
- ✅ Loading states implemented
- ✅ Error handling implemented
- ✅ Type-safe API layer created
- ✅ Environment configuration documented
