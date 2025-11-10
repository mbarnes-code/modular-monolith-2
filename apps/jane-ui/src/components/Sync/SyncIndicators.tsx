/**
 * Real-Time Data Synchronization Indicators.
 *
 * Visual indicators and status components for real-time data synchronization
 * across all 37 integrated tools with executive function accommodations.
 */

import {
    Badge,
    Card,
    CardContent,
    Progress,
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from '@/components/ui';
import {
    Activity,
    AlertTriangle,
    ArrowRightLeft,
    CheckCircle,
    Clock,
    Database,
    Pause,
    RefreshCw,
    Wifi,
    WifiOff,
    Zap,
} from 'lucide-react';
import React, { useEffect, useMemo, useState } from 'react';

// Types for sync indicators
interface SyncIndicatorProps {
  toolId: string;
  toolName: string;
  domain: string;
  status: 'synced' | 'syncing' | 'error' | 'offline' | 'pending';
  lastSyncTime?: string;
  progress?: number;
  errorMessage?: string;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

interface DomainSyncStatus {
  domain: string;
  totalTools: number;
  syncedTools: number;
  syncingTools: number;
  errorTools: number;
  offlineTools: number;
  lastUpdate: string;
  healthScore: number;
}

interface NetworkIndicatorProps {
  isOnline: boolean;
  latency?: number;
  quality: 'excellent' | 'good' | 'fair' | 'poor';
  showDetails?: boolean;
}

interface GlobalSyncStatusProps {
  domains: DomainSyncStatus[];
  enableRealTimeUpdates: boolean;
  onToggleRealTime: () => void;
  compact?: boolean;
}

// Individual tool sync indicator
export const SyncIndicator: React.FC<SyncIndicatorProps> = ({
  toolId,
  toolName,
  domain,
  status,
  lastSyncTime = 'Never',
  progress = 0,
  errorMessage,
  size = 'md',
  showLabel = true,
}) => {
  const getStatusIcon = () => {
    const iconSize = size === 'sm' ? 'w-3 h-3' : size === 'lg' ? 'w-6 h-6' : 'w-4 h-4';
    
    switch (status) {
      case 'synced':
        return <CheckCircle className={`${iconSize} text-green-500`} />;
      case 'syncing':
        return <RefreshCw className={`${iconSize} text-blue-500 animate-spin`} />;
      case 'error':
        return <AlertTriangle className={`${iconSize} text-red-500`} />;
      case 'offline':
        return <WifiOff className={`${iconSize} text-gray-400`} />;
      case 'pending':
        return <Clock className={`${iconSize} text-orange-500`} />;
      default:
        return <Activity className={`${iconSize} text-gray-400`} />;
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'synced': return 'bg-green-100 text-green-800 border-green-200';
      case 'syncing': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'error': return 'bg-red-100 text-red-800 border-red-200';
      case 'offline': return 'bg-gray-100 text-gray-600 border-gray-200';
      case 'pending': return 'bg-orange-100 text-orange-800 border-orange-200';
      default: return 'bg-gray-100 text-gray-600 border-gray-200';
    }
  };

  const getTooltipContent = () => (
    <div className="text-sm space-y-1">
      <div className="font-medium">{toolName}</div>
      <div className="text-gray-600">{domain} Domain</div>
      <div>Status: <span className="capitalize">{status}</span></div>
      <div>Last Sync: {lastSyncTime}</div>
      {status === 'syncing' && progress > 0 && (
        <div>Progress: {Math.round(progress)}%</div>
      )}
      {errorMessage && (
        <div className="text-red-600">Error: {errorMessage}</div>
      )}
    </div>
  );

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className={`flex items-center gap-2 ${size === 'sm' ? 'text-xs' : 'text-sm'}`}>
            {getStatusIcon()}
            {showLabel && (
              <div className="flex flex-col">
                <span className="font-medium truncate max-w-24">{toolName}</span>
                {status === 'syncing' && progress > 0 && (
                  <Progress value={progress} className="h-1 w-20" />
                )}
              </div>
            )}
            <Badge 
              className={`${getStatusColor()} ${size === 'sm' ? 'text-xs px-1' : 'text-xs'}`}
              variant="outline"
            >
              {status}
            </Badge>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          {getTooltipContent()}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
};

// Network connection indicator
export const NetworkIndicator: React.FC<NetworkIndicatorProps> = ({
  isOnline,
  latency = 0,
  quality,
  showDetails = false,
}) => {
  const getQualityColor = () => {
    if (!isOnline) return 'text-red-500';
    switch (quality) {
      case 'excellent': return 'text-green-500';
      case 'good': return 'text-blue-500';
      case 'fair': return 'text-orange-500';
      case 'poor': return 'text-red-500';
      default: return 'text-gray-400';
    }
  };

  const getQualityBars = () => {
    if (!isOnline) return 0;
    switch (quality) {
      case 'excellent': return 4;
      case 'good': return 3;
      case 'fair': return 2;
      case 'poor': return 1;
      default: return 0;
    }
  };

  const bars = getQualityBars();

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="flex items-center gap-2">
            {isOnline ? (
              <Wifi className={`w-4 h-4 ${getQualityColor()}`} />
            ) : (
              <WifiOff className="w-4 h-4 text-red-500" />
            )}
            
            {/* Signal strength bars */}
            <div className="flex items-end gap-px">
              {[1, 2, 3, 4].map((bar) => (
                <div
                  key={bar}
                  className={`w-1 bg-current ${
                    bar <= bars ? getQualityColor() : 'text-gray-300'
                  }`}
                  style={{ height: `${bar * 3 + 2}px` }}
                />
              ))}
            </div>

            {showDetails && (
              <div className="text-xs text-gray-600">
                {isOnline ? `${latency}ms` : 'Offline'}
              </div>
            )}
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <div className="text-sm space-y-1">
            <div>Status: {isOnline ? 'Online' : 'Offline'}</div>
            {isOnline && (
              <>
                <div>Quality: {quality}</div>
                <div>Latency: {latency}ms</div>
              </>
            )}
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
};

// Domain sync status overview
export const DomainSyncOverview: React.FC<{ domainStatus: DomainSyncStatus }> = ({
  domainStatus,
}) => {
  const { domain, totalTools, syncedTools, syncingTools, errorTools, offlineTools, healthScore } = domainStatus;

  const getHealthColor = () => {
    if (healthScore >= 95) return 'text-green-600';
    if (healthScore >= 85) return 'text-orange-600';
    return 'text-red-600';
  };

  return (
    <Card className="relative overflow-hidden">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <h4 className="font-medium text-gray-900">{domain} Domain</h4>
          <div className={`text-lg font-bold ${getHealthColor()}`}>
            {healthScore}%
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm text-gray-600">Total Tools:</span>
            <span className="font-medium">{totalTools}</span>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="flex items-center gap-1">
              <CheckCircle className="w-3 h-3 text-green-500" />
              <span>Synced: {syncedTools}</span>
            </div>
            <div className="flex items-center gap-1">
              <RefreshCw className="w-3 h-3 text-blue-500" />
              <span>Syncing: {syncingTools}</span>
            </div>
            <div className="flex items-center gap-1">
              <AlertTriangle className="w-3 h-3 text-red-500" />
              <span>Errors: {errorTools}</span>
            </div>
            <div className="flex items-center gap-1">
              <WifiOff className="w-3 h-3 text-gray-400" />
              <span>Offline: {offlineTools}</span>
            </div>
          </div>

          <div className="mt-3">
            <div className="flex justify-between text-xs text-gray-600 mb-1">
              <span>Health Score</span>
              <span>{healthScore}%</span>
            </div>
            <Progress value={healthScore} className="h-2" />
          </div>
        </div>

        {/* Status indicator overlay */}
        <div className="absolute top-2 right-2">
          {errorTools > 0 ? (
            <AlertTriangle className="w-4 h-4 text-red-500" />
          ) : syncingTools > 0 ? (
            <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />
          ) : (
            <CheckCircle className="w-4 h-4 text-green-500" />
          )}
        </div>
      </CardContent>
    </Card>
  );
};

// Global sync status header
export const GlobalSyncStatus: React.FC<GlobalSyncStatusProps> = ({
  domains,
  enableRealTimeUpdates,
  onToggleRealTime,
  compact = false,
}) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const aggregateStats = useMemo(() => {
    const totalTools = domains.reduce((sum, d) => sum + d.totalTools, 0);
    const syncedTools = domains.reduce((sum, d) => sum + d.syncedTools, 0);
    const syncingTools = domains.reduce((sum, d) => sum + d.syncingTools, 0);
    const errorTools = domains.reduce((sum, d) => sum + d.errorTools, 0);
    const offlineTools = domains.reduce((sum, d) => sum + d.offlineTools, 0);
    const avgHealthScore = domains.reduce((sum, d) => sum + d.healthScore, 0) / domains.length;

    return {
      totalTools,
      syncedTools,
      syncingTools,
      errorTools,
      offlineTools,
      avgHealthScore: Math.round(avgHealthScore),
      syncRate: Math.round((syncedTools / totalTools) * 100),
    };
  }, [domains]);

  if (compact) {
    return (
      <div className="flex items-center gap-4 p-2 bg-gray-50 rounded-lg">
        <div className="flex items-center gap-2">
          <Database className="w-4 h-4 text-blue-600" />
          <span className="text-sm font-medium">
            {aggregateStats.syncedTools}/{aggregateStats.totalTools} Synced
          </span>
        </div>

        {aggregateStats.syncingTools > 0 && (
          <div className="flex items-center gap-1">
            <RefreshCw className="w-3 h-3 text-blue-500 animate-spin" />
            <span className="text-xs text-gray-600">{aggregateStats.syncingTools} syncing</span>
          </div>
        )}

        {aggregateStats.errorTools > 0 && (
          <div className="flex items-center gap-1">
            <AlertTriangle className="w-3 h-3 text-red-500" />
            <span className="text-xs text-red-600">{aggregateStats.errorTools} errors</span>
          </div>
        )}

        <NetworkIndicator
          isOnline={true}
          latency={150}
          quality="good"
          showDetails={false}
        />
      </div>
    );
  }

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-2">
                {enableRealTimeUpdates ? (
                  <Activity className="w-5 h-5 text-green-500 animate-pulse" />
                ) : (
                  <Pause className="w-5 h-5 text-gray-500" />
                )}
                <span className="font-medium">
                  {enableRealTimeUpdates ? 'Real-time Active' : 'Real-time Paused'}
                </span>
              </div>
              
              <button
                onClick={onToggleRealTime}
                className="text-sm text-blue-600 hover:text-blue-700 underline"
              >
                {enableRealTimeUpdates ? 'Pause' : 'Resume'}
              </button>
            </div>

            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <ArrowRightLeft className="w-4 h-4 text-blue-600" />
                <span>{aggregateStats.syncRate}% Synchronized</span>
              </div>

              <div className="flex items-center gap-2">
                <Zap className="w-4 h-4 text-green-600" />
                <span>{aggregateStats.avgHealthScore}% Health</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <NetworkIndicator
              isOnline={true}
              latency={125}
              quality="excellent"
              showDetails={true}
            />

            <div className="text-sm text-gray-600">
              {currentTime.toLocaleTimeString()}
            </div>
          </div>
        </div>

        {/* Progress bar for overall sync status */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>System Synchronization</span>
            <span>{aggregateStats.syncedTools} of {aggregateStats.totalTools} tools</span>
          </div>
          <Progress value={aggregateStats.syncRate} className="h-2" />
        </div>

        {/* Quick stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-green-500" />
            <div>
              <div className="font-medium">{aggregateStats.syncedTools}</div>
              <div className="text-xs text-gray-600">Synchronized</div>
            </div>
          </div>

          {aggregateStats.syncingTools > 0 && (
            <div className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-blue-500 animate-spin" />
              <div>
                <div className="font-medium">{aggregateStats.syncingTools}</div>
                <div className="text-xs text-gray-600">In Progress</div>
              </div>
            </div>
          )}

          {aggregateStats.errorTools > 0 && (
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-red-500" />
              <div>
                <div className="font-medium text-red-600">{aggregateStats.errorTools}</div>
                <div className="text-xs text-gray-600">Errors</div>
              </div>
            </div>
          )}

          {aggregateStats.offlineTools > 0 && (
            <div className="flex items-center gap-2">
              <WifiOff className="w-4 h-4 text-gray-400" />
              <div>
                <div className="font-medium">{aggregateStats.offlineTools}</div>
                <div className="text-xs text-gray-600">Offline</div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default {
  SyncIndicator,
  NetworkIndicator,
  DomainSyncOverview,
  GlobalSyncStatus,
};