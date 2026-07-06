import type { ViewMode } from "./navigation";

export type SchoolAccount = {
  user_id: string;
  name: string;
  role: "student" | "teacher" | "admin" | string;
  title: string;
  default_view: ViewMode;
  authorized_courses: string[];
  authorized_classes: string[];
  modules: string[];
};

export type SchoolAccountsResponse = {
  accounts: SchoolAccount[];
};

export type LocalAccountsResponse = {
  accounts: SchoolAccount[];
};

export type SchoolIdentitySessionRequest = {
  user_id?: string;
  student_no?: string;
  teacher_no?: string;
  email?: string;
};

export type SchoolSessionResponse = {
  token: string;
  account: SchoolAccount;
  expires_in: number;
};
