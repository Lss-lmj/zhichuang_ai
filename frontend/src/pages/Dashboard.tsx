const modules = [
  {
    title: "课程作业代码分析",
    desc: "上传课程作业代码，生成多维度评分、能力证据和教师可读报告。",
  },
  {
    title: "教师学情诊断",
    desc: "查看班级提交情况、共性问题、学生个人作业报告和能力分布。",
  },
  {
    title: "学生成长路径",
    desc: "基于画像、知识库和目标方向生成学习路径、竞赛建议和组队推荐。",
  },
  {
    title: "RAG 知识库",
    desc: "管理课程大纲、作业要求、评分 Rubric、代码样例和竞赛资料。",
  },
];

export function Dashboard() {
  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">智创Agent</p>
          <h1>计算机学科垂类大模型与双创能力赋能平台</h1>
          <p className="lead">
            面向学校真实教学场景，连接学生成长、课程作业代码分析、教师学情诊断与竞赛创新能力培养。
          </p>
        </div>
      </section>

      <section className="module-grid">
        {modules.map((module) => (
          <article className="module-card" key={module.title}>
            <h2>{module.title}</h2>
            <p>{module.desc}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
