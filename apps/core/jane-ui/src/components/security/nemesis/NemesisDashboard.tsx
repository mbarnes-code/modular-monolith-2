'use client'

import { useEffect, useRef, useState } from 'react'

// This component will wrap the Nemesis Security Platform React application
// and integrate it into the jane-ui framework

interface NemesisDashboardProps {
  className?: string
}

export default function NemesisDashboard({ className = '' }: NemesisDashboardProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [isInitialized, setIsInitialized] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true

    const initializeNemesisApp = async () => {
      try {
        if (!containerRef.current || !mounted) return

        // In a real implementation, we would dynamically import and initialize
        // the actual Nemesis React application here
        // For now, we'll create a functional dashboard interface
        
        // Simulate initialization delay
        await new Promise(resolve => setTimeout(resolve, 500))

        if (!mounted) return

        // Create the nemesis dashboard container
        const dashboardContainer = document.createElement('div')
        dashboardContainer.id = 'nemesis-dashboard'
        dashboardContainer.className = 'w-full h-full'
        dashboardContainer.innerHTML = `
          <div class="w-full h-full bg-gray-50 dark:bg-gray-900">
            <div class="p-6">
              <!-- Header -->
              <div class="mb-6">
                <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">
                  🛡️ Nemesis Security Dashboard
                </h1>
                <p class="text-gray-600 dark:text-gray-300">
                  Advanced threat analysis and file enrichment platform
                </p>
              </div>

              <!-- Status Cards -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                  <div class="flex items-center">
                    <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
                      <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                    </div>
                    <div class="ml-4">
                      <p class="text-sm text-gray-600 dark:text-gray-400">Files Analyzed</p>
                      <p class="text-2xl font-semibold text-gray-900 dark:text-gray-100">2,847</p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                  <div class="flex items-center">
                    <div class="p-2 bg-red-100 dark:bg-red-900 rounded-lg">
                      <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                      </svg>
                    </div>
                    <div class="ml-4">
                      <p class="text-sm text-gray-600 dark:text-gray-400">Threats Detected</p>
                      <p class="text-2xl font-semibold text-gray-900 dark:text-gray-100">23</p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                  <div class="flex items-center">
                    <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg">
                      <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                      </svg>
                    </div>
                    <div class="ml-4">
                      <p class="text-sm text-gray-600 dark:text-gray-400">Clean Files</p>
                      <p class="text-2xl font-semibold text-gray-900 dark:text-gray-100">2,824</p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                  <div class="flex items-center">
                    <div class="p-2 bg-purple-100 dark:bg-purple-900 rounded-lg">
                      <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                      </svg>
                    </div>
                    <div class="ml-4">
                      <p class="text-sm text-gray-600 dark:text-gray-400">Processing</p>
                      <p class="text-2xl font-semibold text-gray-900 dark:text-gray-100">12</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Main Content Grid -->
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Recent Analysis -->
                <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-lg shadow">
                  <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                    <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Recent Analysis</h3>
                  </div>
                  <div class="p-6">
                    <div class="overflow-x-auto">
                      <table class="min-w-full">
                        <thead>
                          <tr class="border-b border-gray-200 dark:border-gray-700">
                            <th class="text-left py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">File</th>
                            <th class="text-left py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">Status</th>
                            <th class="text-left py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">Risk</th>
                            <th class="text-left py-3 px-4 text-sm font-medium text-gray-900 dark:text-gray-100">Time</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                          <tr>
                            <td class="py-3 px-4 text-sm">
                              <div class="flex items-center">
                                <div class="w-8 h-8 bg-gray-200 dark:bg-gray-600 rounded flex items-center justify-center mr-3">
                                  <span class="text-xs font-medium">EXE</span>
                                </div>
                                <span class="text-gray-900 dark:text-gray-100">suspicious.exe</span>
                              </div>
                            </td>
                            <td class="py-3 px-4 text-sm">
                              <span class="px-2 py-1 text-xs bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-full">Threat Detected</span>
                            </td>
                            <td class="py-3 px-4 text-sm">
                              <span class="text-red-600 dark:text-red-400 font-medium">High</span>
                            </td>
                            <td class="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">2 mins ago</td>
                          </tr>
                          <tr>
                            <td class="py-3 px-4 text-sm">
                              <div class="flex items-center">
                                <div class="w-8 h-8 bg-gray-200 dark:bg-gray-600 rounded flex items-center justify-center mr-3">
                                  <span class="text-xs font-medium">PDF</span>
                                </div>
                                <span class="text-gray-900 dark:text-gray-100">document.pdf</span>
                              </div>
                            </td>
                            <td class="py-3 px-4 text-sm">
                              <span class="px-2 py-1 text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full">Clean</span>
                            </td>
                            <td class="py-3 px-4 text-sm">
                              <span class="text-green-600 dark:text-green-400 font-medium">Low</span>
                            </td>
                            <td class="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">5 mins ago</td>
                          </tr>
                          <tr>
                            <td class="py-3 px-4 text-sm">
                              <div class="flex items-center">
                                <div class="w-8 h-8 bg-gray-200 dark:bg-gray-600 rounded flex items-center justify-center mr-3">
                                  <span class="text-xs font-medium">ZIP</span>
                                </div>
                                <span class="text-gray-900 dark:text-gray-100">archive.zip</span>
                              </div>
                            </td>
                            <td class="py-3 px-4 text-sm">
                              <span class="px-2 py-1 text-xs bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded-full">Suspicious</span>
                            </td>
                            <td class="py-3 px-4 text-sm">
                              <span class="text-yellow-600 dark:text-yellow-400 font-medium">Medium</span>
                            </td>
                            <td class="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">12 mins ago</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>

                <!-- Quick Actions -->
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
                  <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                    <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Quick Actions</h3>
                  </div>
                  <div class="p-6 space-y-4">
                    <button class="w-full flex items-center justify-center px-4 py-3 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                      </svg>
                      Upload File
                    </button>
                    
                    <button class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                      </svg>
                      Search Files
                    </button>
                    
                    <button class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                      </svg>
                      View Reports
                    </button>
                    
                    <button class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                      </svg>
                      Settings
                    </button>
                  </div>
                </div>
              </div>

              <!-- Threat Intelligence Feed -->
              <div class="mt-6 bg-white dark:bg-gray-800 rounded-lg shadow">
                <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100">Threat Intelligence Feed</h3>
                </div>
                <div class="p-6">
                  <div class="space-y-4">
                    <div class="flex items-start space-x-3 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                      <div class="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                      <div>
                        <p class="text-sm font-medium text-gray-900 dark:text-gray-100">New malware campaign detected</p>
                        <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">APT group targeting financial institutions - 15 minutes ago</p>
                      </div>
                    </div>
                    
                    <div class="flex items-start space-x-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                      <div class="w-2 h-2 bg-yellow-500 rounded-full mt-2"></div>
                      <div>
                        <p class="text-sm font-medium text-gray-900 dark:text-gray-100">CVE-2024-1234 actively exploited</p>
                        <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">Critical vulnerability in popular software - 1 hour ago</p>
                      </div>
                    </div>
                    
                    <div class="flex items-start space-x-3 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                      <div class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                      <div>
                        <p class="text-sm font-medium text-gray-900 dark:text-gray-100">YARA rules updated</p>
                        <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">New detection rules for recent threats added - 2 hours ago</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `

        containerRef.current.appendChild(dashboardContainer)
        setIsInitialized(true)

      } catch (err) {
        console.error('Failed to initialize Nemesis Dashboard:', err)
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to initialize dashboard')
        }
      }
    }

    initializeNemesisApp()

    return () => {
      mounted = false
    }
  }, [])

  if (error) {
    return (
      <div className={`w-full h-full flex items-center justify-center bg-red-50 dark:bg-red-900/20 ${className}`}>
        <div className="text-center max-w-md p-6">
          <div className="text-red-600 dark:text-red-400 text-4xl mb-4">🛡️</div>
          <h2 className="text-xl font-semibold text-red-900 dark:text-red-100 mb-2">
            Security Dashboard Error
          </h2>
          <p className="text-red-700 dark:text-red-300 mb-4 text-sm">
            {error}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-red-600 text-white rounded-md text-sm hover:bg-red-700 transition-colors"
          >
            Reload Dashboard
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