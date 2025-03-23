export interface NotificationChannel {
  id: number
  name: string
  type: string
  config: Record<string, any>
  enabled: boolean
  created_at: string
  updated_at: string
}

export interface NotificationGroup {
  id: number
  name: string
  members: {
    members: Array<{
      name: string
      email: string
      phone?: string
    }>
  }
  channels: {
    channels: number[]
  }
  created_at: string
  updated_at: string
}

export interface NotificationTemplate {
  id: number
  name: string
  type: string
  content: string
  variables: {
    variables: string[]
  }
  language: string
  created_at: string
  updated_at: string
}