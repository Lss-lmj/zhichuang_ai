import type {
  AgentTaskActionResponse,
  AgentTaskCreateRequest,
  AgentTaskStatus,
  LearningTask,
  ReviewGeneratePayload,
  ReviewResponse,
  SaveTaskPayload,
  TaskListResponse,
} from "../types/tasks";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

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

function authHeaders(token?: string): HeadersInit {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export function fetchStudentTasks(
  studentId = "student_001",
  token?: string,
): Promise<TaskListResponse> {
  return requestJson<TaskListResponse>(`/students/${studentId}/tasks`, {
    headers: authHeaders(token),
  });
}

export function saveTask(
  payload: SaveTaskPayload,
  studentId = "student_001",
  token?: string,
): Promise<LearningTask> {
  return requestJson<LearningTask>("/tasks", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify({
      student_id: studentId,
      ...payload,
    }),
  });
}

export function generateReview(
  studentId = "student_001",
  token?: string,
  payload: ReviewGeneratePayload = {
    period: "本周",
    completed_task_ids: [],
    notes: null,
  },
): Promise<ReviewResponse> {
  return requestJson<ReviewResponse>("/reviews/generate", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify({
      student_id: studentId,
      ...payload,
    }),
  });
}

export function createAgentTask(
  payload: AgentTaskCreateRequest,
  token?: string,
): Promise<AgentTaskStatus> {
  return requestJson<AgentTaskStatus>("/agent-tasks", {
    method: "POST",
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
}

export function fetchAgentTask(taskId: string, token?: string): Promise<AgentTaskStatus> {
  return requestJson<AgentTaskStatus>(`/tasks/${taskId}`, {
    headers: authHeaders(token),
  });
}

export function cancelAgentTask(
  taskId: string,
  token?: string,
): Promise<AgentTaskActionResponse> {
  return requestJson<AgentTaskActionResponse>(`/tasks/${taskId}/cancel`, {
    method: "POST",
    headers: authHeaders(token),
  });
}

export function resumeAgentTask(
  taskId: string,
  token?: string,
): Promise<AgentTaskActionResponse> {
  return requestJson<AgentTaskActionResponse>(`/tasks/${taskId}/resume`, {
    method: "POST",
    headers: authHeaders(token),
  });
}
