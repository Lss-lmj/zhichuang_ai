export type CapabilityDimension = {
  dimension: string;
  score: number;
  confidence: number;
  summary: string;
  evidence: string[];
};

export type GrowthProfile = {
  student_id: string;
  student_name: string;
  target_path: string;
  generated_at: string;
  dimensions: CapabilityDimension[];
  strengths: string[];
  risks: string[];
  next_actions: string[];
  ai_generated: boolean;
};

export type PlanTask = {
  week: number;
  title: string;
  outcome: string;
  resources: string[];
};

export type LearningPlan = {
  plan_id: string;
  student_id: string;
  goal: string;
  weeks: number;
  overview: string;
  tasks: PlanTask[];
  checkpoints: string[];
  ai_generated: boolean;
};

export type CompetitionRecommendation = {
  name: string;
  category: string;
  match_score: number;
  reason: string;
  preparation: string[];
  risk: string;
};

export type CompetitionRecommendResponse = {
  student_id: string;
  target: string;
  recommendations: CompetitionRecommendation[];
  ai_generated: boolean;
};

export type TeamCandidate = {
  student_id: string;
  name: string;
  role: string;
  match_score: number;
  complement: string;
  evidence: string[];
};

export type TeamRecommendResponse = {
  requester_id: string;
  project_goal: string;
  candidates: TeamCandidate[];
  collaboration_tips: string[];
  ai_generated: boolean;
};
