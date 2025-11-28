/**
 * Cognitive Load Visualization Component
 * Advanced visual indicators, heat maps, and real-time cognitive load feedback
 */

import { AnimatePresence, motion } from 'framer-motion';
import {
    Activity,
    AlertTriangle,
    BarChart3,
    Brain,
    CheckCircle,
    Eye,
    Minus,
    TrendingDown,
    TrendingUp,
    Waves,
    Zap
} from 'lucide-react';
import React, { useEffect, useMemo, useRef, useState } from 'react';

interface CognitiveLoadData {
  visual: number;
  cognitive: number;
  memory: number;
  attention: number;
  total: number;
  timestamp: number;
}

interface ToolLoadVisualization {
  toolId: string;
  toolName: string;
  domain: string;
  currentLoad: number;
  averageLoad: number;
  peakLoad: number;
  accessFrequency: number;
  lastUsed: number;
  trend: 'increasing' | 'decreasing' | 'stable';
}

interface CognitiveHeatMapProps {
  tools: ToolLoadVisualization[];
  selectedTool?: string | null;
  onToolHover?: (toolId: string | null) => void;
  onToolSelect?: (toolId: string) => void;
  className?: string;
}

interface LoadTrendVisualizerProps {
  loadHistory: CognitiveLoadData[];
  timeWindow: number; // minutes
  className?: string;
}

interface RealTimeLoadIndicatorProps {
  currentLoad: CognitiveLoadData;
  thresholds: {
    optimal: number;
    warning: number;
    critical: number;
  };
  className?: string;
}

// Color schemes for different load levels
const LOAD_COLORS = {
  low: {
    primary: '#10b981', // green-500
    secondary: '#d1fae5', // green-100
    text: '#047857' // green-700
  },
  medium: {
    primary: '#f59e0b', // amber-500
    secondary: '#fef3c7', // amber-100
    text: '#b45309' // amber-700
  },
  high: {
    primary: '#ef4444', // red-500
    secondary: '#fee2e2', // red-100
    text: '#b91c1c' // red-700
  },
  critical: {
    primary: '#7c2d12', // red-900
    secondary: '#fecaca', // red-200
    text: '#ffffff'
  }
};

const DOMAIN_COLORS = {
  security: '#dc2626', // red-600
  productivity: '#2563eb', // blue-600
  mtg: '#7c3aed', // violet-600
  infrastructure: '#059669' // emerald-600
};

export function CognitiveHeatMap({ 
  tools, 
  selectedTool, 
  onToolHover, 
  onToolSelect, 
  className = '' 
}: CognitiveHeatMapProps) {
  const [viewMode, setViewMode] = useState<'grid' | 'matrix' | 'radial'>('grid');
  const [sortBy, setSortBy] = useState<'load' | 'frequency' | 'domain'>('load');

  const sortedTools = useMemo(() => {
    return [...tools].sort((a, b) => {
      switch (sortBy) {
        case 'load':
          return b.currentLoad - a.currentLoad;
        case 'frequency':
          return b.accessFrequency - a.accessFrequency;
        case 'domain':
          return a.domain.localeCompare(b.domain);
        default:
          return 0;
      }
    });
  }, [tools, sortBy]);

  const getLoadColor = (load: number): string => {
    if (load < 40) return LOAD_COLORS.low.primary;
    if (load < 70) return LOAD_COLORS.medium.primary;
    if (load < 90) return LOAD_COLORS.high.primary;
    return LOAD_COLORS.critical.primary;
  };

  const getLoadIntensity = (load: number): number => {
    return Math.max(0.2, Math.min(1, load / 100));
  };

  const getTrendIcon = (trend: ToolLoadVisualization['trend']) => {
    switch (trend) {
      case 'increasing': return TrendingUp;
      case 'decreasing': return TrendingDown;
      case 'stable': default: return Minus;
    }
  };

  const renderGridView = () => (
    <div className="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-8 gap-2">
      {sortedTools.map((tool) => {
        const isSelected = selectedTool === tool.toolId;
        const intensity = getLoadIntensity(tool.currentLoad);
        const TrendIcon = getTrendIcon(tool.trend);
        
        return (
          <motion.div
            key={tool.toolId}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`
              relative aspect-square rounded-lg cursor-pointer transition-all duration-200
              ${isSelected ? 'ring-2 ring-blue-500 ring-offset-2' : ''}
            `}
            style={{
              backgroundColor: getLoadColor(tool.currentLoad),
              opacity: intensity
            }}
            onMouseEnter={() => onToolHover?.(tool.toolId)}
            onMouseLeave={() => onToolHover?.(null)}
            onClick={() => onToolSelect?.(tool.toolId)}
          >
            {/* Tool identifier */}
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-xs font-medium text-white text-center px-1">
                {tool.toolName.substring(0, 3).toUpperCase()}
              </span>
            </div>
            
            {/* Load percentage */}
            <div className="absolute top-0 right-0 bg-black bg-opacity-50 text-white text-xs px-1 rounded-bl">
              {Math.round(tool.currentLoad)}
            </div>
            
            {/* Trend indicator */}
            <div className="absolute bottom-0 left-0 p-1">
              <TrendIcon className="w-3 h-3 text-white" />
            </div>
            
            {/* Domain indicator */}
            <div 
              className="absolute bottom-0 right-0 w-2 h-2 rounded-tl"
              style={{ backgroundColor: DOMAIN_COLORS[tool.domain as keyof typeof DOMAIN_COLORS] }}
            />
          </motion.div>
        );
      })}
    </div>
  );

  const renderMatrixView = () => {
    // Group tools by domain for matrix view
    const toolsByDomain = sortedTools.reduce((acc, tool) => {
      if (!acc[tool.domain]) acc[tool.domain] = [];
      acc[tool.domain].push(tool);
      return acc;
    }, {} as Record<string, ToolLoadVisualization[]>);

    return (
      <div className="space-y-4">
        {Object.entries(toolsByDomain).map(([domain, domainTools]) => (
          <div key={domain} className="space-y-2">
            <div className="flex items-center gap-2">
              <div 
                className="w-3 h-3 rounded"
                style={{ backgroundColor: DOMAIN_COLORS[domain as keyof typeof DOMAIN_COLORS] }}
              />
              <span className="text-sm font-medium capitalize">{domain}</span>
              <span className="text-xs text-gray-500">
                Avg: {Math.round(domainTools.reduce((sum, t) => sum + t.currentLoad, 0) / domainTools.length)}%
              </span>
            </div>
            <div className="flex flex-wrap gap-1">
              {domainTools.map((tool) => (
                <div
                  key={tool.toolId}
                  className="h-6 px-2 rounded text-xs font-medium text-white flex items-center cursor-pointer transition-all hover:scale-105"
                  style={{
                    backgroundColor: getLoadColor(tool.currentLoad),
                    opacity: getLoadIntensity(tool.currentLoad)
                  }}
                  onMouseEnter={() => onToolHover?.(tool.toolId)}
                  onMouseLeave={() => onToolHover?.(null)}
                  onClick={() => onToolSelect?.(tool.toolId)}
                >
                  {tool.toolName}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderRadialView = () => {
    const centerX = 150;
    const centerY = 150;
    const maxRadius = 120;
    
    return (
      <div className="flex justify-center">
        <svg width="300" height="300" className="overflow-visible">
          {/* Background circles */}
          {[0.25, 0.5, 0.75, 1].map((factor, index) => (
            <circle
              key={index}
              cx={centerX}
              cy={centerY}
              r={maxRadius * factor}
              fill="none"
              stroke="#e5e7eb"
              strokeWidth="1"
              opacity="0.3"
            />
          ))}
          
          {/* Tools positioned by load and frequency */}
          {sortedTools.map((tool, index) => {
            const angle = (index / sortedTools.length) * 2 * Math.PI;
            const radius = (tool.currentLoad / 100) * maxRadius;
            const x = centerX + Math.cos(angle) * radius;
            const y = centerY + Math.sin(angle) * radius;
            const size = Math.max(8, (tool.accessFrequency / 10) * 20);
            
            return (
              <g key={tool.toolId}>
                <circle
                  cx={x}
                  cy={y}
                  r={size}
                  fill={getLoadColor(tool.currentLoad)}
                  opacity={getLoadIntensity(tool.currentLoad)}
                  className="cursor-pointer transition-all hover:r="
                  onMouseEnter={() => onToolHover?.(tool.toolId)}
                  onMouseLeave={() => onToolHover?.(null)}
                  onClick={() => onToolSelect?.(tool.toolId)}
                />
                <text
                  x={x}
                  y={y}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fontSize="8"
                  fill="white"
                  className="pointer-events-none font-medium"
                >
                  {tool.toolName.substring(0, 2).toUpperCase()}
                </text>
              </g>
            );
          })}
          
          {/* Center label */}
          <text
            x={centerX}
            y={centerY}
            textAnchor="middle"
            dominantBaseline="central"
            fontSize="10"
            fill="#6b7280"
            className="font-medium"
          >
            Cognitive Load
          </text>
        </svg>
      </div>
    );
  };

  return (
    <div className={`cognitive-heat-map ${className}`}>
      {/* Controls */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Brain className="w-4 h-4 text-gray-600" />
          <span className="text-sm font-medium">Load Heat Map</span>
        </div>
        
        <div className="flex items-center gap-2">
          {/* Sort controls */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="text-xs border border-gray-300 rounded px-2 py-1"
          >
            <option value="load">By Load</option>
            <option value="frequency">By Usage</option>
            <option value="domain">By Domain</option>
          </select>
          
          {/* View mode controls */}
          <div className="flex border border-gray-300 rounded overflow-hidden">
            {[
              { mode: 'grid' as const, icon: BarChart3 },
              { mode: 'matrix' as const, icon: Activity },
              { mode: 'radial' as const, icon: Waves }
            ].map(({ mode, icon: Icon }) => (
              <button
                key={mode}
                onClick={() => setViewMode(mode)}
                className={`p-1 ${
                  viewMode === mode 
                    ? 'bg-blue-500 text-white' 
                    : 'bg-white text-gray-600 hover:bg-gray-50'
                }`}
              >
                <Icon className="w-3 h-3" />
              </button>
            ))}
          </div>
        </div>
      </div>
      
      {/* Heat map visualization */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        {viewMode === 'grid' && renderGridView()}
        {viewMode === 'matrix' && renderMatrixView()}
        {viewMode === 'radial' && renderRadialView()}
      </div>
      
      {/* Legend */}
      <div className="mt-3 flex items-center justify-center gap-6 text-xs">
        <div className="flex items-center gap-4">
          {Object.entries(LOAD_COLORS).map(([level, colors]) => (
            <div key={level} className="flex items-center gap-1">
              <div 
                className="w-3 h-3 rounded"
                style={{ backgroundColor: colors.primary }}
              />
              <span className="capitalize">{level}</span>
            </div>
          ))}
        </div>
        <div className="w-px h-4 bg-gray-300" />
        <div className="flex items-center gap-4">
          {Object.entries(DOMAIN_COLORS).map(([domain, color]) => (
            <div key={domain} className="flex items-center gap-1">
              <div 
                className="w-3 h-3 rounded"
                style={{ backgroundColor: color }}
              />
              <span className="capitalize">{domain}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function LoadTrendVisualizer({ 
  loadHistory, 
  timeWindow, 
  className = '' 
}: LoadTrendVisualizerProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [hoveredPoint, setHoveredPoint] = useState<{ x: number; y: number; data: CognitiveLoadData } | null>(null);

  // Filter history to time window
  const filteredHistory = useMemo(() => {
    const cutoff = Date.now() - (timeWindow * 60 * 1000);
    return loadHistory.filter(entry => entry.timestamp >= cutoff);
  }, [loadHistory, timeWindow]);

  // Draw trend chart
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || filteredHistory.length < 2) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const { width, height } = canvas;
    ctx.clearRect(0, 0, width, height);

    // Setup
    const padding = 40;
    const chartWidth = width - padding * 2;
    const chartHeight = height - padding * 2;
    
    const maxLoad = Math.max(...filteredHistory.map(h => h.total));
    const minTime = Math.min(...filteredHistory.map(h => h.timestamp));
    const maxTime = Math.max(...filteredHistory.map(h => h.timestamp));

    // Draw grid
    ctx.strokeStyle = '#f3f4f6';
    ctx.lineWidth = 1;
    
    // Horizontal grid lines
    for (let i = 0; i <= 4; i++) {
      const y = padding + (chartHeight / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(padding + chartWidth, y);
      ctx.stroke();
    }
    
    // Vertical grid lines
    for (let i = 0; i <= 6; i++) {
      const x = padding + (chartWidth / 6) * i;
      ctx.beginPath();
      ctx.moveTo(x, padding);
      ctx.lineTo(x, padding + chartHeight);
      ctx.stroke();
    }

    // Draw trend lines
    const drawTrendLine = (
      dataPoints: number[], 
      color: string, 
      label: string
    ) => {
      if (dataPoints.length < 2) return;

      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();

      filteredHistory.forEach((entry, index) => {
        const x = padding + ((entry.timestamp - minTime) / (maxTime - minTime)) * chartWidth;
        const y = padding + chartHeight - (dataPoints[index] / 100) * chartHeight;
        
        if (index === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });

      ctx.stroke();

      // Draw points
      ctx.fillStyle = color;
      filteredHistory.forEach((entry, index) => {
        const x = padding + ((entry.timestamp - minTime) / (maxTime - minTime)) * chartWidth;
        const y = padding + chartHeight - (dataPoints[index] / 100) * chartHeight;
        
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, 2 * Math.PI);
        ctx.fill();
      });
    };

    // Draw each load type
    drawTrendLine(filteredHistory.map(h => h.visual), '#8b5cf6', 'Visual');
    drawTrendLine(filteredHistory.map(h => h.cognitive), '#06b6d4', 'Cognitive');
    drawTrendLine(filteredHistory.map(h => h.memory), '#10b981', 'Memory');
    drawTrendLine(filteredHistory.map(h => h.attention), '#f59e0b', 'Attention');
    drawTrendLine(filteredHistory.map(h => h.total), '#ef4444', 'Total');

    // Draw labels
    ctx.fillStyle = '#374151';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    
    // Y-axis labels
    for (let i = 0; i <= 4; i++) {
      const y = padding + (chartHeight / 4) * i;
      const value = 100 - (i * 25);
      ctx.fillText(value.toString(), padding - 20, y + 4);
    }
    
    // X-axis labels (time)
    for (let i = 0; i <= 3; i++) {
      const x = padding + (chartWidth / 3) * i;
      const timeOffset = (timeWindow / 3) * (3 - i);
      const label = timeOffset === 0 ? 'Now' : `${Math.round(timeOffset)}m ago`;
      ctx.fillText(label, x, height - padding + 20);
    }

  }, [filteredHistory, timeWindow]);

  const handleCanvasMouseMove = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas || filteredHistory.length === 0) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Find closest data point
    const padding = 40;
    const chartWidth = canvas.width - padding * 2;
    const minTime = Math.min(...filteredHistory.map(h => h.timestamp));
    const maxTime = Math.max(...filteredHistory.map(h => h.timestamp));

    let closestPoint = null;
    let closestDistance = Infinity;

    filteredHistory.forEach((entry, index) => {
      const pointX = padding + ((entry.timestamp - minTime) / (maxTime - minTime)) * chartWidth;
      const distance = Math.abs(x - pointX);
      
      if (distance < closestDistance && distance < 20) {
        closestDistance = distance;
        closestPoint = { x: pointX, y, data: entry };
      }
    });

    setHoveredPoint(closestPoint);
  };

  return (
    <div className={`load-trend-visualizer ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-gray-600" />
          <span className="text-sm font-medium">Cognitive Load Trends</span>
        </div>
        <span className="text-xs text-gray-500">Last {timeWindow} minutes</span>
      </div>

      <div className="relative bg-white rounded-lg border border-gray-200 p-4">
        <canvas
          ref={canvasRef}
          width={400}
          height={200}
          className="w-full h-48 cursor-crosshair"
          onMouseMove={handleCanvasMouseMove}
          onMouseLeave={() => setHoveredPoint(null)}
        />

        {/* Hover tooltip */}
        <AnimatePresence>
          {hoveredPoint && (
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="absolute bg-gray-900 text-white text-xs rounded p-2 pointer-events-none z-10"
              style={{
                left: hoveredPoint.x,
                top: hoveredPoint.y - 60,
                transform: 'translateX(-50%)'
              }}
            >
              <div className="space-y-1">
                <div>Total: {hoveredPoint.data.total}%</div>
                <div>Visual: {hoveredPoint.data.visual}%</div>
                <div>Cognitive: {hoveredPoint.data.cognitive}%</div>
                <div>Memory: {hoveredPoint.data.memory}%</div>
                <div>Attention: {hoveredPoint.data.attention}%</div>
              </div>
              <div className="text-center mt-1 text-gray-400">
                {new Date(hoveredPoint.data.timestamp).toLocaleTimeString()}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Legend */}
      <div className="mt-3 flex items-center justify-center gap-4 text-xs">
        {[
          { label: 'Visual', color: '#8b5cf6' },
          { label: 'Cognitive', color: '#06b6d4' },
          { label: 'Memory', color: '#10b981' },
          { label: 'Attention', color: '#f59e0b' },
          { label: 'Total', color: '#ef4444' }
        ].map(({ label, color }) => (
          <div key={label} className="flex items-center gap-1">
            <div 
              className="w-3 h-0.5 rounded"
              style={{ backgroundColor: color }}
            />
            <span>{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function RealTimeLoadIndicator({ 
  currentLoad, 
  thresholds, 
  className = '' 
}: RealTimeLoadIndicatorProps) {
  const [animationPhase, setAnimationPhase] = useState(0);

  // Pulse animation for high load
  useEffect(() => {
    if (currentLoad.total > thresholds.warning) {
      const interval = setInterval(() => {
        setAnimationPhase(prev => (prev + 1) % 4);
      }, 500);
      return () => clearInterval(interval);
    }
  }, [currentLoad.total, thresholds.warning]);

  const getLoadStatus = () => {
    if (currentLoad.total < thresholds.optimal) return 'optimal';
    if (currentLoad.total < thresholds.warning) return 'good';
    if (currentLoad.total < thresholds.critical) return 'warning';
    return 'critical';
  };

  const getStatusIcon = () => {
    switch (getLoadStatus()) {
      case 'optimal': return CheckCircle;
      case 'good': return CheckCircle;
      case 'warning': return AlertTriangle;
      case 'critical': return AlertTriangle;
    }
  };

  const getStatusColor = () => {
    switch (getLoadStatus()) {
      case 'optimal': return LOAD_COLORS.low;
      case 'good': return LOAD_COLORS.low;
      case 'warning': return LOAD_COLORS.medium;
      case 'critical': return LOAD_COLORS.high;
    }
  };

  const StatusIcon = getStatusIcon();
  const statusColor = getStatusColor();
  const shouldPulse = currentLoad.total > thresholds.warning;

  return (
    <div className={`real-time-load-indicator ${className}`}>
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <motion.div
              animate={shouldPulse ? { scale: [1, 1.1, 1] } : {}}
              transition={{ duration: 1, repeat: Infinity }}
            >
              <StatusIcon 
                className={`w-5 h-5`}
                style={{ color: statusColor.primary }}
              />
            </motion.div>
            <span className="font-medium text-gray-900">
              Cognitive Load: {Math.round(currentLoad.total)}%
            </span>
          </div>
          
          <div className="text-xs text-gray-500 capitalize">
            {getLoadStatus()}
          </div>
        </div>

        {/* Load bars */}
        <div className="space-y-3">
          {[
            { label: 'Visual', value: currentLoad.visual, icon: Eye },
            { label: 'Cognitive', value: currentLoad.cognitive, icon: Brain },
            { label: 'Memory', value: currentLoad.memory, icon: Zap },
            { label: 'Attention', value: currentLoad.attention, icon: Activity }
          ].map(({ label, value, icon: Icon }) => (
            <div key={label} className="space-y-1">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <Icon className="w-3 h-3 text-gray-500" />
                  <span className="text-gray-700">{label}</span>
                </div>
                <span className="font-medium">{Math.round(value)}%</span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <motion.div
                  className="h-2 rounded-full transition-colors duration-500"
                  style={{ 
                    backgroundColor: value > 80 ? LOAD_COLORS.high.primary :
                                   value > 60 ? LOAD_COLORS.medium.primary :
                                   LOAD_COLORS.low.primary
                  }}
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(100, value)}%` }}
                  transition={{ duration: 0.8, ease: 'easeOut' }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Total load visualization */}
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-900">Total Load</span>
            <span className="text-lg font-bold" style={{ color: statusColor.primary }}>
              {Math.round(currentLoad.total)}%
            </span>
          </div>
          
          {/* Circular progress indicator */}
          <div className="flex justify-center">
            <div className="relative w-24 h-24">
              <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                {/* Background circle */}
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke="#e5e7eb"
                  strokeWidth="8"
                  fill="none"
                />
                
                {/* Progress circle */}
                <motion.circle
                  cx="50"
                  cy="50"
                  r="40"
                  stroke={statusColor.primary}
                  strokeWidth="8"
                  fill="none"
                  strokeLinecap="round"
                  strokeDasharray={`${2 * Math.PI * 40}`}
                  initial={{ strokeDashoffset: 2 * Math.PI * 40 }}
                  animate={{ 
                    strokeDashoffset: 2 * Math.PI * 40 * (1 - currentLoad.total / 100),
                    stroke: shouldPulse && animationPhase % 2 === 0 ? statusColor.text : statusColor.primary
                  }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                />
              </svg>
              
              {/* Center text */}
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-xs font-medium text-gray-600">
                  {Math.round(currentLoad.total)}%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Threshold indicators */}
        <div className="mt-4 flex justify-between text-xs text-gray-500">
          <span>Optimal: &lt;{thresholds.optimal}%</span>
          <span>Warning: {thresholds.warning}%</span>
          <span>Critical: {thresholds.critical}%</span>
        </div>
      </div>
    </div>
  );
}