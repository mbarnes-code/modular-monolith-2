'use client';
/* eslint-disable no-undef */

import React, { useEffect, useState } from 'react';
import MobileNavigation from './MobileNavigation';

interface MobileLayoutProps {
  children: React.ReactNode;
  currentDomain?: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  className?: string;
}

/**
 * Mobile Layout Component
 * Provides consistent mobile layout with executive function accommodations
 * Includes bottom navigation and gesture support for ADHD/autism users
 */
export default function MobileLayout({
  children,
  currentDomain,
  className = ''
}: MobileLayoutProps) {
  const [isMobile, setIsMobile] = useState(false);
  const [showBottomNav, setShowBottomNav] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  // Detect mobile viewport
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);

    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Hide/show bottom navigation on scroll (ADHD-friendly)
  useEffect(() => {
    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      
      // Show nav when scrolling up, hide when scrolling down
      if (currentScrollY < lastScrollY || currentScrollY < 50) {
        setShowBottomNav(true);
      } else if (currentScrollY > lastScrollY && currentScrollY > 100) {
        setShowBottomNav(false);
      }
      
      setLastScrollY(currentScrollY);
    };

    if (isMobile) {
      window.addEventListener('scroll', handleScroll, { passive: true });
      return () => window.removeEventListener('scroll', handleScroll);
    }
  }, [isMobile, lastScrollY]);

  const quickActions = [
    {
      id: 'dashboard',
      icon: '🏠',
      label: 'Dashboard',
      path: '/',
      active: !currentDomain
    },
    {
      id: 'security',
      icon: '🔒',
      label: 'Security',
      path: '/security',
      active: currentDomain === 'security'
    },
    {
      id: 'productivity',
      icon: '📋',
      label: 'Tasks',
      path: '/productivity',
      active: currentDomain === 'productivity'
    },
    {
      id: 'mtg',
      icon: '🎴',
      label: 'MTG',
      path: '/mtg',
      active: currentDomain === 'mtg'
    },
    {
      id: 'infrastructure',
      icon: '⚙️',
      label: 'System',
      path: '/infrastructure',
      active: currentDomain === 'infrastructure'
    }
  ];

  if (!isMobile) {
    // Desktop layout - just render children
    return <div className={className}>{children}</div>;
  }

  return (
    <div className={`min-h-screen bg-gray-50 ${className}`}>
      {/* Top Navigation */}
      <MobileNavigation currentDomain={currentDomain} />

      {/* Main Content */}
      <main className="pb-20">
        {children}
      </main>

      {/* Bottom Navigation - Fixed */}
      <nav 
        className={`
          fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 
          transition-transform duration-300 ease-in-out z-50
          ${showBottomNav ? 'translate-y-0' : 'translate-y-full'}
        `}
      >
        <div className="grid grid-cols-5 h-16">
          {quickActions.map((action) => (
            <button
              key={action.id}
              className={`
                flex flex-col items-center justify-center space-y-1
                transition-all duration-150 active:bg-gray-100
                focus:outline-none focus:bg-gray-100
                ${action.active 
                  ? 'text-blue-600 bg-blue-50' 
                  : 'text-gray-600 hover:text-gray-900'
                }
              `}
              onClick={() => {
                // In real implementation, navigate to path
                console.log(`Navigate to ${action.path}`);
              }}
            >
              <span className="text-xl">{action.icon}</span>
              <span className="text-xs font-medium">{action.label}</span>
              {action.active && (
                <div className="w-4 h-0.5 bg-blue-600 rounded-full"></div>
              )}
            </button>
          ))}
        </div>
      </nav>

      {/* Floating Action Button for AI Assistant */}
      <button
        className="fixed bottom-20 right-4 w-14 h-14 bg-blue-600 text-white rounded-full
                   shadow-lg hover:bg-blue-700 active:bg-blue-800 
                   transition-all duration-150 flex items-center justify-center
                   focus:outline-none focus:ring-4 focus:ring-blue-300 focus:ring-opacity-75"
        onClick={() => {
          // In real implementation, open AI assistant
          console.log('Open AI assistant');
        }}
        aria-label="Open AI Assistant"
      >
        <span className="text-xl">🤖</span>
      </button>
    </div>
  );
}