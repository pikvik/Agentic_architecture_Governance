const API_BASE_URL = 'http://localhost:8000';

export interface Agent {
  agent_id: string;
  name: string;
  agent_type: string;
  status: string;
  health_score: number;
  total_requests: number;
  successful_requests: number;
  failed_requests: number;
  average_response_time: number;
  error_count: number;
  last_error: string | null;
  last_activity: string | null;
  current_task: string | null;
  queue_length: number;
}

export interface GovernanceRequest {
  scope: string[];
  components: string[];
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  description: string;
}

export interface GovernanceResponse {
  validation_id: string;
  status: string;
  results: any[];
  summary: {
    total_validations: number;
    passed: number;
    failed: number;
    warnings: number;
    risk_score: number;
  };
  recommendations: string[];
  created_at: string;
}

export interface SwarmStatus {
  core_brain: Agent;
  specialized_agents: Record<string, Agent>;
  overall_health: number;
  active_tasks: number;
  total_agents: number;
}

export interface Report {
  id: string;
  type: string;
  status: string;
  created_at: string;
  file_size?: number;
  download_url?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Health and Status
  async getHealth(): Promise<{ status: string; swarm_health: number; active_agents: number; active_tasks: number }> {
    return this.request('/health');
  }

  async getSwarmStatus(): Promise<SwarmStatus> {
    return this.request('/swarm/status');
  }

  // Agents
  async getAgents(): Promise<{ agents: Record<string, Agent>; total_agents: number }> {
    return this.request('/agents');
  }

  async getAgent(agentId: string): Promise<Agent> {
    return this.request(`/agents/${agentId}`);
  }

  async startAgent(agentId: string): Promise<{ message: string }> {
    return this.request(`/agents/${agentId}/start`, { method: 'POST' });
  }

  async stopAgent(agentId: string): Promise<{ message: string }> {
    return this.request(`/agents/${agentId}/stop`, { method: 'POST' });
  }

  async restartAgent(agentId: string): Promise<{ message: string }> {
    return this.request(`/agents/${agentId}/restart`, { method: 'POST' });
  }

  // Governance Validation
  async startGovernanceValidation(request: GovernanceRequest): Promise<{ validation_id: string; message: string }> {
    return this.request('/governance/validate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getValidationStatus(validationId: string): Promise<{ status: string; progress: number; message: string }> {
    return this.request(`/governance/status/${validationId}`);
  }

  async getValidationResults(validationId: string): Promise<GovernanceResponse> {
    return this.request(`/governance/results/${validationId}`);
  }

  // Reports
  async getReports(): Promise<Report[]> {
    return this.request('/reports');
  }

  async generateReport(type: string, format: string, data: any): Promise<{ report_id: string; download_url: string }> {
    return this.request('/reports/generate', {
      method: 'POST',
      body: JSON.stringify({ type, format, data }),
    });
  }

  async downloadReport(reportId: string): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/reports/${reportId}/download`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.blob();
  }

  // System Information
  async getSystemInfo(): Promise<{ version: string; description: string; endpoints: string[] }> {
    return this.request('/');
  }
}

// Create and export a singleton instance
export const apiService = new ApiService();

// Export the class for testing or custom instances
export default ApiService;
