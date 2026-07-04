export type CourseSummary = {
  course_id: string;
  name: string;
  term: string;
  teacher_name: string;
  description: string;
};

export type ClassSummary = {
  class_id: string;
  course_id: string;
  name: string;
  grade: string;
  major: string;
  student_count: number;
};

export type StudentSummary = {
  student_id: string;
  name: string;
  student_no: string;
  class_id: string;
  target_path: string;
  tags: string[];
};

export type CourseListResponse = {
  courses: CourseSummary[];
};

export type ClassListResponse = {
  course_id: string;
  classes: ClassSummary[];
};

export type StudentListResponse = {
  class_id: string;
  students: StudentSummary[];
};

export type AcademicImportCourse = {
  course_id: string;
  name: string;
  term?: string;
  teacher_id?: string;
  teacher_name?: string;
  teacher_no?: string;
  description?: string;
};

export type AcademicImportClass = {
  class_id: string;
  course_id: string;
  name: string;
  grade?: string;
  major?: string;
};

export type AcademicImportStudent = {
  student_id: string;
  name: string;
  student_no: string;
  class_id: string;
  course_ids?: string[];
  target_path?: string;
  tags?: string[];
};

export type AcademicImportRequest = {
  courses?: AcademicImportCourse[];
  classes?: AcademicImportClass[];
  students?: AcademicImportStudent[];
};

export type AcademicImportResponse = {
  imported_courses: number;
  imported_classes: number;
  imported_students: number;
  imported_memberships: number;
  message: string;
};
