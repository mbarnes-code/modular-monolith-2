/**
 * Cross-Domain Data Visualization Component.
 *
 * Advanced visualization component for displaying data flows and relationships
 * across all 4 domains (Security, Productivity, MTG, Infrastructure) with
 * executive function accommodations.
 */

import { Badge, Button, Slider, Switch } from '@/components/ui';
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
    Database,
    Download,
    Filter,
    GitBranch,
    Network,
    RefreshCw,
    Settings
} from 'lucide-react';
import React, { useCallback, useMemo, useState } from 'react';
import {
    Bar,
    CartesianGrid,
    Cell,
    ComposedChart,
    Legend,
    Line,
    ResponsiveContainer,
    Scatter,
    ScatterChart,
    Tooltip,
    XAxis,
    YAxis
} from 'recharts';

// Types
interface CrossDomainNode {
  id: string;
  name: string;
  domain: 'Security' | 'Productivity' | 'MTG' | 'Infrastructure';
  type: 'tool' | 'data_source' | 'integration_point' | 'user_interface';
  dataVolume: number;
  connections: number;
  lastSyncTime: string;
  healthScore: number;
  x?: number;
  y?: number;
}

interface CrossDomainEdge {
  id: string;
  source: string;
  target: string;
  dataType: string;
  volume: number;
  frequency: 'real-time' | 'hourly' | 'daily' | 'on-demand';
  latency: number;
  successRate: number;
  bidirectional: boolean;
}

interface DataFlow {
  timestamp: string;
  sourceTools: string[];
  targetTools: string[];
  dataTypes: string[];
  volume: number;
  duration: number;
  domains: string[];
}

interface CrossDomainViewProps {
  selectedTimeRange: '1h' | '6h' | '24h' | '7d' | '30d';
  enableRealTimeUpdates: boolean;
  onNodeClick?: (node: CrossDomainNode) => void;
  onEdgeClick?: (edge: CrossDomainEdge) => void;
}

// Mock data
const mockNodes: CrossDomainNode[] = [
  // Security Domain
  {
    id: 'misp',
    name: 'MISP',
    domain: 'Security',
    type: 'tool',
    dataVolume: 245000,
    connections: 8,
    lastSyncTime: '2 min ago',
    healthScore: 95,
    x: 100,
    y: 100,
  },
  {
    id: 'helk',
    name: 'HELK',
    domain: 'Security',
    type: 'tool',
    dataVolume: 890000,
    connections: 12,
    lastSyncTime: '1 min ago',
    healthScore: 92,
    x: 250,
    y: 120,
  },
  {
    id: 'securityonion',
    name: 'SecurityOnion',
    domain: 'Security',
    type: 'tool',
    dataVolume: 1200000,
    connections: 15,
    lastSyncTime: '30 sec ago',
    healthScore: 88,
    x: 400,
    y: 80,
  },
  
  // Productivity Domain
  {
    id: 'n8n',
    name: 'n8n',
    domain: 'Productivity',
    type: 'tool',
    dataVolume: 45000,
    connections: 20,
    lastSyncTime: '1 min ago',
    healthScore: 98,
    x: 100,
    y: 300,
  },
  {
    id: 'mealie',
    name: 'Mealie',
    domain: 'Productivity',
    type: 'tool',
    dataVolume: 12000,
    connections: 3,
    lastSyncTime: '5 min ago',
    healthScore: 97,
    x: 250,
    y: 320,
  },
  {
    id: 'dispatch',
    name: 'Dispatch',
    domain: 'Productivity',
    type: 'tool',
    dataVolume: 78000,
    connections: 7,
    lastSyncTime: '2 min ago',
    healthScore: 94,
    x: 400,
    y: 280,
  },
  
  // MTG Domain
  {
    id: 'commander-spellbook',
    name: 'Commander Spellbook',
    domain: 'MTG',
    type: 'tool',
    dataVolume: 156000,
    connections: 4,
    lastSyncTime: '10 min ago',
    healthScore: 96,
    x: 100,
    y: 500,
  },
  {
    id: 'mtg-commander-map',
    name: 'MTG Commander Map',
    domain: 'MTG',
    type: 'tool',
    dataVolume: 89000,
    connections: 3,
    lastSyncTime: '8 min ago',
    healthScore: 93,
    x: 250,
    y: 520,
  },
  
  // Infrastructure Domain
  {
    id: 'kong',
    name: 'Kong Gateway',
    domain: 'Infrastructure',
    type: 'integration_point',
    dataVolume: 2400000,
    connections: 25,
    lastSyncTime: '15 sec ago',
    healthScore: 91,
    x: 600,
    y: 300,
  },
  {
    id: 'ghostwriter',
    name: 'Ghostwriter',
    domain: 'Infrastructure',
    type: 'tool',
    dataVolume: 67000,
    connections: 5,
    lastSyncTime: '3 min ago',
    healthScore: 89,
    x: 600,
    y: 450,
  },
];

const mockEdges: CrossDomainEdge[] = [
  {
    id: 'misp-helk',
    source: 'misp',
    target: 'helk',
    dataType: 'threat_indicators',
    volume: 15000,
    frequency: 'real-time',
    latency: 250,
    successRate: 98.5,
    bidirectional: true,
  },
  {
    id: 'helk-securityonion',
    source: 'helk',
    target: 'securityonion',
    dataType: 'security_events',
    volume: 45000,
    frequency: 'real-time',
    latency: 180,
    successRate: 97.2,
    bidirectional: false,
  },
  {
    id: 'n8n-dispatch',
    source: 'n8n',
    target: 'dispatch',
    dataType: 'workflow_tasks',
    volume: 8900,
    frequency: 'hourly',
    latency: 500,
    successRate: 99.1,
    bidirectional: true,
  },
  {
    id: 'security-productivity',
    source: 'securityonion',
    target: 'dispatch',
    dataType: 'security_alerts',
    volume: 2300,
    frequency: 'real-time',
    latency: 750,
    successRate: 95.8,
    bidirectional: false,
  },
  {
    id: 'kong-all',
    source: 'kong',
    target: 'misp',
    dataType: 'api_gateway',
    volume: 156000,
    frequency: 'real-time',
    latency: 125,
    successRate: 99.8,
    bidirectional: true,
  },
];

// Domain colors (ADHD-friendly high contrast)
const domainColors = {
  Security: '#ef4444',
  Productivity: '#22c55e',
  MTG: '#8b5cf6',
  Infrastructure: '#f59e0b',
};

const frequencyColors = {
  'real-time': '#22c55e',
  'hourly': '#f59e0b',
  'daily': '#3b82f6',
  'on-demand': '#6b7280',
};

export const CrossDomainView: React.FC<CrossDomainViewProps> = ({
  selectedTimeRange = '24h',
  enableRealTimeUpdates = true,
  onNodeClick,
  onEdgeClick,
}) => {
  const [selectedDomains, setSelectedDomains] = useState<string[]>([
    'Security', 'Productivity', 'MTG', 'Infrastructure'
  ]);
  const [visualizationType, setVisualizationType] = useState<'network' | 'sankey' | 'scatter' | 'flow'>('network');
  const [showDataVolume, setShowDataVolume] = useState(true);
  const [showHealthScores, setShowHealthScores] = useState(true);
  const [nodeSize, setNodeSize] = useState(50);
  const [edgeThickness, setEdgeThickness] = useState(3);

  // Filter nodes and edges based on selected domains
  const filteredNodes = useMemo(() => {
    return mockNodes.filter(node => selectedDomains.includes(node.domain));
  }, [selectedDomains]);

  const filteredEdges = useMemo(() => {
    const nodeIds = new Set(filteredNodes.map(n => n.id));
    return mockEdges.filter(edge => 
      nodeIds.has(edge.source) && nodeIds.has(edge.target)
    );
  }, [filteredNodes]);

  // Calculate domain statistics
  const domainStats = useMemo(() => {
    const stats = selectedDomains.map(domain => {
      const domainNodes = filteredNodes.filter(n => n.domain === domain);
      const totalVolume = domainNodes.reduce((sum, n) => sum + n.dataVolume, 0);
      const avgHealth = domainNodes.reduce((sum, n) => sum + n.healthScore, 0) / domainNodes.length;
      const connections = domainNodes.reduce((sum, n) => sum + n.connections, 0);

      return {
        domain,
        nodeCount: domainNodes.length,
        totalVolume,
        avgHealth: Math.round(avgHealth),
        connections,
        color: domainColors[domain as keyof typeof domainColors],
      };
    });
    return stats;
  }, [filteredNodes, selectedDomains]);

  const handleDomainToggle = useCallback((domain: string) => {
    setSelectedDomains(prev => 
      prev.includes(domain) 
        ? prev.filter(d => d !== domain)
        : [...prev, domain]
    );
  }, []);

  const renderNodeTooltip = useCallback((node: CrossDomainNode) => (
    <div className="bg-white p-3 border rounded-lg shadow-lg max-w-xs">
      <div className="flex items-center gap-2 mb-2">
        <Badge style={{ backgroundColor: domainColors[node.domain] }} className="text-white">
          {node.domain}
        </Badge>
        <span className="font-semibold">{node.name}</span>
      </div>
      <div className="space-y-1 text-sm">
        <div>Type: {node.type.replace('_', ' ')}</div>
        <div>Data Volume: {node.dataVolume.toLocaleString()}</div>
        <div>Connections: {node.connections}</div>
        <div>Health: {node.healthScore}%</div>
        <div>Last Sync: {node.lastSyncTime}</div>
      </div>
    </div>
  ), []);

  const renderEdgeTooltip = useCallback((edge: CrossDomainEdge) => (
    <div className="bg-white p-3 border rounded-lg shadow-lg max-w-xs">
      <div className="font-semibold mb-2">
        {mockNodes.find(n => n.id === edge.source)?.name} → {mockNodes.find(n => n.id === edge.target)?.name}
      </div>
      <div className="space-y-1 text-sm">
        <div>Data Type: {edge.dataType.replace('_', ' ')}</div>
        <div>Volume: {edge.volume.toLocaleString()}</div>
        <div>Frequency: {edge.frequency}</div>
        <div>Latency: {edge.latency}ms</div>
        <div>Success Rate: {edge.successRate}%</div>
      </div>
    </div>
  ), []);

  return (
    <div className="w-full h-full space-y-6 p-6">
      {/* Header with controls */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Cross-Domain Data Visualization</h2>
          <p className="text-gray-600 mt-1">
            Interactive visualization of data flows across all 37 integrated tools
          </p>
        </div>
        
        <div className="flex flex-wrap gap-3">
          <Select value={visualizationType} onValueChange={(value) => setVisualizationType(value as any)}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Visualization type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="network">Network Graph</SelectItem>
              <SelectItem value="sankey">Flow Diagram</SelectItem>
              <SelectItem value="scatter">Scatter Plot</SelectItem>
              <SelectItem value="flow">Data Flow</SelectItem>
            </SelectContent>
          </Select>
          
          <Button variant="outline" size="sm">
            <Settings className="w-4 h-4 mr-2" />
            Settings
          </Button>
          
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
          
          <Button variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Domain filters and stats */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="w-5 h-5" />
            Domain Controls & Statistics
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Domain Toggles */}
            <div>
              <h4 className="font-medium mb-3">Active Domains</h4>
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(domainColors).map(([domain, color]) => (
                  <div key={domain} className="flex items-center gap-3">
                    <Switch 
                      checked={selectedDomains.includes(domain)}
                      onCheckedChange={() => handleDomainToggle(domain)}
                    />
                    <Badge style={{ backgroundColor: color }} className="text-white flex-1">
                      {domain}
                    </Badge>
                  </div>
                ))}
              </div>
            </div>

            {/* Visualization Controls */}
            <div>
              <h4 className="font-medium mb-3">Display Options</h4>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Show Data Volume</span>
                  <Switch checked={showDataVolume} onCheckedChange={setShowDataVolume} />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Show Health Scores</span>
                  <Switch checked={showHealthScores} onCheckedChange={setShowHealthScores} />
                </div>
                <div className="space-y-2">
                  <span className="text-sm">Node Size: {nodeSize}</span>
                  <Slider
                    value={[nodeSize]}
                    onValueChange={(value) => setNodeSize(value[0])}
                    min={20}
                    max={100}
                    step={10}
                    className="w-full"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Domain Statistics */}
          <div className="mt-6">
            <h4 className="font-medium mb-3">Domain Statistics</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {domainStats.map((stat) => (
                <div 
                  key={stat.domain}
                  className="p-4 border rounded-lg"
                  style={{ borderColor: stat.color + '40', backgroundColor: stat.color + '10' }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <Badge style={{ backgroundColor: stat.color }} className="text-white">
                      {stat.domain}
                    </Badge>
                    <span className="text-sm text-gray-600">{stat.nodeCount} tools</span>
                  </div>
                  <div className="space-y-1 text-sm">
                    <div>Volume: {stat.totalVolume.toLocaleString()}</div>
                    <div>Connections: {stat.connections}</div>
                    <div>Avg Health: {stat.avgHealth}%</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Visualization */}
      <Card className="flex-1 min-h-[600px]">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Network className="w-5 h-5" />
            {visualizationType === 'network' && 'Network Graph'}
            {visualizationType === 'sankey' && 'Data Flow Diagram'}
            {visualizationType === 'scatter' && 'Tool Relationship Scatter Plot'}
            {visualizationType === 'flow' && 'Real-time Data Flow'}
          </CardTitle>
        </CardHeader>
        <CardContent className="h-full">
          <ResponsiveContainer width="100%" height={500}>
            {visualizationType === 'network' && (
              <div className="relative w-full h-full border rounded">
                {/* Network visualization would use a proper network library like react-force-graph */}
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <Network className="w-16 h-16 mx-auto text-gray-400 mb-4" />
                    <p className="text-gray-600">Network Graph Visualization</p>
                    <p className="text-sm text-gray-500 mt-2">
                      Interactive network showing {filteredNodes.length} tools with {filteredEdges.length} connections
                    </p>
                  </div>
                </div>
                
                {/* Overlay with node/edge counts */}
                <div className="absolute top-4 left-4 bg-white bg-opacity-90 p-3 rounded-lg border">
                  <div className="text-sm space-y-1">
                    <div>Nodes: {filteredNodes.length}</div>
                    <div>Edges: {filteredEdges.length}</div>
                    <div>Domains: {selectedDomains.length}</div>
                  </div>
                </div>
              </div>
            )}
            
            {visualizationType === 'scatter' && (
              <ScatterChart data={filteredNodes}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="dataVolume" 
                  name="Data Volume"
                  type="number"
                  scale="log"
                  domain={['dataMin', 'dataMax']}
                />
                <YAxis 
                  dataKey="healthScore" 
                  name="Health Score"
                  domain={[80, 100]}
                />
                <Tooltip 
                  content={({ active, payload }) => {
                    if (active && payload && payload[0]) {
                      const node = payload[0].payload as CrossDomainNode;
                      return renderNodeTooltip(node);
                    }
                    return null;
                  }}
                />
                <Scatter 
                  dataKey="connections" 
                  fill={(entry: any) => domainColors[entry.domain as keyof typeof domainColors]}
                >
                  {filteredNodes.map((entry, index) => (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={domainColors[entry.domain]} 
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            )}
            
            {visualizationType === 'flow' && (
              <ComposedChart data={domainStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="domain" />
                <YAxis yAxisId="volume" orientation="left" />
                <YAxis yAxisId="health" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="volume" dataKey="totalVolume" fill="#3b82f6" name="Data Volume" />
                <Line yAxisId="health" type="monotone" dataKey="avgHealth" stroke="#ef4444" name="Avg Health" />
              </ComposedChart>
            )}
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Data Flow Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <GitBranch className="w-5 h-5" />
              Active Data Flows
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {filteredEdges.slice(0, 5).map((edge) => (
                <div key={edge.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex-1">
                    <div className="font-medium text-sm">
                      {mockNodes.find(n => n.id === edge.source)?.name} → {mockNodes.find(n => n.id === edge.target)?.name}
                    </div>
                    <div className="text-xs text-gray-600">
                      {edge.dataType.replace('_', ' ')} • {edge.volume.toLocaleString()} records
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Badge 
                      style={{ backgroundColor: frequencyColors[edge.frequency] }}
                      className="text-white text-xs"
                    >
                      {edge.frequency}
                    </Badge>
                    <span className="text-sm text-gray-600">{edge.latency}ms</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Database className="w-5 h-5" />
              Integration Health
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {domainStats.map((stat) => (
                <div key={stat.domain} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <Badge style={{ backgroundColor: stat.color }} className="text-white">
                      {stat.domain}
                    </Badge>
                    <span className="text-sm font-medium">{stat.avgHealth}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="h-2 rounded-full"
                      style={{ 
                        width: `${stat.avgHealth}%`,
                        backgroundColor: stat.color
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default CrossDomainView;