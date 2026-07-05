import type { ViewMode } from "./navigation";

export type DemoAccount = {
  user_id: string;
  name: string;
  role: "student" | "teacher" | "admin" | string;
  title: string;
  default_view: ViewMode;
  authorized_courses: string[];
  authorized_classes: string[];
  modules: string[];
};

export type DemoAccountsResponse = {
  accounts: DemoAccount[];
};

export type LocalAccountsResponse = {
  accounts: DemoAccount[];
};

export type SchoolIdentitySessionRequest = {
  user_id?: string;
  student_no?: string;
  teacher_no?: string;
  email?: string;
};

export type DemoSessionResponse = {
  token: string;
  account: DemoAccount;
  expires_in: number;
};
