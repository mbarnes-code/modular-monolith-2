/**
 * Unified Insights Dashboard Components.
 *
 * React components for displaying cross-tool data insights and analytics
 * across all 37 integrated tools with executive function accommodations.
 */

import {
    Alert,
    AlertDescription,
    Badge,
    Button,
    Progress,
} from '@/components/ui';
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select';
import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from '@/components/ui/tabs';
import {
    Activity,
    AlertCircle,
    CheckCircle,
    Clock,
    Database,
    TrendingUp,
    Zap
} from 'lucide-react';
import React, { useMemo, useState } from 'react';
import {
    Bar,
    BarChart,
    CartesianGrid,
    Cell,
    Line,
    LineChart,
    Pie,
    PieChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts';

// Types
interface DomainMetrics {
  domain: string;
  toolCount: number;
  activeTools: number;
  syncJobs: number;
  dataVolume: number;
  averageResponseTime: number;
  errorRate: number;
  healthScore: number;
}

interface ToolInsight {
  toolId: string;
  toolName: string;
  domain: string;
  status: 'healthy' | 'warning' | 'error' | 'offline';
  lastSyncTime: string;
  dataEntries: number;
  syncSuccess: number;
  errorCount: number;
  responseTime: number;
}

interface SyncActivity {
  timestamp: string;
  sourceTools: string[];
  targetTools: string[];
  recordCount: number;
  duration: number;
  success: boolean;
  errorMessage?: string;
}

interface InsightsDashboardProps {
  timeRange: '1h' | '6h' | '24h' | '7d' | '30d';
  selectedDomains: string[];
  refreshInterval?: number;
}

// Mock data - would be replaced with actual API calls
const mockDomainMetrics: DomainMetrics[] = [
  {
    domain: 'Security',
    toolCount: 13,
    activeTools: 12,
    syncJobs: 45,
    dataVolume: 2847563,
    averageResponseTime: 850,
    errorRate: 2.1,
    healthScore: 94,
  },
  {
    domain: 'Productivity',
    toolCount: 8,
    activeTools: 8,
    syncJobs: 23,
    dataVolume: 156789,
    averageResponseTime: 1200,
    errorRate: 0.8,
    healthScore: 98,
  },
  {
    domain: 'MTG',
    toolCount: 4,
    activeTools: 4,
    syncJobs: 12,
    dataVolume: 89234,
    averageResponseTime: 2100,
    errorRate: 1.2,
    healthScore: 96,
  },
  {
    domain: 'Infrastructure',
    toolCount: 12,
    activeTools: 11,
    syncJobs: 67,
    dataVolume: 3456789,
    averageResponseTime: 3500,
    errorRate: 4.2,
    healthScore: 87,
  },
];

const mockToolInsights: ToolInsight[] = [
  {
    toolId: 'misp',
    toolName: 'MISP',
    domain: 'Security',
    status: 'healthy',
    lastSyncTime: '2 minutes ago',
    dataEntries: 15432,
    syncSuccess: 98.5,
    errorCount: 2,
    responseTime: 650,
  },
  {
    toolId: 'helk',
    toolName: 'HELK',
    domain: 'Security',
    status: 'warning',
    lastSyncTime: '15 minutes ago',
    dataEntries: 98765,
    syncSuccess: 95.2,
    errorCount: 8,
    responseTime: 1200,
  },
  // Add more mock tools...
];

// Color schemes for domains (ADHD-friendly high contrast)
const domainColors = {
  Security: '#ef4444', // Red
  Productivity: '#22c55e', // Green
  MTG: '#8b5cf6', // Purple
  Infrastructure: '#f59e0b', // Orange
};

const statusColors = {
  healthy: '#22c55e',
  warning: '#f59e0b',
  error: '#ef4444',
  offline: '#6b7280',
};

export const InsightsDashboard: React.FC<InsightsDashboardProps> = ({
  timeRange = '24h',
  selectedDomains = ['Security', 'Productivity', 'MTG', 'Infrastructure'],
  refreshInterval = 30000,
}) => {
  const [metrics, setMetrics] = useState<DomainMetrics[]>(mockDomainMetrics);
  const [toolInsights, setToolInsights] = useState<ToolInsight[]>(mockToolInsights);
  const [syncActivity, setSyncActivity] = useState<SyncActivity[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<string>('All');
  const [loading, setLoading] = useState(false);

  // Filter data based on selected domains
  const filteredMetrics = useMemo(() => {
    if (selectedDomain === 'All') return metrics;
    return metrics.filter(m => m.domain === selectedDomain);
  }, [metrics, selectedDomain]);

  const filteredTools = useMemo(() => {
    if (selectedDomain === 'All') return toolInsights;
    return toolInsights.filter(t => t.domain === selectedDomain);
  }, [toolInsights, selectedDomain]);

  // Calculate summary statistics
  const summaryStats = useMemo(() => {
    const totalTools = filteredMetrics.reduce((sum, m) => sum + m.toolCount, 0);
    const activeTools = filteredMetrics.reduce((sum, m) => sum + m.activeTools, 0);
    const totalSyncs = filteredMetrics.reduce((sum, m) => sum + m.syncJobs, 0);
    const avgHealthScore = filteredMetrics.reduce((sum, m) => sum + m.healthScore, 0) / filteredMetrics.length;
    
    return {
      totalTools,
      activeTools,
      totalSyncs,
      avgHealthScore: Math.round(avgHealthScore),
      uptime: Math.round((activeTools / totalTools) * 100),
    };
  }, [filteredMetrics]);

  return (
    <div className="w-full space-y-6 p-6">
      {/* Header with controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Unified Insights Dashboard</h1>
          <p className="text-gray-600 mt-2">
            Cross-tool analytics and data flow monitoring across all 37 integrated tools
          </p>
        </div>
        
        <div className="flex gap-3">
          <Select value={selectedDomain} onValueChange={setSelectedDomain}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Select domain" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="All">All Domains</SelectItem>
              <SelectItem value="Security">Security</SelectItem>
              <SelectItem value="Productivity">Productivity</SelectItem>
              <SelectItem value="MTG">MTG</SelectItem>
              <SelectItem value="Infrastructure">Infrastructure</SelectItem>
            </SelectContent>
          </Select>
          
          <Button 
            variant="outline" 
            onClick={() => {/* Refresh data */}}
            className="px-4"
          >
            <Activity className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card className="bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">Total Tools</p>
                <p className="text-2xl font-bold text-blue-900">{summaryStats.totalTools}</p>
              </div>
              <Database className="w-8 h-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-green-50 to-green-100 border-green-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Active Tools</p>
                <p className="text-2xl font-bold text-green-900">{summaryStats.activeTools}</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600">Sync Jobs</p>
                <p className="text-2xl font-bold text-purple-900">{summaryStats.totalSyncs}</p>
              </div>
              <Zap className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-orange-50 to-orange-100 border-orange-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">Health Score</p>
                <p className="text-2xl font-bold text-orange-900">{summaryStats.avgHealthScore}%</p>
              </div>
              <TrendingUp className="w-8 h-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-indigo-50 to-indigo-100 border-indigo-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-indigo-600">Uptime</p>
                <p className="text-2xl font-bold text-indigo-900">{summaryStats.uptime}%</p>
              </div>
              <Clock className="w-8 h-8 text-indigo-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Dashboard Tabs */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="performance">Performance</TabsTrigger>
          <TabsTrigger value="sync-activity">Sync Activity</TabsTrigger>
          <TabsTrigger value="tools">Tool Status</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Domain Health Overview */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="w-5 h-5" />
                  Domain Health Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={filteredMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="domain" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="healthScore" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Tool Distribution */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="w-5 h-5" />
                  Tool Distribution by Domain
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={filteredMetrics}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="toolCount"
                      nameKey="domain"
                    >
                      {filteredMetrics.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={domainColors[entry.domain as keyof typeof domainColors]} 
                        />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Domain Metrics Table */}
          <Card>
            <CardHeader>
              <CardTitle>Domain Performance Metrics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-2">Domain</th>
                      <th className="text-left p-2">Tools</th>
                      <th className="text-left p-2">Active</th>
                      <th className="text-left p-2">Sync Jobs</th>
                      <th className="text-left p-2">Data Volume</th>
                      <th className="text-left p-2">Avg Response</th>
                      <th className="text-left p-2">Error Rate</th>
                      <th className="text-left p-2">Health</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredMetrics.map((metric) => (
                      <tr key={metric.domain} className="border-b hover:bg-gray-50">
                        <td className="p-2">
                          <Badge 
                            style={{ backgroundColor: domainColors[metric.domain as keyof typeof domainColors] }}
                            className="text-white"
                          >
                            {metric.domain}
                          </Badge>
                        </td>
                        <td className="p-2">{metric.toolCount}</td>
                        <td className="p-2">{metric.activeTools}</td>
                        <td className="p-2">{metric.syncJobs}</td>
                        <td className="p-2">{metric.dataVolume.toLocaleString()}</td>
                        <td className="p-2">{metric.averageResponseTime}ms</td>
                        <td className="p-2">
                          <span className={metric.errorRate > 3 ? 'text-red-600' : 'text-green-600'}>
                            {metric.errorRate}%
                          </span>
                        </td>
                        <td className="p-2">
                          <div className="flex items-center gap-2">
                            <Progress value={metric.healthScore} className="w-16" />
                            <span className="text-sm">{metric.healthScore}%</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Performance Tab */}
        <TabsContent value="performance" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Response Time Trends */}
            <Card>
              <CardHeader>
                <CardTitle>Response Time Trends</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={filteredMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="domain" />
                    <YAxis />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="averageResponseTime" 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Error Rate Analysis */}
            <Card>
              <CardHeader>
                <CardTitle>Error Rate by Domain</CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={filteredMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="domain" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="errorRate" fill="#ef4444" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Tool Status Tab */}
        <TabsContent value="tools" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredTools.map((tool) => (
              <Card key={tool.toolId} className="relative">
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg">{tool.toolName}</CardTitle>
                    <Badge 
                      style={{ backgroundColor: statusColors[tool.status] }}
                      className="text-white"
                    >
                      {tool.status}
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">{tool.domain} Domain</p>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span>Last Sync:</span>
                    <span className="font-medium">{tool.lastSyncTime}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Data Entries:</span>
                    <span className="font-medium">{tool.dataEntries.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Success Rate:</span>
                    <span className="font-medium text-green-600">{tool.syncSuccess}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Response Time:</span>
                    <span className="font-medium">{tool.responseTime}ms</span>
                  </div>
                  {tool.errorCount > 0 && (
                    <Alert className="mt-3">
                      <AlertCircle className="h-4 w-4" />
                      <AlertDescription>
                        {tool.errorCount} errors in last hour
                      </AlertDescription>
                    </Alert>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default InsightsDashboard;