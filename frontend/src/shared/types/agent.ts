export type AgentCitation = {
  title: string;
  source_type: string;
  path: string;
  updated_at: string;
  snippet: string;
};

export type ChatMessage = {
  role: "user" | "assistant" | string;
  content: string;
};

export type ChatResponse = {
  session_id: string;
  answer: string;
  citations: AgentCitation[];
  context_summary: string;
  suggested_next_questions: string[];
  is_uncertain: boolean;
  retrieval_status: "matched" | "no_match" | string;
  ai_generated: boolean;
};
