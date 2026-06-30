'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import ChatWindow from '@/components/ChatWindow'
import { isAuthenticated, getToken } from '@/lib/auth'
import { api } from '@/lib/api'

interface User {
  id: string
  email: string
  full_name: string | null
}

export default function ChatPage() {
  const router = useRouter()
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login')
      return
    }

    const fetchUser = async () => {
      try {
        const data = await api.auth.me()
        setUser(data)
      } catch (err) {
        localStorage.removeItem('access_token')
        router.push('/login')
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
  }, [router])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-pulse text-secondary">Loading...</div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-primary">
      <div className="container h-screen py-4">
        <div className="h-full card p-0 overflow-hidden">
          <ChatWindow userId={user.id} />
        </div>
      </div>
    </div>
  )
}