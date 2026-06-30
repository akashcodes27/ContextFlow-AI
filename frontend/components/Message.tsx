'use client'

interface MessageProps {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export default function Message({ role, content, timestamp }: MessageProps) {
  const isUser = role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fadeIn`}>
      <div
        className={`max-w-[80%] px-4 py-3 rounded-2xl ${
          isUser
            ? 'bg-accent text-white rounded-br-sm'
            : 'bg-tertiary text-primary rounded-bl-sm'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">{content}</div>
        {timestamp && (
          <div className={`text-xs mt-1 ${isUser ? 'text-white/60' : 'text-muted'}`}>
            {new Date(timestamp).toLocaleTimeString()}
          </div>
        )}
      </div>
    </div>
  )
}