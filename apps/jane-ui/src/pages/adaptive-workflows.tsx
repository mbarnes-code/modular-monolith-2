/**
 * Adaptive Workflows Main Page
 * 
 * Dashboard for managing n8n adaptive workflows with pattern detection,
 * workflow generation, and performance monitoring.
 */

import {
    Activity,
    Alert,
    AlertDescription,
    AlertTriangle,
    Badge,
    BarChart3,
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CheckCircle,
    Clock,
    Plus,
    Progress,
    RefreshCw,
    Separator,
    Settings,
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
    TrendingUp,
    Users,
    Zap
} from '@/components/ui';
import React, { useEffect, useState } from 'react';

import { PatternDashboard } from '../components/AdaptiveWorkflows/PatternDashboard';
import { WorkflowBuilder } from '../components/AdaptiveWorkflows/WorkflowBuilder';
import { WorkflowTester } from '../components/AdaptiveWorkflows/WorkflowTester';

interface WorkflowStats {
  total_workflows: number;
  active_workflows: number;
  patterns_detected: number;
  automation_rate: number;
  average_success_rate: number;
  total_executions: number;
}

interface RecentActivity {
  id: string;
  type: 'pattern_detected' | 'workflow_generated' | 'workflow_activated' | 'workflow_executed';
  title: string;
  description: string;
  timestamp: string;
  success?: boolean;
}

const AdaptiveWorkflowsPage: React.FC = () => {
  const [stats, setStats] = useState<WorkflowStats | null>(null);
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [selectedPattern, setSelectedPattern] = useState<string | null>(null);
  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadDashboardData();
    
    // Set up real-time updates
    const interval = setInterval(() => {
      loadDashboardData();
    }, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setError(null);
      
      // Load statistics
      const statsResponse = await fetch('/api/adaptive-workflows/stats');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }

      // Load recent activity
      const activityResponse = await fetch('/api/adaptive-workflows/activity?limit=10');
      if (activityResponse.ok) {
        const activityData = await activityResponse.json();
        setRecentActivity(activityData);
      }

    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard load error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePatternSelect = (patternId: string) => {
    setSelectedPattern(patternId);
    setActiveTab('builder');
  };

  const handleWorkflowSelect = (workflowId: string) => {
    setSelectedWorkflow(workflowId);
    setActiveTab('tester');
  };

  const getActivityIcon = (type: RecentActivity['type']) => {
    switch (type) {
      case 'pattern_detected':
        return <Activity className="h-4 w-4 text-blue-600" />;
      case 'workflow_generated':
        return <Plus className="h-4 w-4 text-green-600" />;
      case 'workflow_activated':
        return <CheckCircle className="h-4 w-4 text-purple-600" />;
      case 'workflow_executed':
        return <Zap className="h-4 w-4 text-orange-600" />;
      default:
        return <Activity className="h-4 w-4 text-gray-600" />;
    }
  };

  const formatTimeAgo = (timestamp: string): string => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffMs = now.getTime() - time.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
  };

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
            <p className="text-lg font-medium">Loading Adaptive Workflows...</p>
            <p className="text-sm text-gray-600">Analyzing patterns and workflows</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8 space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Adaptive Workflows</h1>
          <p className="text-gray-600 mt-1">
            AI-powered workflow automation based on user behavior patterns
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadDashboardData}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
          <Button>
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </Button>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Statistics Overview */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-6">
          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-blue-600" />
                <div>
                  <p className="text-sm text-gray-600">Total Workflows</p>
                  <p className="text-2xl font-bold text-blue-600">
                    {stats.total_workflows}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-green-600" />
                <div>
                  <p className="text-sm text-gray-600">Active</p>
                  <p className="text-2xl font-bold text-green-600">
                    {stats.active_workflows}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center gap-2">
                <Activity className="h-5 w-5 text-purple-600" />
                <div>
                  <p className="text-sm text-gray-600">Patterns</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {stats.patterns_detected}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-orange-600" />
                <div>
                  <p className="text-sm text-gray-600">Automation Rate</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {Math.round(stats.automation_rate * 100)}%
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-teal-600" />
                <div>
                  <p className="text-sm text-gray-600">Success Rate</p>
                  <p className="text-2xl font-bold text-teal-600">
                    {Math.round(stats.average_success_rate * 100)}%
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-4">
              <div className="flex items-center gap-2">
                <Users className="h-5 w-5 text-indigo-600" />
                <div>
                  <p className="text-sm text-gray-600">Executions</p>
                  <p className="text-2xl font-bold text-indigo-600">
                    {stats.total_executions.toLocaleString()}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="patterns">Patterns</TabsTrigger>
          <TabsTrigger value="builder">Builder</TabsTrigger>
          <TabsTrigger value="tester">Tester</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Recent Activity */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Clock className="h-5 w-5" />
                    Recent Activity
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {recentActivity.length > 0 ? (
                    <div className="space-y-4">
                      {recentActivity.map((activity) => (
                        <div key={activity.id} className="flex items-start gap-3 p-3 rounded-lg border">
                          <div className="mt-1">
                            {getActivityIcon(activity.type)}
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center justify-between">
                              <h4 className="font-medium text-sm">{activity.title}</h4>
                              <span className="text-xs text-gray-500">
                                {formatTimeAgo(activity.timestamp)}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600 mt-1">
                              {activity.description}
                            </p>
                            {activity.success !== undefined && (
                              <Badge
                                variant={activity.success ? "default" : "destructive"}
                                className="mt-2 text-xs"
                              >
                                {activity.success ? 'Success' : 'Failed'}
                              </Badge>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <Activity className="h-12 w-12 mx-auto mb-4 opacity-50" />
                      <p>No recent activity</p>
                      <p className="text-sm">Start using tools to see automation opportunities</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Quick Actions */}
            <div>
              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setActiveTab('patterns')}
                  >
                    <Activity className="h-4 w-4 mr-2" />
                    View Patterns
                  </Button>
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setActiveTab('builder')}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Create Workflow
                  </Button>
                  <Button 
                    className="w-full justify-start" 
                    variant="outline"
                    onClick={() => setActiveTab('tester')}
                  >
                    <CheckCircle className="h-4 w-4 mr-2" />
                    Test Workflows
                  </Button>
                  <Separator />
                  <div className="space-y-2">
                    <h4 className="text-sm font-medium">System Status</h4>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Pattern Detection</span>
                      <Badge variant="default" className="text-xs">
                        Active
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">n8n Integration</span>
                      <Badge variant="default" className="text-xs">
                        Connected
                      </Badge>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Workflow Engine</span>
                      <Badge variant="default" className="text-xs">
                        Running
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Performance Overview */}
          {stats && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Performance Overview
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <h4 className="text-sm font-medium mb-2">Automation Efficiency</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Success Rate</span>
                        <span>{Math.round(stats.average_success_rate * 100)}%</span>
                      </div>
                      <Progress value={stats.average_success_rate * 100} />
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">Pattern Recognition</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Active Patterns</span>
                        <span>{stats.patterns_detected}</span>
                      </div>
                      <Progress value={(stats.patterns_detected / Math.max(stats.total_workflows, 1)) * 100} />
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="text-sm font-medium mb-2">Workflow Adoption</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Active Workflows</span>
                        <span>{Math.round(stats.automation_rate * 100)}%</span>
                      </div>
                      <Progress value={stats.automation_rate * 100} />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Patterns Tab */}
        <TabsContent value="patterns">
          <PatternDashboard onPatternSelect={handlePatternSelect} />
        </TabsContent>

        {/* Builder Tab */}
        <TabsContent value="builder">
          {selectedPattern ? (
            <WorkflowBuilder
              patternId={selectedPattern}
              onWorkflowGenerated={(workflowId) => {
                setSelectedWorkflow(workflowId);
                setActiveTab('tester');
              }}
              onBack={() => {
                setSelectedPattern(null);
                setActiveTab('patterns');
              }}
            />
          ) : (
            <Card>
              <CardContent className="pt-6">
                <div className="text-center text-gray-500">
                  <Plus className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="text-lg font-medium">No Pattern Selected</p>
                  <p className="text-sm mb-4">
                    Select a pattern from the Patterns tab to generate a workflow
                  </p>
                  <Button onClick={() => setActiveTab('patterns')}>
                    View Patterns
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Tester Tab */}
        <TabsContent value="tester">
          {selectedWorkflow ? (
            <WorkflowTester
              workflowId={selectedWorkflow}
              workflowName={`Workflow ${selectedWorkflow}`}
              onValidationComplete={(result) => {
                console.log('Validation complete:', result);
                // Handle validation results
              }}
            />
          ) : (
            <Card>
              <CardContent className="pt-6">
                <div className="text-center text-gray-500">
                  <CheckCircle className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="text-lg font-medium">No Workflow Selected</p>
                  <p className="text-sm mb-4">
                    Generate a workflow from the Builder tab to test it
                  </p>
                  <Button onClick={() => setActiveTab('builder')}>
                    Create Workflow
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdaptiveWorkflowsPage;