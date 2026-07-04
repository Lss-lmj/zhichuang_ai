import type { KnowledgeDocumentsResponse, KnowledgeSearchResponse } from "../types/knowledge";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`);

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function fetchKnowledgeDocuments(): Promise<KnowledgeDocumentsResponse> {
  return requestJson<KnowledgeDocumentsResponse>("/knowledge/documents");
}

export function searchKnowledge(query: string, limit = 5): Promise<KnowledgeSearchResponse> {
  const params = new URLSearchParams({ q: query, limit: String(limit) });
  return requestJson<KnowledgeSearchResponse>(`/knowledge/search?${params.toString()}`);
}
