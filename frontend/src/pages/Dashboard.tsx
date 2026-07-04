import { useEffect, useMemo, useState } from "react";

import { analyzeDemoAssignment, fetchAssignmentDashboard } from "../shared/api/assignments";
import type { AssignmentDashboard, AssignmentReport } from "../shared/types/assignments";

type ViewMode = "student" | "teacher";

export function Dashboard() {
  const [mode, setMode] = useState<ViewMode>("teacher");
  const [report, setReport] = useState<AssignmentReport | null>(null);
  const [dashboard, setDashboard] = useState<AssignmentDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function loadData() {
      try {
        setLoading(true);
        setError(null);
        const [reportData, dashboardData] = await Promise.all([
          analyzeDemoAssignment(),
          fetchAssignmentDashboard(),
        ]);

        if (mounted) {
          setReport(reportData);
          setDashboard(dashboardData);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : "加载失败");
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadData();

    return () => {
      mounted = false;
    };
  }, []);

  const averageScore = useMemo(() => {
    if (!report) return 0;
    const total = report.scores.reduce((sum, score) => sum + score.score, 0);
    return Math.round(total / report.scores.length);
  }, [report]);

  return (
    <main className="workspace">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">Z</span>
          <div>
            <strong>智创Agent</strong>
            <span>教学智能体工作台</span>
          </div>
        </div>

        <nav className="nav-list" aria-label="主导航">
          <button className={mode === "teacher" ? "active" : ""} onClick={() => setMode("teacher")}>
            教师看板
          </button>
          <button className={mode === "student" ? "active" : ""} onClick={() => setMode("student")}>
            学生报告
          </button>
        </nav>

        <div className="side-note">
          <span>当前样例</span>
          <strong>Flask Web 项目实践</strong>
          <p>系统分析作业代码与说明，教师直接查看学情诊断。</p>
        </div>
      </aside>

      <section className="content">
        <header className="topbar">
          <div>
            <p className="eyebrow">智创Agent·计算机学科垂类大模型与双创能力赋能平台</p>
            <h1>{mode === "teacher" ? "课程作业学情诊断" : "学生作业分析报告"}</h1>
          </div>
          <button className="primary-action" onClick={() => window.location.reload()}>
            重新分析
          </button>
        </header>

        {loading && <div className="state-box">正在生成演示报告...</div>}
        {error && <div className="state-box error">接口未连接：{error}</div>}

        {!loading && !error && mode === "teacher" && dashboard && (
          <TeacherDashboard dashboard={dashboard} />
        )}

        {!loading && !error && mode === "student" && report && (
          <StudentReport report={report} averageScore={averageScore} />
        )}
      </section>
    </main>
  );
}

function TeacherDashboard({ dashboard }: { dashboard: AssignmentDashboard }) {
  return (
    <>
      <section className="summary-strip">
        {dashboard.metrics.map((metric) => (
          <article className="metric" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <small>{metric.trend}</small>
          </article>
        ))}
      </section>

      <section className="panel-grid">
        <article className="panel wide">
          <div className="panel-header">
            <div>
              <span className="section-label">班级维度分布</span>
              <h2>{dashboard.class_name}</h2>
            </div>
            <strong className="score-pill">{dashboard.average_score}</strong>
          </div>
          <div className="score-list">
            {dashboard.dimension_averages.map((score) => (
              <ScoreBar key={score.dimension} label={score.dimension} score={score.score} />
            ))}
          </div>
        </article>

        <article className="panel">
          <span className="section-label">共性问题</span>
          <div className="finding-list">
            {dashboard.common_findings.map((finding) => (
              <div className="finding-item" key={finding.title}>
                <strong>{finding.title}</strong>
                <p>{finding.detail}</p>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <span className="section-label">学生报告</span>
            <h2>提交情况与个人分析</h2>
          </div>
          <span className="muted">
            {dashboard.submitted_count}/{dashboard.total_students} 已提交
          </span>
        </div>
        <div className="report-table">
          {dashboard.reports.map((report) => (
            <div className="report-row" key={report.report_id}>
              <strong>{report.student_name}</strong>
              <span>{report.status}</span>
              <ScoreBar label="综合" score={report.overall_score} compact />
              <p>{report.summary}</p>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}

function StudentReport({
  report,
  averageScore,
}: {
  report: AssignmentReport;
  averageScore: number;
}) {
  return (
    <>
      <section className="report-hero">
        <div>
          <span className="section-label">{report.course_name}</span>
          <h2>
            {report.student_name} · {report.assignment_title}
          </h2>
          <p>{report.summary}</p>
        </div>
        <strong className="big-score">{averageScore}</strong>
      </section>

      <section className="panel-grid">
        <article className="panel wide">
          <span className="section-label">多维度评分</span>
          <div className="score-list">
            {report.scores.map((score) => (
              <div className="score-detail" key={score.dimension}>
                <ScoreBar label={score.dimension} score={score.score} />
                <p>{score.summary}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <span className="section-label">能力证据</span>
          <div className="evidence-list">
            {report.capability_evidence.map((item) => (
              <div key={item.dimension}>
                <strong>{item.dimension}</strong>
                <p>{item.evidence}</p>
                <small>{item.source}</small>
              </div>
            ))}
          </div>
        </article>
      </section>

      <section className="panel-grid">
        <article className="panel">
          <span className="section-label">主要问题</span>
          <div className="finding-list">
            {report.findings.map((finding) => (
              <div className={`finding-item ${finding.severity}`} key={finding.title}>
                <strong>{finding.title}</strong>
                <p>{finding.detail}</p>
                <small>{finding.suggestion}</small>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <span className="section-label">下一步任务</span>
          <ol className="task-list">
            {report.improvement_tasks.map((task) => (
              <li key={task}>{task}</li>
            ))}
          </ol>
        </article>
      </section>
    </>
  );
}

function ScoreBar({
  label,
  score,
  compact = false,
}: {
  label: string;
  score: number;
  compact?: boolean;
}) {
  return (
    <div className={compact ? "score-bar compact" : "score-bar"}>
      <div className="score-meta">
        <span>{label}</span>
        <strong>{score}</strong>
      </div>
      <div className="score-track">
        <span style={{ width: `${score}%` }} />
      </div>
    </div>
  );
}
