'use client'

import { useState, useRef } from 'react'
import { api } from '@/lib/api'

interface UploadButtonProps {
  onUploadComplete?: (result: any) => void
  onUploadError?: (error: string) => void
}

export default function UploadButton({ onUploadComplete, onUploadError }: UploadButtonProps) {
  const [uploading, setUploading] = useState(false)
  const [fileName, setFileName] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setFileName(file.name)
    setUploading(true)

    try {
      const result = await api.documents.upload(file)
      if (onUploadComplete) onUploadComplete(result)
      // Reset after success
      setTimeout(() => setFileName(null), 3000)
    } catch (err: any) {
      if (onUploadError) onUploadError(err.message || 'Upload failed')
    } finally {
      setUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  return (
    <div>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept=".pdf,.docx,.txt,.md,.markdown"
        className="hidden"
        id="file-upload"
      />
      <label
        htmlFor="file-upload"
        className={`btn-secondary inline-flex items-center gap-2 cursor-pointer ${
          uploading ? 'opacity-50 pointer-events-none' : ''
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
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
        {uploading ? 'Uploading...' : fileName || 'Upload Document'}
      </label>
    </div>
  )
}