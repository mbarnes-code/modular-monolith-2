/**
 * Sidebar Navigation Component
 * 
 * Provides persistent navigation for executive function support:
 * - Always-visible domain access for context preservation
 * - Tool quick access for reduced cognitive load
 * - Status indicators for system awareness
 * - Collapsible design for flexibility
 */

'use client';

import {
    Activity,
    Briefcase,
    ChevronLeft,
    ChevronRight,
    Gamepad2,
    Heart,
    HelpCircle,
    Home,
    Server,
    Settings,
    Shield
} from 'lucide-react';
import React, { useState } from 'react';

interface Domain {
  name: string;
  display_name: string;
  tool_count: number;
  active_tools: number;
  color: string;
  health_percentage?: number;
}

interface Tool {
  id: string;
  name: string;
  display_name: string;
  domain: string;
  status: 'active' | 'inactive' | 'maintenance';
  is_favorite?: boolean;
}

interface SidebarNavigationProps {
  domains: Domain[];
  favoriteTools?: Tool[];
  currentDomain?: string | null;
  onDomainSelect: (domain: string | null) => void;
  onToolSelect?: (tool: Tool) => void;
  executiveFunctionEnabled: boolean;
  className?: string;
}

const getDomainIcon = (domainName: string) => {
  switch (domainName.toLowerCase()) {
    case 'security':
      return Shield;
    case 'productivity':
      return Briefcase;
    case 'mtg':
      return Gamepad2;
    case 'infrastructure':
      return Server;
    default:
      return Activity;
  }
};

export const SidebarNavigation: React.FC<SidebarNavigationProps> = ({
  domains,
  favoriteTools = [],
  currentDomain,
  onDomainSelect,
  onToolSelect,
  executiveFunctionEnabled,
  className = ''
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  const handleSectionToggle = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const sidebarWidth = isCollapsed ? 'w-16' : 'w-64';

  return (
    <aside 
      className={`
        sidebar-navigation 
        ${sidebarWidth}
        bg-white 
        border-r 
        border-gray-200 
        flex 
        flex-col 
        transition-all 
        duration-300 
        ${executiveFunctionEnabled ? 'transform-gpu' : ''}
        ${className}
      `}
      role="navigation"
      aria-label="Domain and tool navigation"
    >
      {/* Sidebar Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        {!isCollapsed && (
          <h2 className="text-lg font-semibold text-gray-900">Navigation</h2>
        )}
        <button
          onClick={() => setIsCollapsed(!isCollapsed)}
          className="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Navigation Content */}
      <div className="flex-1 overflow-y-auto py-4">
        {/* Dashboard Home */}
        <div className="px-4 mb-6">
          <button
            onClick={() => onDomainSelect(null)}
            className={`
              w-full flex items-center space-x-3 px-3 py-3 rounded-lg transition-colors text-left
              focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
              ${!currentDomain 
                ? 'bg-blue-100 text-blue-700 font-medium' 
                : 'text-gray-700 hover:bg-gray-50'
              }
            `}
            title={isCollapsed ? 'Dashboard Overview' : undefined}
          >
            <Home className="w-5 h-5 flex-shrink-0" />
            {!isCollapsed && (
              <div>
                <div className="font-medium">Dashboard</div>
                <div className="text-xs text-gray-500">Overview of all domains</div>
              </div>
            )}
          </button>
        </div>

        {/* Domain Navigation */}
        <div className="px-4 mb-6">
          {!isCollapsed && (
            <h3 className="text-sm font-medium text-gray-900 mb-3">Domains</h3>
          )}
          <div className="space-y-1">
            {domains.map((domain) => {
              const IconComponent = getDomainIcon(domain.name);
              const isActive = currentDomain === domain.name;
              const healthStatus = domain.health_percentage || 100;
              
              return (
                <div key={domain.name}>
                  <button
                    onClick={() => onDomainSelect(domain.name)}
                    className={`
                      w-full flex items-center space-x-3 px-3 py-3 rounded-lg transition-colors text-left
                      focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
                      ${isActive
                        ? 'text-white font-medium shadow-sm'
                        : 'text-gray-700 hover:bg-gray-50'
                      }
                    `}
                    style={isActive ? { backgroundColor: domain.color } : {}}
                    title={isCollapsed ? `${domain.display_name} - ${domain.tool_count} tools` : undefined}
                  >
                    <div className="flex items-center space-x-3 flex-1">
                      <IconComponent className="w-5 h-5 flex-shrink-0" />
                      {!isCollapsed && (
                        <div className="flex-1">
                          <div className="font-medium">{domain.display_name}</div>
                          <div className={`text-xs flex items-center space-x-2 ${
                            isActive ? 'text-white text-opacity-80' : 'text-gray-500'
                          }`}>
                            <span>{domain.tool_count} tools</span>
                            <span>•</span>
                            <span>{domain.active_tools} active</span>
                          </div>
                        </div>
                      )}
                    </div>
                    
                    {/* Health Indicator */}
                    {!isCollapsed && (
                      <div className="flex items-center space-x-1">
                        <Heart 
                          className={`w-4 h-4 ${
                            healthStatus >= 90 ? (isActive ? 'text-white' : 'text-green-500') :
                            healthStatus >= 70 ? (isActive ? 'text-white' : 'text-amber-500') :
                            (isActive ? 'text-white' : 'text-red-500')
                          }`}
                        />
                        <span className={`text-xs ${
                          isActive ? 'text-white text-opacity-80' : 'text-gray-500'
                        }`}>
                          {healthStatus}%
                        </span>
                      </div>
                    )}
                  </button>
                </div>
              );
            })}
          </div>
        </div>

        {/* Favorite Tools - Executive Function Quick Access */}
        {favoriteTools.length > 0 && !isCollapsed && (
          <div className="px-4 mb-6">
            <button
              onClick={() => handleSectionToggle('favorites')}
              className="flex items-center justify-between w-full text-sm font-medium text-gray-900 mb-3 hover:text-gray-700"
            >
              <span>Quick Access</span>
              <ChevronRight 
                className={`w-4 h-4 transition-transform ${
                  expandedSection === 'favorites' ? 'rotate-90' : ''
                }`}
              />
            </button>
            
            {expandedSection === 'favorites' && (
              <div className="space-y-1">
                {favoriteTools.slice(0, 5).map((tool) => (
                  <button
                    key={tool.id}
                    onClick={() => onToolSelect?.(tool)}
                    className="w-full flex items-center space-x-3 px-3 py-2 text-left text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <div className={`w-2 h-2 rounded-full ${
                      tool.status === 'active' ? 'bg-green-400' :
                      tool.status === 'maintenance' ? 'bg-amber-400' :
                      'bg-gray-400'
                    }`} />
                    <span className="truncate">{tool.display_name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* System Status - Executive Function Transparency */}
        {!isCollapsed && (
          <div className="px-4 mb-6">
            <button
              onClick={() => handleSectionToggle('status')}
              className="flex items-center justify-between w-full text-sm font-medium text-gray-900 mb-3 hover:text-gray-700"
            >
              <span>System Status</span>
              <ChevronRight 
                className={`w-4 h-4 transition-transform ${
                  expandedSection === 'status' ? 'rotate-90' : ''
                }`}
              />
            </button>
            
            {expandedSection === 'status' && (
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Total Tools</span>
                  <span className="font-medium">37</span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Active Tools</span>
                  <span className="font-medium text-green-600">
                    {domains.reduce((sum, d) => sum + d.active_tools, 0)}
                  </span>
                </div>
                <div className="flex items-center justify-between text-sm">
                  <span className="text-gray-600">Domains</span>
                  <span className="font-medium">{domains.length}</span>
                </div>
                
                {executiveFunctionEnabled && (
                  <div className="flex items-center space-x-2 text-xs text-green-600 pt-2 border-t border-gray-100">
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    <span>EF accommodations active</span>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Sidebar Footer */}
      <div className="border-t border-gray-200 p-4">
        <div className="space-y-1">
          <button
            className={`
              w-full flex items-center space-x-3 px-3 py-2 text-left text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors
              focus:outline-none focus:ring-2 focus:ring-blue-500
              ${isCollapsed ? 'justify-center' : ''}
            `}
            title={isCollapsed ? 'Settings' : undefined}
          >
            <Settings className="w-4 h-4 flex-shrink-0" />
            {!isCollapsed && <span>Settings</span>}
          </button>
          
          <button
            className={`
              w-full flex items-center space-x-3 px-3 py-2 text-left text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors
              focus:outline-none focus:ring-2 focus:ring-blue-500
              ${isCollapsed ? 'justify-center' : ''}
            `}
            title={isCollapsed ? 'Help' : undefined}
          >
            <HelpCircle className="w-4 h-4 flex-shrink-0" />
            {!isCollapsed && <span>Help</span>}
          </button>
        </div>
      </div>
    </aside>
  );
};