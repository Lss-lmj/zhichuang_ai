import type {
  EvaluationCaseCreate,
  EvaluationDashboardResponse,
  EvaluationRecordCreate,
  EvaluationUpsertResponse,
} from "../types/evaluations";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

function authHeaders(token?: string): HeadersInit {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchEvaluationDashboard(): Promise<EvaluationDashboardResponse> {
  return requestJson<EvaluationDashboardResponse>("/evaluations/dashboard");
}

export function createEvaluationCase(
  payload: EvaluationCaseCreate,
  token?: string,
): Promise<EvaluationUpsertResponse> {
  return requestJson<EvaluationUpsertResponse>("/evaluations/cases", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
}

export function createEvaluationRecord(
  payload: EvaluationRecordCreate,
  token?: string,
): Promise<EvaluationUpsertResponse> {
  return requestJson<EvaluationUpsertResponse>("/evaluations/records", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
}
