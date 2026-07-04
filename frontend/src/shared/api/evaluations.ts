import type { EvaluationDashboardResponse } from "../types/evaluations";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchEvaluationDashboard(): Promise<EvaluationDashboardResponse> {
  return requestJson<EvaluationDashboardResponse>("/evaluations/dashboard");
}
