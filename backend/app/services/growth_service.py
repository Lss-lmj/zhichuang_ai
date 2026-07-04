from __future__ import annotations

from app.schemas.growth import (
    CapabilityDimension,
    CompetitionCatalogResponse,
    CompetitionInfo,
    CompetitionRecommendation,
    CompetitionRecommendRequest,
    CompetitionRecommendResponse,
    GrowthProfileResponse,
    LearningPlanRequest,
    LearningPlanResponse,
    PlanTask,
    TeamCandidate,
    TeamPoolStatus,
    TeamRecommendRequest,
    TeamRecommendResponse,
    TeamRequestCard,
    TeamRequestCreate,
)


class GrowthService:
    generated_at = "2026-07-05T09:00:00+08:00"
    team_created_at = "2026-07-05T11:20:00+08:00"
    competition_updated_at = "2026-07-05T11:40:00+08:00"
    competition_source_note = "系统内置首批竞赛清单，管理员可根据官方通知维护更新。"

    def get_profile(self, student_id: str) -> GrowthProfileResponse:
        return GrowthProfileResponse(
            student_id=student_id,
            student_name="林一舟",
            target_path="AI 应用开发 / 软件项目实践",
            generated_at=self.generated_at,
            dimensions=[
                CapabilityDimension(
                    dimension="算法基础",
                    score=76,
                    confidence=0.72,
                    summary="能完成基础题和常见数据结构应用，动态规划和图论需要继续训练。",
                    evidence=["课程作业中能拆解主流程", "算法竞赛训练记录显示基础专题完成度较高"],
                ),
                CapabilityDimension(
                    dimension="工程实践",
                    score=84,
                    confidence=0.81,
                    summary="具备 Web 项目搭建和接口联调能力，工程边界意识正在形成。",
                    evidence=["Flask 作业完成了页面、接口和数据流闭环", "README 有基本运行说明"],
                ),
                CapabilityDimension(
                    dimension="AI 应用开发",
                    score=79,
                    confidence=0.68,
                    summary="理解 RAG 和 Agent 应用形态，仍需补评测和部署经验。",
                    evidence=["能描述知识库问答流程", "项目计划包含 RAG、引用和评测任务"],
                ),
                CapabilityDimension(
                    dimension="表达与协作",
                    score=73,
                    confidence=0.64,
                    summary="能说明项目目标，但对接口、分工和复盘记录表达还不稳定。",
                    evidence=["项目说明有目标和运行步骤", "缺少稳定的周复盘记录"],
                ),
            ],
            strengths=["工程实践推进快", "适合承担后端接口和 Demo 集成", "能把作业产出转成项目案例"],
            risks=["自动化测试证据不足", "竞赛训练节奏容易被项目开发挤压", "项目表达材料需要模板约束"],
            next_actions=[
                "本周补齐 Flask 作业测试和 README 模板。",
                "两周内完成一个带引用的 RAG 问答 Demo。",
                "每周至少保留 3 次算法专题训练记录。",
            ],
        )

    def generate_plan(self, payload: LearningPlanRequest) -> LearningPlanResponse:
        tasks = [
            PlanTask(
                week=1,
                title="补齐工程基线",
                outcome="作业项目具备 README、接口列表、测试入口和演示数据。",
                resources=["Web 应用开发课程 Rubric", "软件项目实践案例模板"],
            ),
            PlanTask(
                week=2,
                title="完成 RAG 问答闭环",
                outcome="知识库问答能返回答案、引用来源和推荐路径。",
                resources=["AI 应用开发学习路径", "RAG 知识库建设 SOP"],
            ),
            PlanTask(
                week=3,
                title="接入作业分析报告",
                outcome="系统能生成学生报告和教师班级看板。",
                resources=["课程作业代码分析 SOP", "教师学情诊断看板说明"],
            ),
            PlanTask(
                week=4,
                title="形成竞赛准备节奏",
                outcome="完成基础语法、数据结构和搜索专题复盘。",
                resources=["算法竞赛训练路径", "蓝桥杯训练资料"],
            ),
            PlanTask(
                week=5,
                title="完善项目案例材料",
                outcome="输出需求、架构、接口、数据模型和测试记录。",
                resources=["软件项目实践案例模板"],
            ),
            PlanTask(
                week=6,
                title="组队协作与分工",
                outcome="确定后端、前端、算法、表达四类角色和协作节奏。",
                resources=["组队推荐能力互补规则"],
            ),
            PlanTask(
                week=7,
                title="演示与评测",
                outcome="准备固定演示账号、示例作业、知识库问答和教师看板脚本。",
                resources=["开发 SOP", "评测样例清单"],
            ),
            PlanTask(
                week=8,
                title="复盘与下一轮迭代",
                outcome="根据报告和演示反馈更新画像、任务和项目路线。",
                resources=["定期复盘流程", "能力画像评分口径"],
            ),
        ][: max(1, min(payload.weeks, 8))]

        return LearningPlanResponse(
            plan_id=f"plan_{payload.student_id}_ai_app",
            student_id=payload.student_id,
            goal=payload.goal,
            weeks=payload.weeks,
            overview="计划围绕工程基线、RAG Demo、作业分析、竞赛训练和项目表达五条线推进。",
            tasks=tasks,
            checkpoints=["第 2 周完成知识库问答", "第 4 周完成一次算法专题复盘", "第 7 周完成公网 Demo 演示脚本"],
        )

    def recommend_competitions(
        self, payload: CompetitionRecommendRequest
    ) -> CompetitionRecommendResponse:
        return CompetitionRecommendResponse(
            student_id=payload.student_id,
            target=payload.target,
            recommendations=[
                CompetitionRecommendation(
                    name="中国大学生计算机设计大赛",
                    category="软件应用 / AI 应用",
                    match_score=88,
                    reason="当前项目具备教学场景、AI 应用、知识库问答和可展示 Demo，适合软件应用类作品。",
                    preparation=["补齐作品说明书", "准备公网 Demo", "整理教师看板和学生报告演示脚本"],
                    risk="需要尽快补充真实课程样例和稳定演示流程。",
                ),
                CompetitionRecommendation(
                    name="中国国际大学生创新大赛",
                    category="双创项目",
                    match_score=82,
                    reason="平台面向学校真实使用，有教学应用和双创能力赋能叙事。",
                    preparation=["梳理用户场景", "准备商业/推广路径", "补充学校部署方案"],
                    risk="需要把产品价值讲清楚，避免只像技术 Demo。",
                ),
                CompetitionRecommendation(
                    name="蓝桥杯",
                    category="算法竞赛",
                    match_score=74,
                    reason="适合作为个人算法能力提升路径，反哺平台的竞赛推荐和训练计划能力。",
                    preparation=["数据结构专题", "搜索专题", "动态规划专题", "真题复盘"],
                    risk="与项目开发争抢时间，需要固定训练节奏。",
                ),
            ],
        )

    def list_competitions(self) -> CompetitionCatalogResponse:
        competitions = [
            CompetitionInfo(
                competition_id="competition_c4",
                name="中国大学生计算机设计大赛",
                organizer="中国大学生计算机设计大赛组织委员会",
                category="工程开发类",
                tracks=["软件应用", "AI 应用", "数字媒体"],
                registration_time="以当年官方通知为准",
                participant_requirements=(
                    "普通高校在校学生组队参赛，具体组别以官方通知为准。"
                ),
                work_requirements="提交可运行作品、说明材料、演示视频和证明材料。",
                official_url="https://jsjds.blcu.edu.cn/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
            CompetitionInfo(
                competition_id="competition_cy",
                name="中国国际大学生创新大赛",
                organizer="教育部等单位",
                category="创新创业类",
                tracks=["高教主赛道", "青年红色筑梦之旅", "产业命题"],
                registration_time="以当年官方通知为准",
                participant_requirements=(
                    "高校学生团队参赛，负责人和成员要求以官方通知为准。"
                ),
                work_requirements="提交项目计划书、路演材料、佐证材料和展示 Demo。",
                official_url="https://cy.ncss.cn/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
            CompetitionInfo(
                competition_id="competition_lanqiao",
                name="蓝桥杯全国软件和信息技术专业人才大赛",
                organizer="工业和信息化部人才交流中心等单位",
                category="算法类",
                tracks=["软件类", "电子类", "视觉艺术类"],
                registration_time="以当年官方通知为准",
                participant_requirements=(
                    "在校学生可按组别报名，具体科目和资格以官方通知为准。"
                ),
                work_requirements="按赛项完成在线编程、算法题或相关作品提交。",
                official_url="https://dasai.lanqiao.cn/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
            CompetitionInfo(
                competition_id="competition_icpc",
                name="ICPC 国际大学生程序设计竞赛",
                organizer="ICPC Foundation 及区域赛承办单位",
                category="算法类",
                tracks=["区域赛", "邀请赛", "校内选拔"],
                registration_time="以各赛站官方通知为准",
                participant_requirements="通常为高校学生三人组队参赛，资格以赛站规则为准。",
                work_requirements="在限定时间内完成算法编程题目。",
                official_url="https://icpc.global/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
            CompetitionInfo(
                competition_id="competition_challenge_cup",
                name="挑战杯大学生课外学术科技作品竞赛",
                organizer="共青团中央、中国科协、教育部等单位",
                category="创新创业类",
                tracks=["自然科学类", "科技发明制作", "哲学社会科学类"],
                registration_time="以当届官方通知为准",
                participant_requirements=(
                    "高校学生团队或个人参赛，具体要求以官方通知为准。"
                ),
                work_requirements="提交学术科技作品、研究报告、证明材料和答辩材料。",
                official_url="https://www.tiaozhanbei.net/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
            CompetitionInfo(
                competition_id="competition_service_outsourcing",
                name="中国大学生服务外包创新创业大赛",
                organizer="教育部、商务部等相关单位指导",
                category="工程开发类",
                tracks=["企业命题", "创业实践", "软件服务"],
                registration_time="以当年官方通知为准",
                participant_requirements="高校学生组队参赛，命题和资格以官方通知为准。",
                work_requirements="围绕命题提交解决方案、系统原型、演示视频和文档。",
                official_url="https://www.fwwb.org.cn/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
            CompetitionInfo(
                competition_id="competition_ai_challenge",
                name="人工智能创新挑战赛",
                organizer="赛事主办单位或产业平台",
                category="AI 类",
                tracks=["机器学习", "智能应用", "行业算法"],
                registration_time="以对应赛事官方通知为准",
                participant_requirements=(
                    "学生或团队按赛题要求报名，数据使用规则以官方说明为准。"
                ),
                work_requirements="提交模型方案、实验结果、代码说明和应用展示。",
                official_url="https://www.datafountain.cn/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
            CompetitionInfo(
                competition_id="competition_data_mining",
                name="数据挖掘与大数据挑战赛",
                organizer="高校、学会或产业数据竞赛平台",
                category="AI 类",
                tracks=["数据分析", "预测建模", "大数据应用"],
                registration_time="以具体赛题官方通知为准",
                participant_requirements=(
                    "按赛题平台注册参赛，团队人数和数据规则以官方说明为准。"
                ),
                work_requirements="提交预测结果、方法报告、代码说明和复现实验记录。",
                official_url="https://www.datafountain.cn/",
                updated_at=self.competition_updated_at,
                source_note=self.competition_source_note,
            ),
        ]

        return CompetitionCatalogResponse(
            total=len(competitions),
            updated_at=self.competition_updated_at,
            competitions=competitions,
        )

    def recommend_team(self, payload: TeamRecommendRequest) -> TeamRecommendResponse:
        return TeamRecommendResponse(
            requester_id=payload.student_id,
            project_goal=payload.project_goal,
            candidates=[
                TeamCandidate(
                    student_id="student_002",
                    name="陈星然",
                    role="前端与交互",
                    match_score=86,
                    complement="补足工作台界面、演示流程和移动端适配。",
                    evidence=["课程项目中负责过 React 页面", "表达材料完成度高"],
                ),
                TeamCandidate(
                    student_id="student_003",
                    name="周明远",
                    role="算法与评测",
                    match_score=81,
                    complement="补足代码分析规则、评测样例和算法竞赛路径。",
                    evidence=["算法专题训练稳定", "能整理测试用例"],
                ),
                TeamCandidate(
                    student_id="student_004",
                    name="沈知夏",
                    role="产品与答辩",
                    match_score=79,
                    complement="补足需求表达、场景材料和比赛答辩结构。",
                    evidence=["项目报告结构清晰", "擅长用户场景梳理"],
                ),
            ],
            collaboration_tips=[
                "先固定一条演示主线：学生提交作业 -> 系统分析 -> 教师看板 -> 学生成长建议。",
                "每周保留一次项目复盘，记录完成内容、阻塞和下周任务。",
                "接口、页面和演示数据同时推进，避免答辩前只剩单点功能。",
            ],
        )

    def create_team_request(self, payload: TeamRequestCreate) -> TeamRequestCard:
        return TeamRequestCard(
            team_request_id=f"team_req_{payload.student_id}_ai_app",
            student_id=payload.student_id,
            competition_name=payload.competition_name,
            project_direction=payload.project_direction,
            missing_roles=payload.missing_roles,
            expected_skills=payload.expected_skills,
            weekly_hours=payload.weekly_hours,
            communication=payload.communication,
            team_status_enabled=payload.team_status_enabled,
            contact_visible=False,
            status="已发布" if payload.team_status_enabled else "仅保存草稿",
            created_at=self.team_created_at,
        )

    def get_team_pool_status(self, student_id: str) -> TeamPoolStatus:
        return TeamPoolStatus(
            student_id=student_id,
            team_status_enabled=True,
            contact_visible=False,
            visibility_note="已进入推荐池；联系方式默认不公开，需学生主动提供。",
        )
