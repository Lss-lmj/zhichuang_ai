export type KnowledgeDocument = {
  document_id: string;
  title: string;
  source_type: string;
  path: string;
  tags: string[];
  chunk_count: number;
  status: string;
  updated_at: string;
};

export type KnowledgeDocumentsResponse = {
  total: number;
  documents: KnowledgeDocument[];
};

export type KnowledgeSearchResult = {
  title: string;
  source_type: string;
  path: string;
  snippet: string;
  score: number;
  tags: string[];
};

export type KnowledgeSearchResponse = {
  query: string;
  total: number;
  results: KnowledgeSearchResult[];
};
