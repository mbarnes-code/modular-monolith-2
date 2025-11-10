/**
 * Unified Insights Page.
 *
 * Central insights page that consolidates data visualization and monitoring
 * across all 37 integrated tools with executive function accommodations.
 */

import {
    CrossDomainView,
} from '@/components/Data';
import {
    InsightsDashboard,
} from '@/components/Insights';
import {
    DataFlow,
} from '@/components/Sync';
import { Alert, AlertDescription, Button } from '@/components/ui';
import { Card, CardContent } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
    Activity,
    AlertTriangle,
    BarChart3,
    CheckCircle,
    Database,
    Download,
    Network,
    RefreshCw,
    Settings,
    TrendingUp,
} from 'lucide-react';
import { NextPage } from 'next';
import Head from 'next/head';
import { useEffect, useState } from 'react';

// Types for page-level state management
interface InsightsPageState {
  selectedTimeRange: '1h' | '6h' | '24h' | '7d' | '30d';
  selectedDomains: string[];
  enableRealTimeUpdates: boolean;
  showPerformanceAlerts: boolean;
  lastRefresh: Date;
}

interface SystemHealth {
  overallHealth: number;
  domainsOnline: number;
  totalDomains: number;
  activeSyncJobs: number;
  errorCount: number;
  lastUpdate: string;
}

const InsightsPage: NextPage = () => {
  const [pageState, setPageState] = useState<InsightsPageState>({
    selectedTimeRange: '24h',
    selectedDomains: ['Security', 'Productivity', 'MTG', 'Infrastructure'],
    enableRealTimeUpdates: true,
    showPerformanceAlerts: true,
    lastRefresh: new Date(),
  });

  const [systemHealth, setSystemHealth] = useState<SystemHealth>({
    overallHealth: 94,
    domainsOnline: 4,
    totalDomains: 4,
    activeSyncJobs: 12,
    errorCount: 3,
    lastUpdate: 'Just now',
  });

  const [isLoading, setIsLoading] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'connecting' | 'disconnected'>('connected');

  // Auto-refresh system health data
  useEffect(() => {
    if (!pageState.enableRealTimeUpdates) return;

    const interval = setInterval(async () => {
      try {
        setConnectionStatus('connecting');
        // In real implementation, this would fetch from the API
        // const response = await fetch('/api/system/health');
        // const healthData = await response.json();
        
        // Mock update for demonstration
        setSystemHealth(prev => ({
          ...prev,
          overallHealth: Math.max(85, Math.min(99, prev.overallHealth + (Math.random() - 0.5) * 4)),
          activeSyncJobs: Math.max(0, prev.activeSyncJobs + Math.floor((Math.random() - 0.5) * 6)),
          errorCount: Math.max(0, prev.errorCount + Math.floor((Math.random() - 0.7) * 3)),
          lastUpdate: new Date().toLocaleTimeString(),
        }));
        
        setPageState(prev => ({ ...prev, lastRefresh: new Date() }));
        setConnectionStatus('connected');
      } catch (error) {
        console.error('Failed to refresh system health:', error);
        setConnectionStatus('disconnected');
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [pageState.enableRealTimeUpdates]);

  const handleRefresh = async () => {
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setPageState(prev => ({ ...prev, lastRefresh: new Date() }));
      setConnectionStatus('connected');
    } catch (error) {
      console.error('Failed to refresh data:', error);
      setConnectionStatus('disconnected');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTimeRangeChange = (timeRange: string) => {
    setPageState(prev => ({
      ...prev,
      selectedTimeRange: timeRange as InsightsPageState['selectedTimeRange'],
    }));
  };

  const toggleRealTimeUpdates = () => {
    setPageState(prev => ({
      ...prev,
      enableRealTimeUpdates: !prev.enableRealTimeUpdates,
    }));
  };

  const getHealthStatusColor = (health: number) => {
    if (health >= 95) return 'text-green-600';
    if (health >= 85) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConnectionStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'connecting':
        return <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />;
      case 'disconnected':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
    }
  };

  return (
    <>
      <Head>
        <title>Unified Insights - Mental Prosthetic Platform</title>
        <meta 
          name="description" 
          content="Comprehensive insights dashboard for all 37 integrated executive function tools with real-time monitoring and analytics." 
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header Section */}
        <div className="bg-white border-b border-gray-200 shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center py-6 gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
                  <BarChart3 className="w-8 h-8 text-blue-600" />
                  Unified Insights
                </h1>
                <p className="text-gray-600 mt-2 max-w-2xl">
                  Comprehensive analytics and monitoring across all 37 integrated tools 
                  with executive function accommodations and real-time data synchronization.
                </p>
              </div>

              {/* Control Panel */}
              <div className="flex flex-wrap items-center gap-4">
                <div className="flex items-center gap-2">
                  {getConnectionStatusIcon()}
                  <span className="text-sm text-gray-600">
                    {connectionStatus === 'connected' && 'Connected'}
                    {connectionStatus === 'connecting' && 'Connecting...'}
                    {connectionStatus === 'disconnected' && 'Disconnected'}
                  </span>
                </div>

                <Select value={pageState.selectedTimeRange} onValueChange={handleTimeRangeChange}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Time range" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1h">Last Hour</SelectItem>
                    <SelectItem value="6h">Last 6 Hours</SelectItem>
                    <SelectItem value="24h">Last 24 Hours</SelectItem>
                    <SelectItem value="7d">Last 7 Days</SelectItem>
                    <SelectItem value="30d">Last 30 Days</SelectItem>
                  </SelectContent>
                </Select>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={toggleRealTimeUpdates}
                  className={pageState.enableRealTimeUpdates ? 'bg-green-50 border-green-200' : ''}
                >
                  <Activity className="w-4 h-4 mr-2" />
                  {pageState.enableRealTimeUpdates ? 'Live' : 'Paused'}
                </Button>

                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleRefresh}
                  disabled={isLoading}
                >
                  <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
                  Refresh
                </Button>

                <Button variant="outline" size="sm">
                  <Download className="w-4 h-4 mr-2" />
                  Export
                </Button>

                <Button variant="outline" size="sm">
                  <Settings className="w-4 h-4 mr-2" />
                  Settings
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* System Health Banner */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
            <CardContent className="p-4">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div className="flex items-center gap-6">
                  <div className="flex items-center gap-2">
                    <div className={`text-2xl font-bold ${getHealthStatusColor(systemHealth.overallHealth)}`}>
                      {systemHealth.overallHealth}%
                    </div>
                    <div className="text-sm text-gray-600">System Health</div>
                  </div>

                  <div className="flex items-center gap-2">
                    <Database className="w-5 h-5 text-blue-600" />
                    <div className="text-sm">
                      <span className="font-medium">{systemHealth.domainsOnline}/{systemHealth.totalDomains}</span>
                      <span className="text-gray-600 ml-1">Domains Online</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-green-600" />
                    <div className="text-sm">
                      <span className="font-medium">{systemHealth.activeSyncJobs}</span>
                      <span className="text-gray-600 ml-1">Active Syncs</span>
                    </div>
                  </div>

                  {systemHealth.errorCount > 0 && (
                    <div className="flex items-center gap-2">
                      <AlertTriangle className="w-5 h-5 text-red-600" />
                      <div className="text-sm">
                        <span className="font-medium text-red-600">{systemHealth.errorCount}</span>
                        <span className="text-gray-600 ml-1">Errors</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="text-sm text-gray-500">
                  Last updated: {systemHealth.lastUpdate}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Performance Alerts */}
        {pageState.showPerformanceAlerts && systemHealth.errorCount > 0 && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-4">
            <Alert className="border-orange-200 bg-orange-50">
              <AlertTriangle className="h-4 w-4 text-orange-600" />
              <AlertDescription>
                <strong>Performance Alert:</strong> {systemHealth.errorCount} errors detected across domains. 
                Check the Data Flow monitoring tab for detailed information.
              </AlertDescription>
            </Alert>
          </div>
        )}

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-8">
          <Tabs defaultValue="dashboard" className="space-y-6">
            <TabsList className="grid w-full grid-cols-3 lg:w-auto lg:grid-cols-3">
              <TabsTrigger value="dashboard" className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                <span className="hidden sm:inline">Dashboard</span>
              </TabsTrigger>
              <TabsTrigger value="cross-domain" className="flex items-center gap-2">
                <Network className="w-4 h-4" />
                <span className="hidden sm:inline">Cross-Domain</span>
              </TabsTrigger>
              <TabsTrigger value="data-flow" className="flex items-center gap-2">
                <Activity className="w-4 h-4" />
                <span className="hidden sm:inline">Data Flow</span>
              </TabsTrigger>
            </TabsList>

            {/* Dashboard Tab */}
            <TabsContent value="dashboard" className="space-y-6">
              <InsightsDashboard
                timeRange={pageState.selectedTimeRange}
                selectedDomains={pageState.selectedDomains}
                refreshInterval={pageState.enableRealTimeUpdates ? 30000 : undefined}
              />
            </TabsContent>

            {/* Cross-Domain Visualization Tab */}
            <TabsContent value="cross-domain" className="space-y-6">
              <CrossDomainView
                selectedTimeRange={pageState.selectedTimeRange}
                enableRealTimeUpdates={pageState.enableRealTimeUpdates}
              />
            </TabsContent>

            {/* Data Flow Monitoring Tab */}
            <TabsContent value="data-flow" className="space-y-6">
              <DataFlow
                refreshInterval={pageState.enableRealTimeUpdates ? 5000 : undefined}
                enableRealTimeUpdates={pageState.enableRealTimeUpdates}
                showPerformanceAlerts={pageState.showPerformanceAlerts}
              />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </>
  );
};

export default InsightsPage;