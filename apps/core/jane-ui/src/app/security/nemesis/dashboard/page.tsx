'use client'

import dynamic from 'next/dynamic'
import { useEffect, useState } from 'react'

// Dynamically import the Nemesis React app to avoid SSR issues
const NemesisDashboardApp = dynamic(
  () => import('@/components/security/nemesis/NemesisDashboard'),
  { 
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-300">Loading Nemesis Dashboard...</p>
        </div>
      </div>
    )
  }
)

export default function NemesisDashboardPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Initialize Nemesis Dashboard
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-red-50 dark:bg-red-900/20">
        <div className="text-center max-w-md">
          <div className="text-red-600 dark:text-red-400 text-6xl mb-4">⚠️</div>
          <h1 className="text-2xl font-bold text-red-900 dark:text-red-100 mb-2">
            Failed to Load Nemesis Dashboard
          </h1>
          <p className="text-red-700 dark:text-red-300 mb-6">
            {error}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full h-screen flex flex-col">
      {/* Header with breadcrumbs */}
      <div className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-300">
            <a href="/security" className="hover:text-red-600 dark:hover:text-red-400">
              Security
            </a>
            <span>›</span>
            <a href="/security/nemesis" className="hover:text-red-600 dark:hover:text-red-400">
              Nemesis
            </a>
            <span>›</span>
            <span className="text-gray-900 dark:text-gray-100 font-medium">Dashboard</span>
          </div>
          
          {/* Quick action buttons */}
          <div className="flex items-center space-x-3">
            <a
              href="/security/nemesis/analysis"
              className="px-3 py-1.5 text-sm bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
            >
              Upload File
            </a>
            <a
              href="/security/nemesis/search"
              className="px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
            >
              Search
            </a>
          </div>
        </div>
      </div>

      {/* Main application container */}
      <div className="flex-1 relative">
        {isLoading ? (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-50 dark:bg-gray-900">
            <div className="text-center">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-red-600 mx-auto mb-6"></div>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-2">
                Loading Security Dashboard
              </h2>
              <p className="text-gray-600 dark:text-gray-300">
                Initializing threat analysis platform...
              </p>
            </div>
          </div>
        ) : (
          <div className="w-full h-full">
            <NemesisDashboardApp />
          </div>
        )}
      </div>
    </div>
  )
}