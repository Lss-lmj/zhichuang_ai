import type { ClassListResponse, CourseListResponse, StudentListResponse } from "../types/academic";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchCourses(): Promise<CourseListResponse> {
  return requestJson<CourseListResponse>("/courses");
}

export function fetchClasses(courseId = "course_web_2026"): Promise<ClassListResponse> {
  return requestJson<ClassListResponse>(`/courses/${courseId}/classes`);
}

export function fetchStudents(classId = "class_cs_2024_01"): Promise<StudentListResponse> {
  return requestJson<StudentListResponse>(`/classes/${classId}/students`);
}
