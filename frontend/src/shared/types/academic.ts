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
