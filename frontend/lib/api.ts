const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('access_token')
  
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  }    

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  // Merge with any custom headers from options
  if (options.headers) {   
    const customHeaders = options.headers as Record<string, string>
    Object.assign(headers, customHeaders)
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))
    throw new Error(error.detail || `HTTP error ${response.status}`)
  }

  return response.json()
}

export const api = {
  auth: {
    register: (email: string, password: string, full_name?: string) =>
      apiRequest<{ id: string; email: string; full_name: string | null }>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email, password, full_name }),
      }),
    
    login: (email: string, password: string) =>
      apiRequest<{ access_token: string; token_type: string }>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      }),
    
    me: () =>
      apiRequest<{ id: string; email: string; full_name: string | null; is_active: boolean }>('/auth/me', {
        method: 'GET',
      }),
  },

  chat: {
    send: (query: string, user_id: string) =>
      apiRequest<{ query: string; response: string; sources: Array<{ content: string; metadata: Record<string, any> }> }>('/chat', {
        method: 'POST',
        body: JSON.stringify({ query, user_id }),
      }),
  },

  documents: {
    upload: (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      
      const token = localStorage.getItem('access_token')
      
      const headers: Record<string, string> = {}
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
      
      return fetch(`${API_URL}/documents/upload`, {
        method: 'POST',
        headers,
        body: formData,
      }).then(async (res) => {
        if (!res.ok) {
          const error = await res.json().catch(() => ({}))
          throw new Error(error.detail || 'Upload failed')
        }
        return res.json() as Promise<{ message: string; document_id: string; filename: string; chunks: number }>
      })
    },
  },
}