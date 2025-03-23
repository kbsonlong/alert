export interface AlertRule {
  id: number
  name: string
  description: string
  conditions: Record<string, any>
  severity: string
  enabled: boolean
  created_at: string
  updated_at: string
  created_by: number
}

export interface AlertRecord {
  id: number
  rule_id: number
  title: string
  content: string
  severity: string
  status: string
  source: string
  created_at: string
  updated_at: string
  handled_by: number
  handling_notes: string
}

export interface AnalysisRecord {
  id: number
  alert_id: number
  analysis_result: string
  suggestions: {
    suggestions: string[]
  }
  similar_alerts: {
    similar: string[]
  }
  created_at: string
  confirmed: boolean
}