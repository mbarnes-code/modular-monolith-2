'use client';
/* eslint-disable no-undef */

import { useEffect, useState } from 'react';

interface MobileDashboardProps {
  className?: string;
}

interface ToolStatus {
  id: string;
  name: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure';
  status: 'active' | 'idle' | 'offline';
  lastUsed?: Date;
  icon: string;
}

/**
 * Mobile Dashboard Component
 * Executive function-focused dashboard optimized for mobile devices
 * Provides quick access to all 37 tools with ADHD/autism accommodations
 */
export default function MobileDashboard({ className = '' }: MobileDashboardProps) {
  const [tools, setTools] = useState<ToolStatus[]>([]);
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  // Mock tool data (in real implementation, this would come from API)
  const mockTools: ToolStatus[] = [
    // Security Domain (13 tools)
    { id: 'misp', name: 'MISP', domain: 'security', status: 'active', icon: '🔍' },
    { id: 'helk', name: 'HELK', domain: 'security', status: 'idle', icon: '📊' },
    { id: 'security-onion', name: 'SecurityOnion', domain: 'security', status: 'active', icon: '🧅' },
    { id: 'yara-x', name: 'YARA-X', domain: 'security', status: 'idle', icon: '🎯' },
    { id: 'cyberchef', name: 'CyberChef', domain: 'security', status: 'active', icon: '👨‍🍳' },
    { id: 'maltrail', name: 'Maltrail', domain: 'security', status: 'idle', icon: '🕵️' },
    { id: 'nemesis', name: 'Nemesis', domain: 'security', status: 'offline', icon: '⚡' },
    { id: 'malware-bazaar', name: 'MalwareBazaar', domain: 'security', status: 'idle', icon: '🏪' },
    { id: 'virustotal', name: 'VirusTotal', domain: 'security', status: 'active', icon: '🛡️' },
    { id: 'apiscout', name: 'APIScout', domain: 'security', status: 'idle', icon: '🔎' },
    { id: 'blackarch', name: 'BlackArch', domain: 'security', status: 'offline', icon: '🏴' },
    { id: 'brute-ratel', name: 'Brute Ratel', domain: 'security', status: 'idle', icon: '🔨' },
    { id: 'forensic-kit', name: 'Forensic Kit', domain: 'security', status: 'idle', icon: '🔬' },

    // Productivity Domain (8 tools)
    { id: 'actual', name: 'Actual Budget', domain: 'productivity', status: 'active', icon: '💰' },
    { id: 'dispatch', name: 'Dispatch', domain: 'productivity', status: 'idle', icon: '📞' },
    { id: 'mealie', name: 'Mealie', domain: 'productivity', status: 'active', icon: '🍽️' },
    { id: 'firecrawl', name: 'Firecrawl', domain: 'productivity', status: 'idle', icon: '🔥' },
    { id: 'goose', name: 'Goose', domain: 'productivity', status: 'active', icon: '🪿' },
    { id: 'inspector', name: 'Inspector', domain: 'productivity', status: 'idle', icon: '🔍' },
    { id: 'it-tools', name: 'IT-Tools', domain: 'productivity', status: 'active', icon: '🛠️' },
    { id: 'n8n', name: 'n8n', domain: 'productivity', status: 'active', icon: '🔄' },

    // MTG Domain (4 tools)
    { id: 'commander-spellbook', name: 'Commander Spellbook', domain: 'mtg', status: 'idle', icon: '📖' },
    { id: 'mtg-commander-map', name: 'MTG Commander Map', domain: 'mtg', status: 'active', icon: '🗺️' },
    { id: 'mtg-scripting', name: 'MTG Scripting', domain: 'mtg', status: 'idle', icon: '📜' },
    { id: 'hexstrike-ai', name: 'HexStrike AI', domain: 'mtg', status: 'active', icon: '🎴' },

    // Infrastructure Domain (12 tools)
    { id: 'kong', name: 'Kong', domain: 'infrastructure', status: 'active', icon: '🦍' },
    { id: 'ghostwriter', name: 'Ghostwriter', domain: 'infrastructure', status: 'idle', icon: '👻' },
    { id: 'kasmvnc', name: 'KasmVNC', domain: 'infrastructure', status: 'active', icon: '🖥️' },
    { id: 'chroma-mcp', name: 'Chroma MCP', domain: 'infrastructure', status: 'active', icon: '🌈' },
    { id: 'filescope-mcp', name: 'FileScopeMCP', domain: 'infrastructure', status: 'idle', icon: '📁' },
    { id: 'n8n-mcp', name: 'n8n MCP', domain: 'infrastructure', status: 'active', icon: '🔗' },
    { id: 'firecrawl-mcp', name: 'Firecrawl MCP', domain: 'infrastructure', status: 'idle', icon: '🕷️' },
    { id: 'lscript', name: 'LScript', domain: 'infrastructure', status: 'idle', icon: '📝' },
    { id: 'meterpreter', name: 'Meterpreter', domain: 'infrastructure', status: 'offline', icon: '🎯' },
    { id: 'onex', name: 'OneX', domain: 'infrastructure', status: 'idle', icon: '1️⃣' },
    { id: 'rita', name: 'RITA', domain: 'infrastructure', status: 'active', icon: '📈' },
    { id: 'workflow-security', name: 'Security Workflows', domain: 'infrastructure', status: 'active', icon: '🔄' },
  ];

  useEffect(() => {
    // Simulate loading tools data
    const loadTools = async () => {
      setIsLoading(true);
      // In real implementation, fetch from API
      await new Promise(resolve => setTimeout(resolve, 1000));
      setTools(mockTools);
      setIsLoading(false);
    };

    loadTools();
  }, []);

  // Filter tools based on domain and search query
  const filteredTools = tools.filter(tool => {
    const matchesDomain = selectedDomain === 'all' || tool.domain === selectedDomain;
    const matchesSearch = tool.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDomain && matchesSearch;
  });

  // Group tools by domain for better organization
  const toolsByDomain = {
    security: filteredTools.filter(t => t.domain === 'security'),
    productivity: filteredTools.filter(t => t.domain === 'productivity'),
    mtg: filteredTools.filter(t => t.domain === 'mtg'),
    infrastructure: filteredTools.filter(t => t.domain === 'infrastructure'),
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'idle':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'offline':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getDomainColor = (domain: string) => {
    switch (domain) {
      case 'security':
        return 'bg-red-600';
      case 'productivity':
        return 'bg-blue-600';
      case 'mtg':
        return 'bg-purple-600';
      case 'infrastructure':
        return 'bg-green-600';
      default:
        return 'bg-gray-600';
    }
  };

  const domainCounts = {
    all: tools.length,
    security: toolsByDomain.security.length,
    productivity: toolsByDomain.productivity.length,
    mtg: toolsByDomain.mtg.length,
    infrastructure: toolsByDomain.infrastructure.length,
  };

  if (isLoading) {
    return (
      <div className={`p-4 ${className}`}>
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading executive function tools...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`p-4 ${className}`}>
      {/* Search and Filter Header */}
      <div className="mb-6">
        <div className="mb-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search tools..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg 
                         focus:ring-2 focus:ring-blue-500 focus:border-transparent
                         text-base placeholder-gray-500"
            />
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>
        </div>

        {/* Domain Filter Tabs */}
        <div className="flex overflow-x-auto space-x-2 pb-2">
          {[
            { id: 'all', name: 'All Tools', icon: '🧠' },
            { id: 'security', name: 'Security', icon: '🔒' },
            { id: 'productivity', name: 'Productivity', icon: '📋' },
            { id: 'mtg', name: 'MTG', icon: '🎴' },
            { id: 'infrastructure', name: 'Infrastructure', icon: '⚙️' },
          ].map((domain) => (
            <button
              key={domain.id}
              onClick={() => setSelectedDomain(domain.id)}
              className={`
                flex-shrink-0 flex items-center space-x-2 px-4 py-2 rounded-full
                text-sm font-medium border transition-all duration-150
                ${selectedDomain === domain.id
                  ? 'bg-blue-600 text-white border-blue-600'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                }
              `}
            >
              <span>{domain.icon}</span>
              <span>{domain.name}</span>
              <span className={`
                px-2 py-0.5 rounded-full text-xs
                ${selectedDomain === domain.id
                  ? 'bg-white bg-opacity-20'
                  : 'bg-gray-100'
                }
              `}>
                {domainCounts[domain.id as keyof typeof domainCounts]}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Tools Grid */}
      <div className="space-y-6">
        {selectedDomain === 'all' ? (
          // Show all domains grouped
          Object.entries(toolsByDomain).map(([domain, domainTools]) => {
            if (domainTools.length === 0) return null;
            
            return (
              <div key={domain} className="space-y-3">
                <div className="flex items-center space-x-2">
                  <div className={`w-3 h-3 rounded-full ${getDomainColor(domain)}`}></div>
                  <h3 className="text-lg font-semibold text-gray-900 capitalize">{domain} Domain</h3>
                  <span className="text-sm text-gray-500">({domainTools.length} tools)</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {domainTools.map((tool) => (
                    <ToolCard key={tool.id} tool={tool} />
                  ))}
                </div>
              </div>
            );
          })
        ) : (
          // Show single domain
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {filteredTools.map((tool) => (
              <ToolCard key={tool.id} tool={tool} />
            ))}
          </div>
        )}

        {filteredTools.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No tools found</h3>
            <p className="text-gray-600">
              {searchQuery
                ? `No tools match "${searchQuery}"`
                : `No tools available in ${selectedDomain} domain`
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

/**
 * Individual Tool Card Component
 */
function ToolCard({ tool }: { tool: ToolStatus }) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'idle':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'offline':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const handleToolClick = () => {
    // In real implementation, navigate to tool or open tool interface
    console.log(`Opening ${tool.name} tool`);
  };

  return (
    <button
      onClick={handleToolClick}
      className="w-full p-4 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 
                 hover:border-gray-300 transition-all duration-150 text-left
                 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center space-x-3">
          <div className="text-2xl">{tool.icon}</div>
          <div>
            <h4 className="text-sm font-medium text-gray-900">{tool.name}</h4>
            <p className="text-xs text-gray-500 capitalize">{tool.domain} domain</p>
          </div>
        </div>
        <span className={`
          px-2 py-1 text-xs font-medium rounded-full border
          ${getStatusColor(tool.status)}
        `}>
          {tool.status}
        </span>
      </div>
      
      {tool.lastUsed && (
        <div className="text-xs text-gray-500">
          Last used: {tool.lastUsed.toLocaleDateString()}
        </div>
      )}
      
      <div className="mt-2 flex items-center justify-between">
        <div className="flex items-center space-x-1">
          <div className={`w-2 h-2 rounded-full ${
            tool.status === 'active' ? 'bg-green-500' : 
            tool.status === 'idle' ? 'bg-yellow-500' : 'bg-red-500'
          }`}></div>
          <span className="text-xs text-gray-500">
            {tool.status === 'active' ? 'Ready' : 
             tool.status === 'idle' ? 'Standby' : 'Offline'}
          </span>
        </div>
        <svg 
          className="w-4 h-4 text-gray-400" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
        </svg>
      </div>
    </button>
  );
}