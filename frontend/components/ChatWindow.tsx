'use client'

import { useState, useRef, useEffect } from 'react'
import Message from './Message'
import UploadButton from './UploadButton'
import { api } from '@/lib/api'
import { getToken } from '@/lib/auth'

interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

interface ChatWindowProps {
  userId: string
}

export default function ChatWindow({ userId }: ChatWindowProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'welcome',
      role: 'assistant',
      content: 'Hello! I\'m ContextFlow AI. Upload documents and ask me anything about them.',
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`
    }
  }, [input])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.chat.send(input, userId)
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (err: any) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: `Error: ${err.message || 'Something went wrong'}`,
        timestamp: new Date().toISOString(),
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleUploadComplete = (result: any) => {
    setUploadStatus(`✅ Uploaded: ${result.filename} (${result.chunks} chunks)`)
    setTimeout(() => setUploadStatus(null), 5000)
  }

  const handleUploadError = (error: string) => {
    setUploadStatus(`❌ Error: ${error}`)
    setTimeout(() => setUploadStatus(null), 5000)
  }

  return (
    <div className="flex flex-col h-full bg-primary rounded-lg overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-border bg-secondary/50">
        <div className="flex items-center gap-3">
          <div className="w-3 h-3 rounded-full bg-accent animate-pulse"></div>
          <span className="font-semibold text-primary">ContextFlow AI</span>
        </div>
        <div className="flex items-center gap-3">
          <UploadButton
            onUploadComplete={handleUploadComplete}
            onUploadError={handleUploadError}
          />
          <button
            onClick={() => {
              localStorage.removeItem('access_token')
              window.location.href = '/login'
            }}
            className="text-sm text-secondary hover:text-primary transition-colors"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Upload Status */}
      {uploadStatus && (
        <div className={`px-6 py-2 text-sm ${
          uploadStatus.startsWith('✅') ? 'text-success' : 'text-error'
        } bg-secondary/30 border-b border-border`}>
          {uploadStatus}
        </div>
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        {messages.map((msg) => (
          <Message
            key={msg.id}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
          />
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-tertiary px-4 py-3 rounded-2xl rounded-bl-sm">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-muted rounded-full animate-pulse"></span>
                <span className="w-2 h-2 bg-muted rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></span>
                <span className="w-2 h-2 bg-muted rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-border bg-secondary/30 p-4">
        <form onSubmit={handleSubmit} className="flex gap-3 items-end">
          <div className="flex-1 relative">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about your documents..."
              className="input-field w-full px-4 py-3 bg-secondary border border-border rounded-xl text-primary placeholder-muted resize-none focus:outline-none focus:border-accent focus:ring-1 focus:ring-accent transition-colors"
              rows={1}
              disabled={loading}
            />
          </div>
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className={`p-3 rounded-xl transition-all ${
              input.trim() && !loading
                ? 'bg-accent hover:bg-accent-hover text-white'
                : 'bg-tertiary text-muted cursor-not-allowed'
            }`}
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  )
}