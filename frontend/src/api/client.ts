/**
 * Process Doctor API Client
 * 
 * Provides typed API methods for interacting with the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';;

// Type definitions
export interface AnalyzeRequest {
  workflow_input: string;
  source_type: 'text' | 'github' | 'file';
}

export interface AnalyzeResponse {
  analysis_id: string;
  status: string;
  workflow_structure?: any;
  bottlenecks: Array<{
    type: string;
    severity: string;
    description: string;
    location: string;
    impact: string;
  }>;
  metrics: {
    current_duration: string;
    estimated_optimal: string;
    efficiency_score: number;
  };
  recommendations: string[];
  estimated_improvement: string;
}

export interface FixRequest {
  analysis_id: string;
  optimization_strategy?: 'aggressive' | 'balanced' | 'conservative';
}

export interface FixResponse {
  fix_id: string;
  analysis_id: string;
  status: string;
  optimized_workflow?: any;
  changes: Array<{
    type: string;
    description: string;
    impact: string;
  }>;
  improvements: {
    time_saved: string;
    efficiency_gain: string;
    optimizations_applied: number;
  };
  diff: string;
}

export interface PRRequest {
  fix_id: string;
  repository: string;
  branch?: string;
  title?: string;
  description?: string;
}

export interface PRResponse {
  pr_number: number;
  pr_url: string;
  branch: string;
  status: string;
  message: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  timestamp: string;
  environment: string;
}

// API Error class
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

// Helper function for API requests
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  try {
    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new APIError(
        errorData.error || errorData.detail || 'API request failed',
        response.status,
        errorData
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(
      error instanceof Error ? error.message : 'Network error',
      0
    );
  }
}

// API Client
export const api = {
  /**
   * Health check endpoint
   */
  health: {
    check: () => apiRequest<HealthResponse>('/health'),
    ready: () => apiRequest<{ status: string }>('/ready'),
  },

  /**
   * Workflow analysis endpoints
   */
  analyze: {
    /**
     * Analyze a workflow for optimization opportunities
     */
    create: (data: AnalyzeRequest) =>
      apiRequest<AnalyzeResponse>('/api/analyze', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    /**
     * Get analysis results by ID
     */
    get: (analysisId: string) =>
      apiRequest<AnalyzeResponse>(`/api/analyze/${analysisId}`),
  },

  /**
   * Workflow optimization endpoints
   */
  fix: {
    /**
     * Generate optimized workflow
     */
    create: (data: FixRequest) =>
      apiRequest<FixResponse>('/api/fix', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    /**
     * Get fix results by ID
     */
    get: (fixId: string) =>
      apiRequest<FixResponse>(`/api/fix/${fixId}`),
  },

  /**
   * Pull request endpoints
   */
  pr: {
    /**
     * Create a pull request with optimized workflow
     */
    create: (data: PRRequest) =>
      apiRequest<PRResponse>('/api/pr', {
        method: 'POST',
        body: JSON.stringify(data),
      }),

    /**
     * Get pull request status
     */
    getStatus: (repository: string, prNumber: number) =>
      apiRequest<any>(`/api/pr/${repository}/${prNumber}`),
  },
};

// React Query hooks (optional, for better integration)
export const queryKeys = {
  health: ['health'] as const,
  analyze: (id: string) => ['analyze', id] as const,
  fix: (id: string) => ['fix', id] as const,
  prStatus: (repo: string, prNumber: number) => ['pr', repo, prNumber] as const,
};

// Export default
export default api;

// Made with Bob
