'use client'

import { useEffect, useRef, useState } from 'react'

// This component will wrap the Actual Budget React application
// and integrate it into the jane-ui framework

interface ActualAppProps {
  className?: string
}

export default function ActualApp({ className = '' }: ActualAppProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [isInitialized, setIsInitialized] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    const initializeActualApp = async () => {
      try {
        if (!containerRef.current || !mounted) return

        // In a real implementation, we would dynamically import and initialize
        // the actual Actual Budget React application here
        // For now, we'll create a placeholder that maintains the expected interface
        
        // Simulate initialization delay
        await new Promise(resolve => setTimeout(resolve, 500))

        if (!mounted) return

        // Create the actual app container
        const appContainer = document.createElement('div')
        appContainer.id = 'actual-budget-app'
        appContainer.className = 'w-full h-full'
        appContainer.innerHTML = `
          <div class="w-full h-full bg-white dark:bg-gray-900">
            <div class="h-full flex">
              <!-- Sidebar placeholder -->
              <div class="w-64 bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
                <div class="p-4 border-b border-gray-200 dark:border-gray-700">
                  <h1 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Actual Budget</h1>
                  <p class="text-sm text-gray-600 dark:text-gray-300">Personal Finance</p>
                </div>
                <nav class="flex-1 p-4 space-y-2">
                  <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100">
                    Budget
                  </a>
                  <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    Accounts
                  </a>
                  <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    Payees
                  </a>
                  <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    Rules
                  </a>
                  <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    Reports
                  </a>
                  <a href="#" class="block px-3 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
                    Settings
                  </a>
                </nav>
              </div>

              <!-- Main content area -->
              <div class="flex-1 flex flex-col">
                <!-- Top bar -->
                <div class="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 px-6 py-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Budget Overview</h2>
                      <p class="text-sm text-gray-600 dark:text-gray-300">December 2024</p>
                    </div>
                    <div class="flex items-center space-x-4">
                      <select class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100">
                        <option>This Month</option>
                        <option>Last Month</option>
                        <option>Year to Date</option>
                      </select>
                      <button class="px-4 py-2 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700 transition-colors">
                        Add Transaction
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Budget content -->
                <div class="flex-1 p-6 bg-gray-50 dark:bg-gray-900 overflow-auto">
                  <!-- Summary cards -->
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                      <div class="flex items-center">
                        <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                          <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                          </svg>
                        </div>
                        <div class="ml-4">
                          <p class="text-sm text-gray-600 dark:text-gray-400">Income</p>
                          <p class="text-2xl font-semibold text-gray-900 dark:text-gray-100">$5,200</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                      <div class="flex items-center">
                        <div class="p-2 bg-red-100 dark:bg-red-900 rounded-lg">
                          <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path>
                          </svg>
                        </div>
                        <div class="ml-4">
                          <p class="text-sm text-gray-600 dark:text-gray-400">Expenses</p>
                          <p class="text-2xl font-semibold text-gray-900 dark:text-gray-100">$4,650</p>
                        </div>
                      </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                      <div class="flex items-center">
                        <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                          <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                          </svg>
                        </div>
                        <div class="ml-4">
                          <p class="text-sm text-gray-600 dark:text-gray-400">Remaining</p>
                          <p class="text-2xl font-semibold text-green-600 dark:text-green-400">$550</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Budget categories -->
                  <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
                    <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                      <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Budget Categories</h3>
                    </div>
                    <div class="p-6">
                      <div class="overflow-x-auto">
                        <table class="min-w-full">
                          <thead>
                            <tr class="border-b border-gray-200 dark:border-gray-700">
                              <th class="text-left py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">Category</th>
                              <th class="text-right py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">Budgeted</th>
                              <th class="text-right py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">Spent</th>
                              <th class="text-right py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">Remaining</th>
                            </tr>
                          </thead>
                          <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                            <tr>
                              <td class="py-3 px-4 text-sm text-gray-900 dark:text-gray-100">🏠 Housing</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$1,800</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$1,750</td>
                              <td class="py-3 px-4 text-sm text-right text-green-600 dark:text-green-400">$50</td>
                            </tr>
                            <tr>
                              <td class="py-3 px-4 text-sm text-gray-900 dark:text-gray-100">🍕 Food</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$600</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$580</td>
                              <td class="py-3 px-4 text-sm text-right text-green-600 dark:text-green-400">$20</td>
                            </tr>
                            <tr>
                              <td class="py-3 px-4 text-sm text-gray-900 dark:text-gray-100">🚗 Transportation</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$400</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$350</td>
                              <td class="py-3 px-4 text-sm text-right text-green-600 dark:text-green-400">$50</td>
                            </tr>
                            <tr>
                              <td class="py-3 px-4 text-sm text-gray-900 dark:text-gray-100">🎮 Entertainment</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$200</td>
                              <td class="py-3 px-4 text-sm text-right text-gray-900 dark:text-gray-100">$180</td>
                              <td class="py-3 px-4 text-sm text-right text-green-600 dark:text-green-400">$20</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `

        containerRef.current.appendChild(appContainer)
        setIsInitialized(true)

      } catch (err) {
        console.error('Failed to initialize Actual Budget app:', err)
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to initialize application')
        }
      }
    }

    initializeActualApp()

    return () => {
      mounted = false
    }
  }, [])

  if (error) {
    return (
      <div className={`w-full h-full flex items-center justify-center bg-red-50 dark:bg-red-900/20 ${className}`}>
        <div className="text-center max-w-md p-6">
          <div className="text-red-600 dark:text-red-400 text-4xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-red-900 dark:text-red-100 mb-2">
            Application Error
          </h2>
          <p className="text-red-700 dark:text-red-300 mb-4 text-sm">
            {error}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-red-600 text-white rounded-md text-sm hover:bg-red-700 transition-colors"
          >
            Reload Application
          </button>
        </div>
      </div>
    )
  }

  return (
    <div 
      ref={containerRef}
      className={`w-full h-full ${className}`}
      style={{ minHeight: '100vh' }}
    />
  )
}