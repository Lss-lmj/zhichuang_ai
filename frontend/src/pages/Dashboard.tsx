import { useEffect, useMemo, useState } from "react";

import { askAgent } from "../shared/api/agent";
import { analyzeDemoAssignment, fetchAssignmentDashboard } from "../shared/api/assignments";
import {
  fetchGrowthProfile,
  generateLearningPlan,
  recommendCompetitions,
  recommendTeam,
} from "../shared/api/growth";
import type { ChatResponse } from "../shared/types/agent";
import type { AssignmentDashboard, AssignmentReport } from "../shared/types/assignments";
import type {
  CompetitionRecommendResponse,
  GrowthProfile,
  LearningPlan,
  TeamRecommendResponse,
} from "../shared/types/growth";

type ViewMode = "student" | "teacher" | "knowledge" | "growth";

export function Dashboard() {
  const [mode, setMode] = useState<ViewMode>("teacher");
  const [report, setReport] = useState<AssignmentReport | null>(null);
  const [dashboard, setDashboard] = useState<AssignmentDashboard | null>(null);
  const [profile, setProfile] = useState<GrowthProfile | null>(null);
  const [plan, setPlan] = useState<LearningPlan | null>(null);
  const [competitions, setCompetitions] = useState<CompetitionRecommendResponse | null>(null);
  const [team, setTeam] = useState<TeamRecommendResponse | null>(null);
  const [chatQuestion, setChatQuestion] = useState("如何准备算法竞赛？");
  const [chatResponse, setChatResponse] = useState<ChatResponse | null>(null);
  const [chatLoading, setChatLoading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    async function loadData() {
      try {
        setLoading(true);
        setError(null);
        const [reportData, dashboardData, profileData, planData, competitionData, teamData] =
          await Promise.all([
            analyzeDemoAssignment(),
            fetchAssignmentDashboard(),
            fetchGrowthProfile(),
            generateLearningPlan(),
            recommendCompetitions(),
            recommendTeam(),
          ]);

        if (mounted) {
          setReport(reportData);
          setDashboard(dashboardData);
          setProfile(profileData);
          setPlan(planData);
          setCompetitions(competitionData);
          setTeam(teamData);
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

  async function handleAskAgent(question = chatQuestion) {
    try {
      setChatLoading(true);
      setError(null);
      setChatQuestion(question);
      const response = await askAgent(question);
      setChatResponse(response);
      setMode("knowledge");
    } catch (err) {
      setError(err instanceof Error ? err.message : "知识库问答加载失败");
    } finally {
      setChatLoading(false);
    }
  }

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
          <button className={mode === "growth" ? "active" : ""} onClick={() => setMode("growth")}>
            成长路径
          </button>
          <button
            className={mode === "knowledge" ? "active" : ""}
            onClick={() => {
              setMode("knowledge");
              if (!chatResponse) {
                handleAskAgent();
              }
            }}
          >
            知识库问答
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
            <h1>
              {mode === "teacher"
                ? "课程作业学情诊断"
                : mode === "student"
                  ? "学生作业分析报告"
                  : mode === "growth"
                    ? "学生成长路径"
                    : "学科知识库问答"}
            </h1>
          </div>
          <button
            className="primary-action"
            onClick={() => (mode === "knowledge" ? handleAskAgent() : window.location.reload())}
          >
            {mode === "knowledge" ? "重新检索" : "重新分析"}
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

        {!loading && !error && mode === "knowledge" && (
          <KnowledgeAssistant
            question={chatQuestion}
            response={chatResponse}
            loading={chatLoading}
            onQuestionChange={setChatQuestion}
            onAsk={handleAskAgent}
          />
        )}

        {!loading && !error && mode === "growth" && profile && plan && competitions && team && (
          <GrowthPath
            profile={profile}
            plan={plan}
            competitions={competitions}
            team={team}
          />
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

function KnowledgeAssistant({
  question,
  response,
  loading,
  onQuestionChange,
  onAsk,
}: {
  question: string;
  response: ChatResponse | null;
  loading: boolean;
  onQuestionChange: (question: string) => void;
  onAsk: (question?: string) => void;
}) {
  const examples = ["如何准备算法竞赛？", "教师怎么看本次代码作业共性问题？", "AI 应用开发首个 Demo 做什么？"];

  return (
    <>
      <section className="ask-panel">
        <div>
          <span className="section-label">RAG 知识库</span>
          <h2>围绕课程、作业、竞赛和项目案例给出可追溯回答</h2>
        </div>
        <div className="ask-box">
          <input
            value={question}
            onChange={(event) => onQuestionChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                onAsk();
              }
            }}
            aria-label="知识库问题"
          />
          <button onClick={() => onAsk()} disabled={loading || !question.trim()}>
            {loading ? "检索中" : "提问"}
          </button>
        </div>
        <div className="quick-questions">
          {examples.map((example) => (
            <button key={example} onClick={() => onAsk(example)}>
              {example}
            </button>
          ))}
        </div>
      </section>

      <section className="panel-grid">
        <article className="panel wide">
          <span className="section-label">回答</span>
          <div className="answer-box">
            {response ? (
              response.answer.split("\n").map((line) => <p key={line}>{line}</p>)
            ) : (
              <p>选择一个问题，系统会从首批知识库资料中检索并生成回答。</p>
            )}
          </div>
        </article>

        <article className="panel">
          <span className="section-label">引用来源</span>
          <div className="citation-list">
            {response?.citations.map((citation) => (
              <div className="citation-card" key={`${citation.title}-${citation.source_type}`}>
                <strong>{citation.title}</strong>
                <span>{citation.source_type}</span>
                <p>{citation.snippet}</p>
              </div>
            ))}
            {!response && <p className="muted">等待检索结果。</p>}
          </div>
        </article>
      </section>
    </>
  );
}

function GrowthPath({
  profile,
  plan,
  competitions,
  team,
}: {
  profile: GrowthProfile;
  plan: LearningPlan;
  competitions: CompetitionRecommendResponse;
  team: TeamRecommendResponse;
}) {
  return (
    <>
      <section className="growth-hero">
        <div>
          <span className="section-label">能力画像</span>
          <h2>
            {profile.student_name} · {profile.target_path}
          </h2>
          <p>{plan.overview}</p>
        </div>
        <div className="growth-actions">
          {profile.next_actions.map((action) => (
            <span key={action}>{action}</span>
          ))}
        </div>
      </section>

      <section className="panel-grid">
        <article className="panel wide">
          <span className="section-label">画像维度</span>
          <div className="score-list">
            {profile.dimensions.map((dimension) => (
              <div className="score-detail" key={dimension.dimension}>
                <ScoreBar label={dimension.dimension} score={dimension.score} />
                <p>{dimension.summary}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <span className="section-label">风险提醒</span>
          <div className="risk-list">
            {profile.risks.map((risk) => (
              <div key={risk}>{risk}</div>
            ))}
          </div>
          <span className="section-label block-label">优势</span>
          <div className="tag-list">
            {profile.strengths.map((strength) => (
              <span key={strength}>{strength}</span>
            ))}
          </div>
        </article>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <span className="section-label">学习计划</span>
            <h2>{plan.goal}</h2>
          </div>
          <span className="muted">{plan.weeks} 周</span>
        </div>
        <div className="timeline">
          {plan.tasks.map((task) => (
            <article className="timeline-item" key={`${task.week}-${task.title}`}>
              <strong>W{task.week}</strong>
              <div>
                <h3>{task.title}</h3>
                <p>{task.outcome}</p>
                <small>{task.resources.join(" / ")}</small>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel-grid">
        <article className="panel">
          <span className="section-label">竞赛推荐</span>
          <div className="recommend-list">
            {competitions.recommendations.map((item) => (
              <div className="recommend-card" key={item.name}>
                <div>
                  <strong>{item.name}</strong>
                  <span>{item.category}</span>
                </div>
                <b>{item.match_score}</b>
                <p>{item.reason}</p>
                <small>{item.risk}</small>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <span className="section-label">组队推荐</span>
          <div className="recommend-list">
            {team.candidates.map((candidate) => (
              <div className="recommend-card" key={candidate.student_id}>
                <div>
                  <strong>{candidate.name}</strong>
                  <span>{candidate.role}</span>
                </div>
                <b>{candidate.match_score}</b>
                <p>{candidate.complement}</p>
                <small>{candidate.evidence.join(" / ")}</small>
              </div>
            ))}
          </div>
        </article>
      </section>
    </>
  );
}
