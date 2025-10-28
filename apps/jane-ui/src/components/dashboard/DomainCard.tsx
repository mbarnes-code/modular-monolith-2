/**
 * Domain Card Component
 * 
 * Displays individual domain information with executive function accommodations:
 * - Clear visual hierarchy for cognitive load reduction
 * - ADHD-friendly interactions with immediate feedback
 * - Autism-friendly consistent patterns and predictable layouts
 * - Performance indicators for constitutional compliance
 */

'use client';

import { motion } from 'framer-motion';
import {
    Activity,
    AlertTriangle,
    Briefcase,
    CheckCircle,
    Clock,
    Gamepad2,
    Server,
    Shield
} from 'lucide-react';
import React from 'react';

interface Domain {
  name: string;
  display_name: string;
  description?: string;
  tool_count: number;
  active_tools: number;
  color: string;
  icon?: string;
  performance_stats?: {
    avg_response_time_ms: number;
    health_percentage: number;
    last_updated: string;
  };
  constitutional_limits: {
    max_response_ms: number;
    target_tools: number;
  };
}

interface DomainCardProps {
  domain: Domain;
  onClick: () => void;
  executiveFunctionEnabled: boolean;
  detailed?: boolean;
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

const getPerformanceStatus = (
  avgResponseTime: number, 
  maxResponseTime: number,
  healthPercentage: number
) => {
  if (avgResponseTime > maxResponseTime) {
    return { status: 'warning', color: 'text-amber-600', bgColor: 'bg-amber-50' };
  }
  if (healthPercentage < 80) {
    return { status: 'error', color: 'text-red-600', bgColor: 'bg-red-50' };
  }
  return { status: 'success', color: 'text-green-600', bgColor: 'bg-green-50' };
};

export const DomainCard: React.FC<DomainCardProps> = ({
  domain,
  onClick,
  executiveFunctionEnabled,
  detailed = false,
  className = ''
}) => {
  const IconComponent = getDomainIcon(domain.name);
  
  const performanceStatus = domain.performance_stats 
    ? getPerformanceStatus(
        domain.performance_stats.avg_response_time_ms,
        domain.constitutional_limits.max_response_ms,
        domain.performance_stats.health_percentage
      )
    : null;

  const cardVariants = {
    idle: { 
      scale: 1, 
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)' 
    },
    hover: { 
      scale: executiveFunctionEnabled ? 1.02 : 1.05,
      boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
      transition: {
        duration: executiveFunctionEnabled ? 0.1 : 0.2,
        ease: 'easeOut'
      }
    },
    tap: { 
      scale: 0.98,
      transition: { duration: 0.1 }
    }
  };

  return (
    <motion.div
      variants={cardVariants}
      initial="idle"
      whileHover="hover"
      whileTap="tap"
      onClick={onClick}
      className={`
        domain-card
        relative
        bg-white
        rounded-lg
        border-2
        border-gray-200
        p-6
        cursor-pointer
        transition-all
        duration-200
        hover:border-blue-300
        focus-within:ring-2
        focus-within:ring-blue-500
        focus-within:ring-opacity-50
        ${executiveFunctionEnabled ? 'transform-gpu' : ''}
        ${className}
      `}
      style={{
        borderLeftColor: domain.color,
        borderLeftWidth: '4px'
      }}
      role="button"
      tabIndex={0}
      aria-label={`${domain.display_name} domain with ${domain.tool_count} tools`}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {/* Domain Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div 
            className="flex items-center justify-center w-12 h-12 rounded-lg"
            style={{ backgroundColor: `${domain.color}20` }}
          >
            <IconComponent 
              className="w-6 h-6"
              style={{ color: domain.color }}
            />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {domain.display_name}
            </h3>
            <p className="text-sm text-gray-500">
              {domain.tool_count} tools • {domain.active_tools} active
            </p>
          </div>
        </div>

        {/* Performance Indicator */}
        {performanceStatus && (
          <div className={`flex items-center space-x-1 px-2 py-1 rounded-full ${performanceStatus.bgColor}`}>
            {performanceStatus.status === 'success' && <CheckCircle className={`w-4 h-4 ${performanceStatus.color}`} />}
            {performanceStatus.status === 'warning' && <Clock className={`w-4 h-4 ${performanceStatus.color}`} />}
            {performanceStatus.status === 'error' && <AlertTriangle className={`w-4 h-4 ${performanceStatus.color}`} />}
          </div>
        )}
      </div>

      {/* Domain Description */}
      {domain.description && (
        <p className="text-sm text-gray-600 mb-4 line-clamp-2">
          {domain.description}
        </p>
      )}

      {/* Performance Stats */}
      {detailed && domain.performance_stats && (
        <div className="space-y-3 mb-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Response Time</span>
            <div className="flex items-center space-x-1">
              <span className={`font-medium ${
                domain.performance_stats.avg_response_time_ms > domain.constitutional_limits.max_response_ms
                  ? 'text-amber-600' 
                  : 'text-green-600'
              }`}>
                {domain.performance_stats.avg_response_time_ms}ms
              </span>
              <span className="text-gray-400">
                / {domain.constitutional_limits.max_response_ms}ms
              </span>
            </div>
          </div>

          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Health Score</span>
            <span className={`font-medium ${
              domain.performance_stats.health_percentage >= 80 
                ? 'text-green-600' 
                : 'text-red-600'
            }`}>
              {domain.performance_stats.health_percentage}%
            </span>
          </div>

          {/* Constitutional Compliance Bar */}
          <div className="space-y-1">
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>Constitutional Compliance</span>
              <span>
                {domain.tool_count}/{domain.constitutional_limits.target_tools} tools
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-300 ${
                  domain.tool_count >= domain.constitutional_limits.target_tools
                    ? 'bg-green-500'
                    : domain.tool_count >= domain.constitutional_limits.target_tools * 0.8
                    ? 'bg-amber-500'
                    : 'bg-red-500'
                }`}
                style={{
                  width: `${Math.min(100, (domain.tool_count / domain.constitutional_limits.target_tools) * 100)}%`
                }}
              />
            </div>
          </div>
        </div>
      )}

      {/* Quick Stats */}
      <div className="grid grid-cols-2 gap-4 text-center">
        <div className="space-y-1">
          <div className="text-2xl font-bold" style={{ color: domain.color }}>
            {domain.tool_count}
          </div>
          <div className="text-xs text-gray-500 uppercase tracking-wide">
            Total Tools
          </div>
        </div>
        <div className="space-y-1">
          <div className="text-2xl font-bold text-green-600">
            {domain.active_tools}
          </div>
          <div className="text-xs text-gray-500 uppercase tracking-wide">
            Active
          </div>
        </div>
      </div>

      {/* Executive Function Indicators */}
      {executiveFunctionEnabled && (
        <div className="mt-4 pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-400 rounded-full"></div>
              <span>EF Optimized</span>
            </span>
            {domain.performance_stats && (
              <span>
                Updated {new Date(domain.performance_stats.last_updated).toLocaleTimeString()}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Hover Effect Overlay */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent to-blue-50 opacity-0 hover:opacity-100 transition-opacity duration-200 rounded-lg pointer-events-none" />
    </motion.div>
  );
};