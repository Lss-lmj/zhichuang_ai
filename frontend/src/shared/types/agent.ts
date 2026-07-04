export type AgentCitation = {
  title: string;
  source_type: string;
  snippet: string;
};

export type ChatResponse = {
  answer: string;
  citations: AgentCitation[];
  ai_generated: boolean;
};
