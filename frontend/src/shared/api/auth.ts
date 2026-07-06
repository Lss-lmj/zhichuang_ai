import type {
  SchoolAccountsResponse,
  SchoolSessionResponse,
  LocalAccountsResponse,
  SchoolIdentitySessionRequest,
} from "../types/auth";
import { responseErrorMessage } from "./errors";

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
    throw new Error(await responseErrorMessage(response));
  }

  return response.json() as Promise<T>;
}

export function fetchSchoolAccounts(): Promise<SchoolAccountsResponse> {
  return requestJson<SchoolAccountsResponse>("/auth/demo-accounts");
}

export function fetchLocalAccounts(token: string): Promise<LocalAccountsResponse> {
  return requestJson<LocalAccountsResponse>("/auth/local-accounts", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

export function createSchoolAccountSession(userId: string): Promise<SchoolSessionResponse> {
  return requestJson<SchoolSessionResponse>("/auth/demo-session", {
    method: "POST",
    body: JSON.stringify({ user_id: userId }),
  });
}

export function createLocalSession(userId: string): Promise<SchoolSessionResponse> {
  return requestJson<SchoolSessionResponse>("/auth/local-session", {
    method: "POST",
    body: JSON.stringify({ user_id: userId }),
  });
}

export function createSchoolIdentitySession(
  payload: SchoolIdentitySessionRequest,
  sharedSecret: string,
): Promise<SchoolSessionResponse> {
  return requestJson<SchoolSessionResponse>("/auth/school-session", {
    method: "POST",
    headers: {
      "X-School-Identity-Secret": sharedSecret,
    },
    body: JSON.stringify(payload),
  });
}
