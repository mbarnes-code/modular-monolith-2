/**
 * Tool Grid Component
 * 
 * Displays tools in grid or list layout with executive function accommodations:
 * - Consistent visual patterns for autism support
 * - Quick access actions for ADHD support
 * - Cognitive load management with progressive disclosure
 * - Performance indicators and health status
 */

'use client';

import { AnimatePresence, motion } from 'framer-motion';
import {
    Activity,
    CheckCircle,
    Clock,
    ExternalLink,
    Heart,
    Info
} from 'lucide-react';
import React, { useMemo, useState } from 'react';

interface Tool {
  id: string;
  name: string;
  display_name: string;
  description: string;
  domain: string;
  url?: string;
  icon?: string;
  status: 'active' | 'inactive' | 'maintenance';
  health_score: number;
  last_used?: string;
  integration_status: 'integrated' | 'partial' | 'pending';
  cognitive_load_score: number;
  executive_function_features: string[];
  constitutional_compliance: boolean;
  performance_metrics?: {
    avg_response_time_ms: number;
    uptime_percentage: number;
    last_health_check: string;
  };
}

interface ToolGridProps {
  tools: Tool[];
  onToolClick: (tool: Tool) => void;
  layout: 'grid' | 'list';
  executiveFunctionEnabled: boolean;
  showPerformanceMetrics?: boolean;
  cognitiveLoadFilter?: 'low' | 'medium' | 'high' | null;
  className?: string;
}

interface ToolCardProps {
  tool: Tool;
  onClick: () => void;
  layout: 'grid' | 'list';
  executiveFunctionEnabled: boolean;
  showPerformanceMetrics: boolean;
}

const getStatusColor = (status: Tool['status']) => {
  switch (status) {
    case 'active':
      return 'text-green-600 bg-green-50';
    case 'maintenance':
      return 'text-amber-600 bg-amber-50';
    case 'inactive':
      return 'text-gray-600 bg-gray-50';
    default:
      return 'text-gray-600 bg-gray-50';
  }
};

const getHealthColor = (healthScore: number) => {
  if (healthScore >= 90) return 'text-green-600';
  if (healthScore >= 70) return 'text-amber-600';
  return 'text-red-600';
};

const getCognitiveLoadLabel = (score: number) => {
  if (score <= 3) return { label: 'Low', color: 'text-green-600 bg-green-50' };
  if (score <= 6) return { label: 'Medium', color: 'text-amber-600 bg-amber-50' };
  return { label: 'High', color: 'text-red-600 bg-red-50' };
};

const ToolCard: React.FC<ToolCardProps> = ({
  tool,
  onClick,
  layout,
  executiveFunctionEnabled,
  showPerformanceMetrics
}) => {
  const [showDetails, setShowDetails] = useState(false);
  
  const statusColor = getStatusColor(tool.status);
  const healthColor = getHealthColor(tool.health_score);
  const cognitiveLoad = getCognitiveLoadLabel(tool.cognitive_load_score);

  const cardVariants = {
    idle: { 
      scale: 1, 
      boxShadow: '0 1px 3px rgba(0,0,0,0.1)' 
    },
    hover: { 
      scale: executiveFunctionEnabled ? 1.01 : 1.02,
      boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
      transition: {
        duration: executiveFunctionEnabled ? 0.1 : 0.2,
        ease: 'easeOut'
      }
    }
  };

  if (layout === 'list') {
    return (
      <motion.div
        variants={cardVariants}
        initial="idle"
        whileHover="hover"
        className="tool-card-list bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
        onClick={onClick}
        role="button"
        tabIndex={0}
        aria-label={`${tool.display_name} - ${tool.description}`}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 flex-1">
            {/* Tool Icon/Status */}
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                tool.status === 'active' ? 'bg-green-400' :
                tool.status === 'maintenance' ? 'bg-amber-400' :
                'bg-gray-400'
              }`} />
              <Activity className="w-5 h-5 text-gray-500" />
            </div>

            {/* Tool Info */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2">
                <h3 className="font-medium text-gray-900 truncate">
                  {tool.display_name}
                </h3>
                <span className={`px-2 py-1 text-xs rounded-full ${statusColor}`}>
                  {tool.status}
                </span>
                {tool.constitutional_compliance && (
                  <CheckCircle className="w-4 h-4 text-green-500" title="Constitutional compliance" />
                )}
              </div>
              <p className="text-sm text-gray-500 truncate mt-1">
                {tool.description}
              </p>
            </div>
          </div>

          {/* Performance Metrics */}
          {showPerformanceMetrics && (
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center space-x-1">
                <Heart className={`w-4 h-4 ${healthColor}`} />
                <span className={healthColor}>{tool.health_score}%</span>
              </div>
              {tool.performance_metrics && (
                <div className="flex items-center space-x-1">
                  <Clock className="w-4 h-4 text-gray-400" />
                  <span className="text-gray-600">
                    {tool.performance_metrics.avg_response_time_ms}ms
                  </span>
                </div>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex items-center space-x-2 ml-4">
            {executiveFunctionEnabled && (
              <div className={`px-2 py-1 text-xs rounded ${cognitiveLoad.color}`}>
                {cognitiveLoad.label} Load
              </div>
            )}
            <button
              onClick={(e) => {
                e.stopPropagation();
                setShowDetails(!showDetails);
              }}
              className="p-1 text-gray-400 hover:text-gray-600"
              aria-label="Toggle details"
            >
              <Info className="w-4 h-4" />
            </button>
            <ExternalLink className="w-4 h-4 text-gray-400" />
          </div>
        </div>

        {/* Extended Details */}
        <AnimatePresence>
          {showDetails && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="mt-4 pt-4 border-t border-gray-100 space-y-2"
            >
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Domain:</span>
                  <span className="ml-2 font-medium capitalize">{tool.domain}</span>
                </div>
                <div>
                  <span className="text-gray-500">Integration:</span>
                  <span className={`ml-2 font-medium ${
                    tool.integration_status === 'integrated' ? 'text-green-600' :
                    tool.integration_status === 'partial' ? 'text-amber-600' :
                    'text-gray-600'
                  }`}>
                    {tool.integration_status}
                  </span>
                </div>
              </div>
              
              {tool.executive_function_features.length > 0 && (
                <div>
                  <span className="text-gray-500 text-sm">Executive Function Features:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {tool.executive_function_features.map((feature, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded"
                      >
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    );
  }

  // Grid layout
  return (
    <motion.div
      variants={cardVariants}
      initial="idle"
      whileHover="hover"
      className="tool-card-grid bg-white border border-gray-200 rounded-lg p-6 hover:border-blue-300 transition-colors cursor-pointer"
      onClick={onClick}
      role="button"
      tabIndex={0}
      aria-label={`${tool.display_name} - ${tool.description}`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="flex items-center justify-center w-10 h-10 bg-gray-100 rounded-lg">
            <Activity className="w-5 h-5 text-gray-600" />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-gray-900 truncate">
              {tool.display_name}
            </h3>
            <p className="text-sm text-gray-500 capitalize">{tool.domain}</p>
          </div>
        </div>
        
        {/* Status Badge */}
        <div className="flex items-center space-x-1">
          <div className={`w-2 h-2 rounded-full ${
            tool.status === 'active' ? 'bg-green-400' :
            tool.status === 'maintenance' ? 'bg-amber-400' :
            'bg-gray-400'
          }`} />
          {tool.constitutional_compliance && (
            <CheckCircle className="w-4 h-4 text-green-500" />
          )}
        </div>
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">
        {tool.description}
      </p>

      {/* Metrics */}
      <div className="space-y-3 mb-4">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-500">Health Score</span>
          <div className="flex items-center space-x-1">
            <Heart className={`w-4 h-4 ${healthColor}`} />
            <span className={`font-medium ${healthColor}`}>
              {tool.health_score}%
            </span>
          </div>
        </div>

        {executiveFunctionEnabled && (
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Cognitive Load</span>
            <span className={`px-2 py-1 text-xs rounded ${cognitiveLoad.color}`}>
              {cognitiveLoad.label}
            </span>
          </div>
        )}

        {showPerformanceMetrics && tool.performance_metrics && (
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Response Time</span>
            <div className="flex items-center space-x-1">
              <Clock className="w-4 h-4 text-gray-400" />
              <span className="text-gray-600">
                {tool.performance_metrics.avg_response_time_ms}ms
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Integration Status */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-100">
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${
            tool.integration_status === 'integrated' ? 'bg-green-400' :
            tool.integration_status === 'partial' ? 'bg-amber-400' :
            'bg-gray-400'
          }`} />
          <span className="text-xs text-gray-500 capitalize">
            {tool.integration_status}
          </span>
        </div>
        
        {tool.last_used && (
          <span className="text-xs text-gray-400">
            Used {new Date(tool.last_used).toLocaleDateString()}
          </span>
        )}
      </div>

      {/* Executive Function Features */}
      {executiveFunctionEnabled && tool.executive_function_features.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex flex-wrap gap-1">
            {tool.executive_function_features.slice(0, 2).map((feature, index) => (
              <span
                key={index}
                className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded"
              >
                {feature}
              </span>
            ))}
            {tool.executive_function_features.length > 2 && (
              <span className="px-2 py-1 text-xs bg-gray-50 text-gray-600 rounded">
                +{tool.executive_function_features.length - 2} more
              </span>
            )}
          </div>
        </div>
      )}
    </motion.div>
  );
};

export const ToolGrid: React.FC<ToolGridProps> = ({
  tools,
  onToolClick,
  layout,
  executiveFunctionEnabled,
  showPerformanceMetrics = false,
  cognitiveLoadFilter = null,
  className = ''
}) => {
  const filteredTools = useMemo(() => {
    if (!cognitiveLoadFilter) return tools;
    
    return tools.filter(tool => {
      const cognitiveLoad = getCognitiveLoadLabel(tool.cognitive_load_score);
      return cognitiveLoad.label.toLowerCase() === cognitiveLoadFilter;
    });
  }, [tools, cognitiveLoadFilter]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: executiveFunctionEnabled ? 0.05 : 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: executiveFunctionEnabled ? 0.2 : 0.3
      }
    }
  };

  if (filteredTools.length === 0) {
    return (
      <div className={`tool-grid-empty text-center py-12 ${className}`}>
        <Activity className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No Tools Found</h3>
        <p className="text-gray-500">
          {cognitiveLoadFilter 
            ? `No tools match the ${cognitiveLoadFilter} cognitive load filter.`
            : 'No tools are available at the moment.'
          }
        </p>
      </div>
    );
  }

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className={`tool-grid ${className}`}
    >
      <div className={
        layout === 'grid' 
          ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
          : 'space-y-4'
      }>
        {filteredTools.map((tool) => (
          <motion.div key={tool.id} variants={itemVariants}>
            <ToolCard
              tool={tool}
              onClick={() => onToolClick(tool)}
              layout={layout}
              executiveFunctionEnabled={executiveFunctionEnabled}
              showPerformanceMetrics={showPerformanceMetrics}
            />
          </motion.div>
        ))}
      </div>

      {/* Summary Stats */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>
            Showing {filteredTools.length} of {tools.length} tools
          </span>
          {executiveFunctionEnabled && (
            <span className="flex items-center space-x-1">
              <CheckCircle className="w-4 h-4 text-green-500" />
              <span>Executive function optimized</span>
            </span>
          )}
        </div>
      </div>
    </motion.div>
  );
};