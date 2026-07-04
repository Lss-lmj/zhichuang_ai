from __future__ import annotations

from app.schemas.academic import (
    ClassListResponse,
    ClassSummary,
    CourseListResponse,
    CourseSummary,
    StudentListResponse,
    StudentSummary,
)


class AcademicService:
    courses = [
        CourseSummary(
            course_id="course_web_2026",
            name="Web 应用开发",
            term="2025-2026 春季学期",
            teacher_name="周老师",
            description="围绕 Flask、前端页面、数据库访问和项目文档完成 Web 项目实践。",
        ),
        CourseSummary(
            course_id="course_algo_2026",
            name="算法设计与分析",
            term="2025-2026 春季学期",
            teacher_name="李老师",
            description="围绕数据结构、搜索、动态规划和图论训练算法竞赛基础能力。",
        ),
    ]
    classes = [
        ClassSummary(
            class_id="class_cs_2024_01",
            course_id="course_web_2026",
            name="2024 级计算机科学与技术 1 班",
            grade="2024",
            major="计算机科学与技术",
            student_count=32,
        ),
        ClassSummary(
            class_id="class_cs_2024_01",
            course_id="course_algo_2026",
            name="2024 级计算机科学与技术 1 班",
            grade="2024",
            major="计算机科学与技术",
            student_count=32,
        ),
    ]
    students = [
        StudentSummary(
            student_id="student_001",
            name="林一舟",
            student_no="2024010101",
            class_id="class_cs_2024_01",
            target_path="AI 应用开发 / 软件项目实践",
            tags=["工程实践", "RAG", "后端接口"],
        ),
        StudentSummary(
            student_id="student_002",
            name="陈星然",
            student_no="2024010102",
            class_id="class_cs_2024_01",
            target_path="前端交互 / 项目展示",
            tags=["React", "交互设计", "答辩材料"],
        ),
        StudentSummary(
            student_id="student_003",
            name="周明远",
            student_no="2024010103",
            class_id="class_cs_2024_01",
            target_path="算法竞赛 / 评测",
            tags=["算法", "测试用例", "评测"],
        ),
        StudentSummary(
            student_id="student_004",
            name="沈知夏",
            student_no="2024010104",
            class_id="class_cs_2024_01",
            target_path="产品表达 / 双创材料",
            tags=["需求分析", "项目报告", "路演"],
        ),
        StudentSummary(
            student_id="student_005",
            name="许嘉木",
            student_no="2024010105",
            class_id="class_cs_2024_01",
            target_path="数据库 / 部署",
            tags=["SQL", "Docker", "运维"],
        ),
    ]

    def list_courses(self) -> CourseListResponse:
        return CourseListResponse(courses=self.courses)

    def list_classes(self, course_id: str) -> ClassListResponse:
        classes = [class_item for class_item in self.classes if class_item.course_id == course_id]
        return ClassListResponse(course_id=course_id, classes=classes)

    def list_students(self, class_id: str) -> StudentListResponse:
        students = [student for student in self.students if student.class_id == class_id]
        return StudentListResponse(class_id=class_id, students=students)
