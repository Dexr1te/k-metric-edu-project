export interface User {
  id: number;
  username: string;
  role: string;
}

export interface CronTask {
  id: number;
  name: string;
  status: 'success' | 'failed';
  runtime: number;
  executed_at: string;
}

export interface ApiMetricSummary {
  endpoint: string;
  avg_response_time: number;
  request_count: number;
  hour: string;
}

export interface AuthResponse {
  token: string;
}
