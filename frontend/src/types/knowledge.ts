export interface KnowledgeBase {
  id: number
  name: string
  description: string
  source_type: string
  content: string
  tags: string[]
  created_at: string
  updated_at: string
  created_by: number
}

export interface KnowledgeQuery {
  query: string
  top_k: number
  threshold: number
}

export interface KnowledgeSearchResult {
  id: number
  content: string
  similarity: number
  metadata: Record<string, any>
}