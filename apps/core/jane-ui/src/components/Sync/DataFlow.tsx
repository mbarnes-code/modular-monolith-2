/**
 * Data Flow Monitoring Interface.
 *
 * Real-time monitoring and visualization of data synchronization flows
 * across all 37 integrated tools with executive function accommodations.
 */

import {
    Alert,
    AlertDescription,
    Badge,
    Button,
    Progress,
    Switch,
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
    Activity,
    AlertTriangle,
    CheckCircle,
    Clock,
    Database,
    Download,
    Pause,
    Play,
    RefreshCw,
    Settings,
    TrendingUp,
    Zap
} from 'lucide-react';
import React, { useEffect, useMemo, useState } from 'react';
import {
    Area,
    AreaChart,
    CartesianGrid,
    Line,
    LineChart,
    ReferenceLine,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis
} from 'recharts';

// Types
interface SyncJob {
  id: string;
  name: string;
  sourceTool: string;
  targetTool: string;
  sourceDomain: string;
  targetDomain: string;
  status: 'running' | 'completed' | 'failed' | 'queued' | 'paused';
  startTime: string;
  endTime?: string;
  duration: number;
  recordsProcessed: number;
  recordsTotal: number;
  dataType: string;
  errorMessage?: string;
  priority: 'high' | 'medium' | 'low';
}

interface FlowMetrics {
  timestamp: string;
  throughput: number;
  latency: number;
  errorRate: number;
  activeJobs: number;
  queuedJobs: number;
  successRate: number;
}

interface DomainFlowStatus {
  domain: string;
  activeFlows: number;
  totalThroughput: number;
  avgLatency: number;
  errorCount: number;
  healthScore: number;
  lastUpdate: string;
}

interface DataFlowProps {
  refreshInterval?: number;
  enableRealTimeUpdates?: boolean;
  showPerformanceAlerts?: boolean;
}

// Mock data
const mockSyncJobs: SyncJob[] = [
  {
    id: 'sync-001',
    name: 'MISP → HELK Threat Intelligence',
    sourceTool: 'MISP',
    targetTool: 'HELK',
    sourceDomain: 'Security',
    targetDomain: 'Security',
    status: 'running',
    startTime: '2 minutes ago',
    duration: 120000,
    recordsProcessed: 15430,
    recordsTotal: 18500,
    dataType: 'threat_indicators',
    priority: 'high',
  },
  {
    id: 'sync-002',
    name: 'SecurityOnion → Dispatch Alerts',
    sourceTool: 'SecurityOnion',
    targetTool: 'Dispatch',
    sourceDomain: 'Security',
    targetDomain: 'Productivity',
    status: 'completed',
    startTime: '5 minutes ago',
    endTime: '3 minutes ago',
    duration: 95000,
    recordsProcessed: 8700,
    recordsTotal: 8700,
    dataType: 'security_alerts',
    priority: 'high',
  },
  {
    id: 'sync-003',
    name: 'n8n → Mealie Recipe Sync',
    sourceTool: 'n8n',
    targetTool: 'Mealie',
    sourceDomain: 'Productivity',
    targetDomain: 'Productivity',
    status: 'failed',
    startTime: '8 minutes ago',
    duration: 45000,
    recordsProcessed: 234,
    recordsTotal: 1200,
    dataType: 'recipes',
    errorMessage: 'API rate limit exceeded',
    priority: 'medium',
  },
  {
    id: 'sync-004',
    name: 'Commander Spellbook → MTG Map',
    sourceTool: 'Commander Spellbook',
    targetTool: 'MTG Commander Map',
    sourceDomain: 'MTG',
    targetDomain: 'MTG',
    status: 'queued',
    startTime: 'scheduled in 2 minutes',
    duration: 0,
    recordsProcessed: 0,
    recordsTotal: 15600,
    dataType: 'combo_data',
    priority: 'low',
  },
  {
    id: 'sync-005',
    name: 'Kong Gateway → Monitoring',
    sourceTool: 'Kong Gateway',
    targetTool: 'Infrastructure Monitor',
    sourceDomain: 'Infrastructure',
    targetDomain: 'Infrastructure',
    status: 'running',
    startTime: '30 seconds ago',
    duration: 30000,
    recordsProcessed: 45600,
    recordsTotal: 50000,
    dataType: 'api_metrics',
    priority: 'medium',
  },
];

const mockFlowMetrics: FlowMetrics[] = [
  { timestamp: '10:00', throughput: 15400, latency: 250, errorRate: 1.2, activeJobs: 8, queuedJobs: 3, successRate: 98.8 },
  { timestamp: '10:05', throughput: 16800, latency: 280, errorRate: 0.8, activeJobs: 12, queuedJobs: 1, successRate: 99.2 },
  { timestamp: '10:10', throughput: 14200, latency: 320, errorRate: 2.1, activeJobs: 6, queuedJobs: 4, successRate: 97.9 },
  { timestamp: '10:15', throughput: 18900, latency: 190, errorRate: 0.5, activeJobs: 15, queuedJobs: 2, successRate: 99.5 },
  { timestamp: '10:20', throughput: 17300, latency: 240, errorRate: 1.8, activeJobs: 9, queuedJobs: 5, successRate: 98.2 },
  { timestamp: '10:25', throughput: 16100, latency: 210, errorRate: 1.1, activeJobs: 11, queuedJobs: 2, successRate: 98.9 },
  { timestamp: '10:30', throughput: 19500, latency: 180, errorRate: 0.3, activeJobs: 18, queuedJobs: 1, successRate: 99.7 },
];

const mockDomainStatus: DomainFlowStatus[] = [
  {
    domain: 'Security',
    activeFlows: 8,
    totalThroughput: 45600,
    avgLatency: 420,
    errorCount: 3,
    healthScore: 94,
    lastUpdate: '15 seconds ago',
  },
  {
    domain: 'Productivity',
    activeFlows: 12,
    totalThroughput: 23400,
    avgLatency: 680,
    errorCount: 1,
    healthScore: 97,
    lastUpdate: '8 seconds ago',
  },
  {
    domain: 'MTG',
    activeFlows: 3,
    totalThroughput: 8900,
    avgLatency: 1200,
    errorCount: 0,
    healthScore: 99,
    lastUpdate: '22 seconds ago',
  },
  {
    domain: 'Infrastructure',
    activeFlows: 15,
    totalThroughput: 156000,
    avgLatency: 890,
    errorCount: 7,
    healthScore: 91,
    lastUpdate: '5 seconds ago',
  },
];

// Status colors (ADHD-friendly high contrast)
const statusColors = {
  running: '#3b82f6',
  completed: '#22c55e',
  failed: '#ef4444',
  queued: '#f59e0b',
  paused: '#6b7280',
};

const priorityColors = {
  high: '#ef4444',
  medium: '#f59e0b',
  low: '#22c55e',
};

const domainColors = {
  Security: '#ef4444',
  Productivity: '#22c55e',
  MTG: '#8b5cf6',
  Infrastructure: '#f59e0b',
};

export const DataFlow: React.FC<DataFlowProps> = ({
  refreshInterval = 5000,
  enableRealTimeUpdates = true,
  showPerformanceAlerts = true,
}) => {
  const [syncJobs, setSyncJobs] = useState<SyncJob[]>(mockSyncJobs);
  const [flowMetrics, setFlowMetrics] = useState<FlowMetrics[]>(mockFlowMetrics);
  const [domainStatus, setDomainStatus] = useState<DomainFlowStatus[]>(mockDomainStatus);
  const [selectedDomain, setSelectedDomain] = useState<string>('All');
  const [selectedStatus, setSelectedStatus] = useState<string>('All');
  const [isPaused, setIsPaused] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(enableRealTimeUpdates);

  // Auto-refresh data
  useEffect(() => {
    if (!autoRefresh || isPaused) return;

    const interval = setInterval(() => {
      // Simulate real-time updates
      setSyncJobs(prevJobs => 
        prevJobs.map(job => {
          if (job.status === 'running' && job.recordsProcessed < job.recordsTotal) {
            const increment = Math.min(
              Math.floor(Math.random() * 1000) + 100,
              job.recordsTotal - job.recordsProcessed
            );
            return {
              ...job,
              recordsProcessed: job.recordsProcessed + increment,
              duration: job.duration + refreshInterval,
            };
          }
          return job;
        })
      );
    }, refreshInterval);

    return () => clearInterval(interval);
  }, [autoRefresh, isPaused, refreshInterval]);

  // Filter jobs based on selected criteria
  const filteredJobs = useMemo(() => {
    return syncJobs.filter(job => {
      const domainMatch = selectedDomain === 'All' || 
        job.sourceDomain === selectedDomain || 
        job.targetDomain === selectedDomain;
      const statusMatch = selectedStatus === 'All' || job.status === selectedStatus;
      return domainMatch && statusMatch;
    });
  }, [syncJobs, selectedDomain, selectedStatus]);

  // Calculate summary metrics
  const summaryMetrics = useMemo(() => {
    const runningJobs = syncJobs.filter(j => j.status === 'running').length;
    const queuedJobs = syncJobs.filter(j => j.status === 'queued').length;
    const failedJobs = syncJobs.filter(j => j.status === 'failed').length;
    const totalThroughput = domainStatus.reduce((sum, d) => sum + d.totalThroughput, 0);
    const avgHealthScore = domainStatus.reduce((sum, d) => sum + d.healthScore, 0) / domainStatus.length;

    return {
      runningJobs,
      queuedJobs,
      failedJobs,
      totalThroughput,
      avgHealthScore: Math.round(avgHealthScore),
    };
  }, [syncJobs, domainStatus]);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <Activity className="w-4 h-4 animate-pulse" />;
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'failed': return <AlertTriangle className="w-4 h-4" />;
      case 'queued': return <Clock className="w-4 h-4" />;
      case 'paused': return <Pause className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const formatDuration = (ms: number) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  };

  return (
    <div className="w-full space-y-6 p-6">
      {/* Header with controls */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Data Flow Monitoring</h2>
          <p className="text-gray-600 mt-1">
            Real-time synchronization monitoring across all 37 integrated tools
          </p>
        </div>
        
        <div className="flex flex-wrap gap-3">
          <div className="flex items-center gap-2">
            <Switch 
              checked={autoRefresh} 
              onCheckedChange={setAutoRefresh}
            />
            <span className="text-sm">Auto-refresh</span>
          </div>
          
          <Button
            variant={isPaused ? "default" : "outline"}
            size="sm"
            onClick={() => setIsPaused(!isPaused)}
          >
            {isPaused ? <Play className="w-4 h-4 mr-2" /> : <Pause className="w-4 h-4 mr-2" />}
            {isPaused ? 'Resume' : 'Pause'}
          </Button>
          
          <Button variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          
          <Button variant="outline" size="sm">
            <Settings className="w-4 h-4 mr-2" />
            Configure
          </Button>
        </div>
      </div>

      {/* Summary metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <Card className="bg-gradient-to-r from-blue-50 to-blue-100 border-blue-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-blue-600">Running Jobs</p>
                <p className="text-2xl font-bold text-blue-900">{summaryMetrics.runningJobs}</p>
              </div>
              <Activity className="w-8 h-8 text-blue-500 animate-pulse" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-orange-50 to-orange-100 border-orange-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-orange-600">Queued Jobs</p>
                <p className="text-2xl font-bold text-orange-900">{summaryMetrics.queuedJobs}</p>
              </div>
              <Clock className="w-8 h-8 text-orange-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-red-50 to-red-100 border-red-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-red-600">Failed Jobs</p>
                <p className="text-2xl font-bold text-red-900">{summaryMetrics.failedJobs}</p>
              </div>
              <AlertTriangle className="w-8 h-8 text-red-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-green-50 to-green-100 border-green-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-green-600">Throughput</p>
                <p className="text-2xl font-bold text-green-900">
                  {(summaryMetrics.totalThroughput / 1000).toFixed(1)}k
                </p>
              </div>
              <TrendingUp className="w-8 h-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-r from-purple-50 to-purple-100 border-purple-200">
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-purple-600">Health Score</p>
                <p className="text-2xl font-bold text-purple-900">{summaryMetrics.avgHealthScore}%</p>
              </div>
              <CheckCircle className="w-8 h-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance metrics charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Throughput & Latency Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={flowMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis yAxisId="throughput" orientation="left" />
                <YAxis yAxisId="latency" orientation="right" />
                <Tooltip />
                <Line 
                  yAxisId="throughput"
                  type="monotone" 
                  dataKey="throughput" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  name="Throughput"
                />
                <Line 
                  yAxisId="latency"
                  type="monotone" 
                  dataKey="latency" 
                  stroke="#ef4444" 
                  strokeWidth={2}
                  name="Latency (ms)"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Error Rate & Success Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={flowMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Area 
                  type="monotone" 
                  dataKey="successRate" 
                  stackId="1"
                  stroke="#22c55e" 
                  fill="#22c55e"
                  name="Success Rate (%)"
                />
                <Area 
                  type="monotone" 
                  dataKey="errorRate" 
                  stackId="2"
                  stroke="#ef4444" 
                  fill="#ef4444"
                  name="Error Rate (%)"
                />
                <ReferenceLine y={95} stroke="#f59e0b" strokeDasharray="3 3" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Domain status overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="w-5 h-5" />
            Domain Flow Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {domainStatus.map((domain) => (
              <div 
                key={domain.domain}
                className="p-4 border rounded-lg"
                style={{ 
                  borderColor: domainColors[domain.domain as keyof typeof domainColors] + '40',
                  backgroundColor: domainColors[domain.domain as keyof typeof domainColors] + '10'
                }}
              >
                <div className="flex items-center justify-between mb-3">
                  <Badge 
                    style={{ backgroundColor: domainColors[domain.domain as keyof typeof domainColors] }}
                    className="text-white"
                  >
                    {domain.domain}
                  </Badge>
                  <span className="text-sm text-gray-600">{domain.activeFlows} active</span>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>Throughput:</span>
                    <span className="font-medium">{domain.totalThroughput.toLocaleString()}/min</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Avg Latency:</span>
                    <span className="font-medium">{domain.avgLatency}ms</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Errors:</span>
                    <span className={domain.errorCount > 0 ? 'font-medium text-red-600' : 'font-medium text-green-600'}>
                      {domain.errorCount}
                    </span>
                  </div>
                  <div className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span>Health:</span>
                      <span className="font-medium">{domain.healthScore}%</span>
                    </div>
                    <Progress value={domain.healthScore} className="h-2" />
                  </div>
                  <div className="text-xs text-gray-500 mt-2">
                    Updated {domain.lastUpdate}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Active sync jobs */}
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <CardTitle className="flex items-center gap-2">
              <Zap className="w-5 h-5" />
              Active Sync Jobs
            </CardTitle>
            
            <div className="flex gap-3">
              <Select value={selectedDomain} onValueChange={setSelectedDomain}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Domain" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="All">All Domains</SelectItem>
                  <SelectItem value="Security">Security</SelectItem>
                  <SelectItem value="Productivity">Productivity</SelectItem>
                  <SelectItem value="MTG">MTG</SelectItem>
                  <SelectItem value="Infrastructure">Infrastructure</SelectItem>
                </SelectContent>
              </Select>
              
              <Select value={selectedStatus} onValueChange={setSelectedStatus}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="All">All Status</SelectItem>
                  <SelectItem value="running">Running</SelectItem>
                  <SelectItem value="completed">Completed</SelectItem>
                  <SelectItem value="failed">Failed</SelectItem>
                  <SelectItem value="queued">Queued</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredJobs.map((job) => (
              <div key={job.id} className="border rounded-lg p-4">
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <div style={{ color: statusColors[job.status] }}>
                        {getStatusIcon(job.status)}
                      </div>
                      <h4 className="font-medium">{job.name}</h4>
                      <Badge 
                        style={{ backgroundColor: priorityColors[job.priority] }}
                        className="text-white text-xs"
                      >
                        {job.priority}
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Status: </span>
                        <Badge 
                          style={{ backgroundColor: statusColors[job.status] }}
                          className="text-white"
                        >
                          {job.status}
                        </Badge>
                      </div>
                      <div>
                        <span className="text-gray-600">Duration: </span>
                        <span className="font-medium">{formatDuration(job.duration)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Records: </span>
                        <span className="font-medium">
                          {job.recordsProcessed.toLocaleString()} / {job.recordsTotal.toLocaleString()}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-600">Data Type: </span>
                        <span className="font-medium">{job.dataType.replace('_', ' ')}</span>
                      </div>
                    </div>

                    {job.status === 'running' && (
                      <div className="mt-3">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm text-gray-600">Progress</span>
                          <span className="text-sm font-medium">
                            {Math.round((job.recordsProcessed / job.recordsTotal) * 100)}%
                          </span>
                        </div>
                        <Progress 
                          value={(job.recordsProcessed / job.recordsTotal) * 100} 
                          className="h-2"
                        />
                      </div>
                    )}

                    {job.errorMessage && (
                      <Alert className="mt-3">
                        <AlertTriangle className="h-4 w-4" />
                        <AlertDescription>{job.errorMessage}</AlertDescription>
                      </Alert>
                    )}
                  </div>
                  
                  <div className="flex gap-2">
                    {job.status === 'running' && (
                      <Button variant="outline" size="sm">
                        <Pause className="w-4 h-4 mr-2" />
                        Pause
                      </Button>
                    )}
                    {job.status === 'failed' && (
                      <Button variant="outline" size="sm">
                        <RefreshCw className="w-4 h-4 mr-2" />
                        Retry
                      </Button>
                    )}
                    <Button variant="outline" size="sm">
                      <Download className="w-4 h-4 mr-2" />
                      Logs
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Performance alerts */}
      {showPerformanceAlerts && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5" />
              Performance Alerts
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {domainStatus
                .filter(d => d.healthScore < 95 || d.errorCount > 5)
                .map((domain) => (
                  <Alert key={domain.domain} className="border-orange-200 bg-orange-50">
                    <AlertTriangle className="h-4 w-4 text-orange-600" />
                    <AlertDescription>
                      <strong>{domain.domain} Domain:</strong> 
                      {domain.healthScore < 95 && ` Health score below threshold (${domain.healthScore}%)`}
                      {domain.errorCount > 5 && ` High error count (${domain.errorCount} errors)`}
                    </AlertDescription>
                  </Alert>
                ))}
              
              {domainStatus.every(d => d.healthScore >= 95 && d.errorCount <= 5) && (
                <Alert className="border-green-200 bg-green-50">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                  <AlertDescription>
                    All domains are operating within normal parameters.
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default DataFlow;