'use client';

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';

interface DomainMetric {
  timestamp: number;
  responseTime: number;
  requests: number;
  errors: number;
}

interface DomainChartsProps {
  domain: string;
  threshold: number;
  data?: DomainMetric[];
  className?: string;
}

export const DomainCharts: React.FC<DomainChartsProps> = ({
  domain,
  threshold,
  data = [],
  className = ''
}) => {
  const [chartData, setChartData] = useState<DomainMetric[]>(data);
  const [isLoading] = useState(false);

  // Generate mock data for development
  const generateMockData = (): DomainMetric[] => {
    const now = Date.now();
    const mockData: DomainMetric[] = [];
    
    for (let i = 23; i >= 0; i--) {
      const timestamp = now - (i * 60 * 60 * 1000); // hourly data for 24 hours
      const baseResponse = threshold * 0.7; // 70% of threshold as baseline
      const variation = Math.random() * (threshold * 0.4); // +/- 20% variation
      const responseTime = Math.max(50, baseResponse + variation - (threshold * 0.2));
      
      mockData.push({
        timestamp,
        responseTime: Math.round(responseTime),
        requests: Math.floor(Math.random() * 1000) + 100,
        errors: Math.floor(Math.random() * 10),
      });
    }
    
    return mockData;
  };

  useEffect(() => {
    if (data.length === 0) {
      // Generate mock data if none provided
      setChartData(generateMockData());
    } else {
      setChartData(data);
    }
  }, [data, threshold]);

  const formatTime = (timestamp: number) => {
    return new Date(timestamp).toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  };

  const formatResponseTime = (ms: number) => {
    if (ms < 1000) {
      return `${ms}ms`;
    }
    return `${(ms / 1000).toFixed(2)}s`;
  };

  const maxResponseTime = Math.max(...chartData.map(d => d.responseTime), threshold);
  const maxRequests = Math.max(...chartData.map(d => d.requests));

  // Calculate chart dimensions
  const chartHeight = 200;
  const chartWidth = 600;
  const padding = { top: 20, right: 20, bottom: 40, left: 60 };
  const innerWidth = chartWidth - padding.left - padding.right;
  const innerHeight = chartHeight - padding.top - padding.bottom;

  // Create chart points
  const responseTimePoints = chartData.map((point, index) => {
    const x = padding.left + (index / (chartData.length - 1)) * innerWidth;
    const y = padding.top + ((maxResponseTime - point.responseTime) / maxResponseTime) * innerHeight;
    return { x, y, value: point.responseTime, timestamp: point.timestamp };
  });

  const requestPoints = chartData.map((point, index) => {
    const x = padding.left + (index / (chartData.length - 1)) * innerWidth;
    const y = padding.top + ((maxRequests - point.requests) / maxRequests) * innerHeight;
    return { x, y, value: point.requests, timestamp: point.timestamp };
  });

  // Threshold line
  const thresholdY = padding.top + ((maxResponseTime - threshold) / maxResponseTime) * innerHeight;

  const createPath = (points: typeof responseTimePoints) => {
    if (points.length === 0) return '';
    
    let path = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      path += ` L ${points[i].x} ${points[i].y}`;
    }
    return path;
  };

  const getDomainColor = (domain: string) => {
    const colors = {
      Security: '#dc2626', // red-600
      Productivity: '#2563eb', // blue-600
      MTG: '#9333ea', // purple-600
      Infrastructure: '#16a34a', // green-600
    };
    return colors[domain as keyof typeof colors] || '#6b7280';
  };

  const domainColor = getDomainColor(domain);

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Response Time Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            {domain} Domain - Response Time Trend
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center h-48">
              <span className="animate-spin mr-2">⟳</span>
              <span>Loading chart data...</span>
            </div>
          ) : (
            <div className="relative">
              <svg width={chartWidth} height={chartHeight} className="border rounded">
                {/* Grid lines */}
                {[0, 0.25, 0.5, 0.75, 1].map(ratio => {
                  const y = padding.top + ratio * innerHeight;
                  return (
                    <line
                      key={`grid-${ratio}`}
                      x1={padding.left}
                      y1={y}
                      x2={chartWidth - padding.right}
                      y2={y}
                      stroke="#f3f4f6"
                      strokeWidth="1"
                    />
                  );
                })}
                
                {/* Time grid lines */}
                {chartData.map((_, index) => {
                  if (index % 4 === 0) {
                    const x = padding.left + (index / (chartData.length - 1)) * innerWidth;
                    return (
                      <line
                        key={`time-grid-${index}`}
                        x1={x}
                        y1={padding.top}
                        x2={x}
                        y2={chartHeight - padding.bottom}
                        stroke="#f3f4f6"
                        strokeWidth="1"
                      />
                    );
                  }
                  return null;
                })}

                {/* Threshold line */}
                <line
                  x1={padding.left}
                  y1={thresholdY}
                  x2={chartWidth - padding.right}
                  y2={thresholdY}
                  stroke="#ef4444"
                  strokeWidth="2"
                  strokeDasharray="5,5"
                />
                <text
                  x={chartWidth - padding.right - 10}
                  y={thresholdY - 5}
                  textAnchor="end"
                  className="text-xs fill-red-500"
                >
                  Threshold: {formatResponseTime(threshold)}
                </text>

                {/* Response time line */}
                <path
                  d={createPath(responseTimePoints)}
                  fill="none"
                  stroke={domainColor}
                  strokeWidth="2"
                />

                {/* Data points */}
                {responseTimePoints.map((point, index) => (
                  <circle
                    key={index}
                    cx={point.x}
                    cy={point.y}
                    r="3"
                    fill={point.value > threshold ? '#ef4444' : domainColor}
                    className="hover:r-5 cursor-pointer"
                  >
                    <title>
                      {formatTime(point.timestamp)}: {formatResponseTime(point.value)}
                    </title>
                  </circle>
                ))}

                {/* Y-axis labels */}
                {[0, 0.25, 0.5, 0.75, 1].map(ratio => {
                  const y = padding.top + ratio * innerHeight;
                  const value = maxResponseTime * (1 - ratio);
                  return (
                    <text
                      key={`y-label-${ratio}`}
                      x={padding.left - 10}
                      y={y + 4}
                      textAnchor="end"
                      className="text-xs fill-gray-600"
                    >
                      {formatResponseTime(value)}
                    </text>
                  );
                })}

                {/* X-axis labels */}
                {chartData.map((point, index) => {
                  if (index % 4 === 0) {
                    const x = padding.left + (index / (chartData.length - 1)) * innerWidth;
                    return (
                      <text
                        key={`x-label-${index}`}
                        x={x}
                        y={chartHeight - padding.bottom + 15}
                        textAnchor="middle"
                        className="text-xs fill-gray-600"
                      >
                        {formatTime(point.timestamp)}
                      </text>
                    );
                  }
                  return null;
                })}
              </svg>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Request Volume Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">
            {domain} Domain - Request Volume
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center h-48">
              <span className="animate-spin mr-2">⟳</span>
              <span>Loading chart data...</span>
            </div>
          ) : (
            <div className="relative">
              <svg width={chartWidth} height={chartHeight} className="border rounded">
                {/* Grid lines */}
                {[0, 0.25, 0.5, 0.75, 1].map(ratio => {
                  const y = padding.top + ratio * innerHeight;
                  return (
                    <line
                      key={`req-grid-${ratio}`}
                      x1={padding.left}
                      y1={y}
                      x2={chartWidth - padding.right}
                      y2={y}
                      stroke="#f3f4f6"
                      strokeWidth="1"
                    />
                  );
                })}

                {/* Request volume bars */}
                {requestPoints.map((point, index) => {
                  const barWidth = Math.max(1, innerWidth / chartData.length - 2);
                  const barHeight = chartHeight - padding.bottom - point.y;
                  return (
                    <rect
                      key={index}
                      x={point.x - barWidth / 2}
                      y={point.y}
                      width={barWidth}
                      height={barHeight}
                      fill={domainColor}
                      opacity="0.7"
                      className="hover:opacity-100 cursor-pointer"
                    >
                      <title>
                        {formatTime(point.timestamp)}: {point.value} requests
                      </title>
                    </rect>
                  );
                })}

                {/* Y-axis labels */}
                {[0, 0.25, 0.5, 0.75, 1].map(ratio => {
                  const y = padding.top + ratio * innerHeight;
                  const value = Math.round(maxRequests * (1 - ratio));
                  return (
                    <text
                      key={`req-y-label-${ratio}`}
                      x={padding.left - 10}
                      y={y + 4}
                      textAnchor="end"
                      className="text-xs fill-gray-600"
                    >
                      {value}
                    </text>
                  );
                })}

                {/* X-axis labels */}
                {chartData.map((point, index) => {
                  if (index % 4 === 0) {
                    const x = padding.left + (index / (chartData.length - 1)) * innerWidth;
                    return (
                      <text
                        key={`req-x-label-${index}`}
                        x={x}
                        y={chartHeight - padding.bottom + 15}
                        textAnchor="middle"
                        className="text-xs fill-gray-600"
                      >
                        {formatTime(point.timestamp)}
                      </text>
                    );
                  }
                  return null;
                })}
              </svg>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Summary Statistics */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">24-Hour Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: domainColor }}>
                {formatResponseTime(Math.round(chartData.reduce((sum, d) => sum + d.responseTime, 0) / chartData.length))}
              </div>
              <div className="text-sm text-gray-600">Avg Response</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: domainColor }}>
                {formatResponseTime(Math.max(...chartData.map(d => d.responseTime)))}
              </div>
              <div className="text-sm text-gray-600">Peak Response</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold" style={{ color: domainColor }}>
                {chartData.reduce((sum, d) => sum + d.requests, 0).toLocaleString()}
              </div>
              <div className="text-sm text-gray-600">Total Requests</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">
                {chartData.filter(d => d.responseTime > threshold).length}
              </div>
              <div className="text-sm text-gray-600">Threshold Violations</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DomainCharts;