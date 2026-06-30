export interface User {
  id: string
  email: string
  full_name: string | null
  is_active: boolean
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  created_at: string
}

export interface ChatResponse {
  query: string
  response: string
  sources: Array<{
    content: string
    metadata: Record<string, any>
  }>
}

export interface AuthResponse {
  access_token: string
  token_type: string
}