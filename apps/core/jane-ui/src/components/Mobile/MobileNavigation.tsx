'use client';
/* eslint-disable no-undef */

import { useEffect, useState } from 'react';

interface MobileNavigationProps {
  currentDomain?: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  onDomainChange?: (domain: string) => void;
  className?: string;
}

/**
 * Mobile Navigation Component
 * ADHD/Autism-friendly mobile navigation with consistent patterns
 * Supports PWA and executive function accommodations
 */
export default function MobileNavigation({
  currentDomain,
  onDomainChange,
  className = ''
}: MobileNavigationProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [syncStatus, setSyncStatus] = useState<'online' | 'offline' | 'synced'>('online');

  // Domain configurations for 4-domain architecture
  const domains = [
    {
      id: 'security',
      name: 'Security',
      icon: '🔒',
      color: 'bg-red-600',
      tools: 13,
      description: 'Threat analysis and security tools'
    },
    {
      id: 'productivity',
      name: 'Productivity',
      icon: '📋',
      color: 'bg-blue-600',
      tools: 8,
      description: 'Task management and organization'
    },
    {
      id: 'mtg',
      name: 'MTG',
      icon: '🎴',
      color: 'bg-purple-600',
      tools: 4,
      description: 'Magic: The Gathering analysis'
    },
    {
      id: 'infrastructure',
      name: 'Infrastructure',
      icon: '⚙️',
      color: 'bg-green-600',
      tools: 12,
      description: 'System management and automation'
    }
  ];

  // Listen for sync status updates
  useEffect(() => {
    const handleSyncStatus = (event: CustomEvent) => {
      setSyncStatus(event.detail.status);
    };

    window.addEventListener('jane-sync-status', handleSyncStatus as EventListener);
    
    // Check localStorage for initial status
    const savedStatus = localStorage.getItem('jane-sync-status');
    if (savedStatus) {
      try {
        const { status } = JSON.parse(savedStatus);
        setSyncStatus(status);
      } catch (error) {
        console.warn('Failed to parse sync status:', error);
      }
    }

    return () => {
      window.removeEventListener('jane-sync-status', handleSyncStatus as EventListener);
    };
  }, []);

  const handleDomainSelect = (domainId: string) => {
    setIsMenuOpen(false);
    onDomainChange?.(domainId);
  };

  const getSyncStatusColor = () => {
    switch (syncStatus) {
      case 'online':
      case 'synced':
        return 'text-green-500';
      case 'offline':
        return 'text-yellow-500';
      default:
        return 'text-gray-500';
    }
  };

  const getSyncStatusIcon = () => {
    switch (syncStatus) {
      case 'online':
        return '🟢';
      case 'synced':
        return '✅';
      case 'offline':
        return '🟡';
      default:
        return '⚪';
    }
  };

  return (
    <nav className={`bg-white border-b border-gray-200 shadow-sm ${className}`}>
      {/* Mobile Header */}
      <div className="px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="text-2xl">🧠</div>
            <div>
              <h1 className="text-lg font-semibold text-gray-900">Jane Platform</h1>
              {currentDomain && (
                <p className="text-sm text-gray-600 capitalize">{currentDomain} Domain</p>
              )}
            </div>
          </div>

          {/* Status and Menu Button */}
          <div className="flex items-center space-x-3">
            {/* Sync Status Indicator */}
            <div 
              className={`flex items-center space-x-1 ${getSyncStatusColor()}`}
              data-jane-sync-status={syncStatus}
            >
              <span className="text-xs">{getSyncStatusIcon()}</span>
              <span className="text-xs font-medium capitalize">{syncStatus}</span>
            </div>

            {/* Menu Toggle Button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-lg text-gray-600 hover:text-gray-900 hover:bg-gray-100 
                         transition-colors duration-150 focus:outline-none focus:ring-2 
                         focus:ring-blue-500 focus:ring-offset-2"
              aria-label="Toggle navigation menu"
              aria-expanded={isMenuOpen}
            >
              <svg
                className={`w-6 h-6 transform transition-transform duration-200 ${
                  isMenuOpen ? 'rotate-90' : ''
                }`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d={isMenuOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'}
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      <div 
        className={`transition-all duration-300 ease-in-out overflow-hidden ${
          isMenuOpen ? 'max-h-screen opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="border-t border-gray-200 bg-gray-50">
          {/* Domain Navigation */}
          <div className="px-4 py-3">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Executive Function Domains</h3>
            <div className="grid grid-cols-1 gap-2">
              {domains.map((domain) => (
                <button
                  key={domain.id}
                  onClick={() => handleDomainSelect(domain.id)}
                  className={`
                    flex items-center space-x-3 w-full p-3 rounded-lg text-left
                    transition-all duration-150 focus:outline-none focus:ring-2 
                    focus:ring-blue-500 focus:ring-offset-2
                    ${currentDomain === domain.id
                      ? `${domain.color} text-white shadow-md`
                      : 'bg-white text-gray-900 hover:bg-gray-100 border border-gray-200'
                    }
                  `}
                >
                  <div className="text-2xl">{domain.icon}</div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-medium truncate">{domain.name}</h4>
                      <span className={`
                        text-xs px-2 py-1 rounded-full
                        ${currentDomain === domain.id
                          ? 'bg-white bg-opacity-20 text-white'
                          : 'bg-gray-100 text-gray-600'
                        }
                      `}>
                        {domain.tools} tools
                      </span>
                    </div>
                    <p className={`
                      text-xs mt-1 truncate
                      ${currentDomain === domain.id ? 'text-white text-opacity-90' : 'text-gray-600'}
                    `}>
                      {domain.description}
                    </p>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="px-4 py-3 border-t border-gray-200">
            <h3 className="text-sm font-medium text-gray-900 mb-3">Quick Actions</h3>
            <div className="grid grid-cols-2 gap-2">
              <button className="flex items-center justify-center space-x-2 p-3 bg-white rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors duration-150">
                <span>🎯</span>
                <span className="text-sm font-medium">AI Assistant</span>
              </button>
              <button className="flex items-center justify-center space-x-2 p-3 bg-white rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors duration-150">
                <span>📊</span>
                <span className="text-sm font-medium">Dashboard</span>
              </button>
              <button className="flex items-center justify-center space-x-2 p-3 bg-white rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors duration-150">
                <span>⚙️</span>
                <span className="text-sm font-medium">Settings</span>
              </button>
              <button className="flex items-center justify-center space-x-2 p-3 bg-white rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors duration-150">
                <span>📋</span>
                <span className="text-sm font-medium">Tasks</span>
              </button>
            </div>
          </div>

          {/* Executive Function Status */}
          <div className="px-4 py-3 border-t border-gray-200 bg-blue-50">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium text-gray-900">Platform Active</span>
              </div>
              <span className="text-xs text-gray-600">
                {new Date().toLocaleTimeString()}
              </span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}