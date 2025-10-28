/**
 * Domain Navigation Component
 * 
 * Constitutional Requirements:
 * - Consistent interface patterns across all 4 domains
 * - Cognitive load reduction with clear visual hierarchy
 * - WCAG 2.1 AA compliance for accessibility
 * - ADHD/autism-friendly navigation with predictable behavior
 * - Context switching minimization with breadcrumbs and state preservation
 */

'use client';

import {
    ArrowLeft,
    Briefcase,
    ChevronRight,
    Gamepad2,
    Home,
    Menu,
    Search,
    Server,
    Settings,
    Shield,
    User,
    X
} from 'lucide-react';
import React, { useCallback, useMemo, useState } from 'react';

interface Domain {
  name: string;
  display_name: string;
  description: string;
  tool_count: number;
  active_tools: number;
  color: string;
  icon?: string;
}

interface NavigationProps {
  currentDomain?: string | null;
  currentPath?: string[];
  domains: Domain[];
  onDomainChange: (domain: string | null) => void;
  onPathChange: (path: string[]) => void;
  executiveFunctionEnabled: boolean;
  className?: string;
}

interface BreadcrumbProps {
  path: string[];
  onPathChange: (path: string[]) => void;
  executiveFunctionEnabled: boolean;
}

interface DomainMenuProps {
  domains: Domain[];
  currentDomain: string | null;
  onDomainSelect: (domain: string | null) => void;
  executiveFunctionEnabled: boolean;
  isOpen: boolean;
  onToggle: () => void;
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
      return Home;
  }
};

const Breadcrumb: React.FC<BreadcrumbProps> = ({
  path,
  onPathChange,
  executiveFunctionEnabled
}) => {
  const handleNavigate = useCallback((index: number) => {
    const newPath = path.slice(0, index + 1);
    onPathChange(newPath);
  }, [path, onPathChange]);

  if (path.length === 0) {
    return null;
  }

  return (
    <nav 
      aria-label="Breadcrumb navigation"
      className="flex items-center space-x-2 text-sm text-gray-600"
    >
      <button
        onClick={() => onPathChange([])}
        className="flex items-center space-x-1 hover:text-gray-900 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 rounded px-2 py-1"
        aria-label="Go to dashboard home"
      >
        <Home className="w-4 h-4" />
        <span>Dashboard</span>
      </button>

      {path.map((segment, index) => (
        <React.Fragment key={`${segment}-${index}`}>
          <ChevronRight className="w-4 h-4 text-gray-400" />
          <button
            onClick={() => handleNavigate(index)}
            className={`
              hover:text-gray-900 
              transition-colors 
              focus:outline-none 
              focus:ring-2 
              focus:ring-blue-500 
              focus:ring-opacity-50 
              rounded 
              px-2 
              py-1
              ${index === path.length - 1 ? 'text-gray-900 font-medium' : ''}
              ${executiveFunctionEnabled ? 'transform-gpu' : ''}
            `}
            aria-current={index === path.length - 1 ? 'page' : undefined}
          >
            <span className="capitalize">{segment}</span>
          </button>
        </React.Fragment>
      ))}
    </nav>
  );
};

const DomainMenu: React.FC<DomainMenuProps> = ({
  domains,
  currentDomain,
  onDomainSelect,
  executiveFunctionEnabled,
  isOpen,
  onToggle
}) => {
  const handleDomainSelect = useCallback((domainName: string | null) => {
    onDomainSelect(domainName);
    onToggle(); // Close menu after selection on mobile
  }, [onDomainSelect, onToggle]);

  return (
    <div className="relative">
      {/* Mobile Menu Toggle */}
      <button
        onClick={onToggle}
        className="md:hidden flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
        aria-label="Toggle domain menu"
        aria-expanded={isOpen}
      >
        {isOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        <span className="text-sm font-medium">Domains</span>
      </button>

      {/* Desktop Menu - Always Visible */}
      <nav className="hidden md:flex items-center space-x-1" role="navigation" aria-label="Domain navigation">
        {/* Dashboard Home */}
        <button
          onClick={() => handleDomainSelect(null)}
          className={`
            flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
            ${!currentDomain 
              ? 'bg-blue-100 text-blue-700 font-medium' 
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
            }
            ${executiveFunctionEnabled ? 'transform-gpu' : ''}
          `}
          aria-current={!currentDomain ? 'page' : undefined}
        >
          <Home className="w-4 h-4" />
          <span className="text-sm">Overview</span>
        </button>

        {/* Domain Buttons */}
        {domains.map((domain) => {
          const IconComponent = getDomainIcon(domain.name);
          const isActive = currentDomain === domain.name;
          
          return (
            <button
              key={domain.name}
              onClick={() => handleDomainSelect(domain.name)}
              className={`
                flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
                ${isActive
                  ? 'text-white font-medium shadow-md'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }
                ${executiveFunctionEnabled ? 'transform-gpu' : ''}
              `}
              style={isActive ? { backgroundColor: domain.color } : {}}
              aria-current={isActive ? 'page' : undefined}
              title={`${domain.display_name} - ${domain.tool_count} tools`}
            >
              <IconComponent className="w-4 h-4" />
              <span className="text-sm">{domain.display_name}</span>
              <span className="text-xs opacity-70">({domain.tool_count})</span>
            </button>
          );
        })}
      </nav>

      {/* Mobile Menu - Slide Down */}
      {isOpen && (
        <div className="md:hidden absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
          <nav className="p-4 space-y-2" role="navigation" aria-label="Mobile domain navigation">
            {/* Dashboard Home */}
            <button
              onClick={() => handleDomainSelect(null)}
              className={`
                w-full flex items-center space-x-3 px-3 py-3 rounded-lg transition-colors text-left
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
                ${!currentDomain 
                  ? 'bg-blue-100 text-blue-700 font-medium' 
                  : 'text-gray-700 hover:bg-gray-50'
                }
              `}
              aria-current={!currentDomain ? 'page' : undefined}
            >
              <Home className="w-5 h-5" />
              <div>
                <div className="font-medium">Overview</div>
                <div className="text-xs text-gray-500">All domains and tools</div>
              </div>
            </button>

            {/* Domain Options */}
            {domains.map((domain) => {
              const IconComponent = getDomainIcon(domain.name);
              const isActive = currentDomain === domain.name;
              
              return (
                <button
                  key={domain.name}
                  onClick={() => handleDomainSelect(domain.name)}
                  className={`
                    w-full flex items-center space-x-3 px-3 py-3 rounded-lg transition-colors text-left
                    focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50
                    ${isActive
                      ? 'text-white font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                    }
                  `}
                  style={isActive ? { backgroundColor: domain.color } : {}}
                  aria-current={isActive ? 'page' : undefined}
                >
                  <IconComponent className="w-5 h-5" />
                  <div className="flex-1">
                    <div className="font-medium">{domain.display_name}</div>
                    <div className={`text-xs ${isActive ? 'text-white text-opacity-80' : 'text-gray-500'}`}>
                      {domain.tool_count} tools • {domain.active_tools} active
                    </div>
                  </div>
                  {domain.active_tools < domain.tool_count && (
                    <div className="w-2 h-2 bg-amber-400 rounded-full" title="Some tools inactive" />
                  )}
                </button>
              );
            })}
          </nav>
        </div>
      )}
    </div>
  );
};

export const DomainNavigation: React.FC<NavigationProps> = ({
  currentDomain = null,
  currentPath = [],
  domains,
  onDomainChange,
  onPathChange,
  executiveFunctionEnabled,
  className = ''
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleDomainChange = useCallback((domain: string | null) => {
    onDomainChange(domain);
    // Reset path when changing domains for cognitive load reduction
    onPathChange(domain ? [domain] : []);
  }, [onDomainChange, onPathChange]);

  const handleBackNavigation = useCallback(() => {
    if (currentPath.length > 1) {
      onPathChange(currentPath.slice(0, -1));
    } else if (currentDomain) {
      handleDomainChange(null);
    }
  }, [currentPath, currentDomain, handleDomainChange, onPathChange]);

  // Get current domain data for context
  const currentDomainData = useMemo(() => {
    return domains.find(d => d.name === currentDomain) || null;
  }, [domains, currentDomain]);

  return (
    <header 
      className={`
        domain-navigation 
        bg-white 
        border-b 
        border-gray-200 
        px-4 
        py-3 
        md:px-6 
        ${className}
      `}
      role="banner"
    >
      <div className="flex items-center justify-between">
        {/* Back Button - Executive Function Support */}
        {(currentDomain || currentPath.length > 0) && (
          <button
            onClick={handleBackNavigation}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 rounded p-2 mr-4"
            aria-label="Go back to previous view"
          >
            <ArrowLeft className="w-4 h-4" />
            <span className="text-sm font-medium">Back</span>
          </button>
        )}

        {/* Domain Menu */}
        <div className="flex-1">
          <DomainMenu
            domains={domains}
            currentDomain={currentDomain}
            onDomainSelect={handleDomainChange}
            executiveFunctionEnabled={executiveFunctionEnabled}
            isOpen={mobileMenuOpen}
            onToggle={() => setMobileMenuOpen(!mobileMenuOpen)}
          />
        </div>

        {/* Right Side Actions */}
        <div className="flex items-center space-x-2">
          {/* Quick Search - Hidden on mobile to reduce cognitive load */}
          <button
            className="hidden md:flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Open search"
          >
            <Search className="w-4 h-4" />
            <span className="text-sm">Search</span>
          </button>

          {/* User Menu */}
          <button
            className="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="User menu"
          >
            <User className="w-4 h-4" />
          </button>

          {/* Settings */}
          <button
            className="flex items-center space-x-2 p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Settings"
          >
            <Settings className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Breadcrumb Navigation - Executive Function Context Preservation */}
      {currentPath.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <Breadcrumb
            path={currentPath}
            onPathChange={onPathChange}
            executiveFunctionEnabled={executiveFunctionEnabled}
          />
        </div>
      )}

      {/* Current Domain Context - ADHD/Autism Support */}
      {currentDomainData && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div 
                className="w-3 h-3 rounded-full"
                style={{ backgroundColor: currentDomainData.color }}
                aria-hidden="true"
              />
              <div>
                <h2 className="text-lg font-semibold text-gray-900">
                  {currentDomainData.display_name}
                </h2>
                <p className="text-sm text-gray-600">
                  {currentDomainData.description}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <span className="font-medium text-gray-900">
                  {currentDomainData.active_tools}
                </span>
                <span>/ {currentDomainData.tool_count} active tools</span>
              </div>
              
              {executiveFunctionEnabled && (
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span>EF Optimized</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Executive Function Status Indicator */}
      {executiveFunctionEnabled && (
        <div className="mt-2 text-xs text-gray-500 flex items-center justify-end">
          <div className="flex items-center space-x-1">
            <div className="w-2 h-2 bg-green-400 rounded-full"></div>
            <span>Executive function accommodations active</span>
          </div>
        </div>
      )}
    </header>
  );
};