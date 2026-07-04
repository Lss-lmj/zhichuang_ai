import type {
  CompetitionRecommendResponse,
  GrowthProfile,
  LearningPlan,
  TeamRecommendResponse,
} from "../types/growth";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchGrowthProfile(studentId = "student_001"): Promise<GrowthProfile> {
  return requestJson<GrowthProfile>(`/students/${studentId}/profile`);
}

export function generateLearningPlan(studentId = "student_001"): Promise<LearningPlan> {
  return requestJson<LearningPlan>("/plans/generate", {
    method: "POST",
    body: JSON.stringify({
      student_id: studentId,
      goal: "三个月内完成 AI 应用开发 Demo 并准备校级双创项目",
      weeks: 8,
    }),
  });
}

export function recommendCompetitions(
  studentId = "student_001",
): Promise<CompetitionRecommendResponse> {
  return requestJson<CompetitionRecommendResponse>("/competitions/recommend", {
    method: "POST",
    body: JSON.stringify({
      student_id: studentId,
      target: "AI 应用开发与软件项目实践",
      available_weeks: 8,
    }),
  });
}

export function recommendTeam(studentId = "student_001"): Promise<TeamRecommendResponse> {
  return requestJson<TeamRecommendResponse>("/teams/recommend", {
    method: "POST",
    body: JSON.stringify({
      student_id: studentId,
      project_goal: "做一个课程作业代码分析与教师看板 Demo",
    }),
  });
}
