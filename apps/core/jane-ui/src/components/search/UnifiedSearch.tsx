/**
 * Unified Search Component
 * Cross-domain search across all 37 tools in the mental prosthetic platform
 */

import { Clock, Database, Filter, Search, Star, Zap } from 'lucide-react';
import { useCallback, useEffect, useMemo, useState } from 'react';
import { usePerformanceMonitor } from '../../services/performance/performanceMonitor';
import { useSharedContext } from '../../services/state/optimizedStateManager';

export interface SearchResult {
  id: string;
  title: string;
  description: string;
  content: string;
  tool: string;
  domain: 'security' | 'productivity' | 'mtg' | 'infrastructure' | 'ai';
  type: 'document' | 'recipe' | 'report' | 'finding' | 'card' | 'workflow' | 'data' | 'configuration';
  relevanceScore: number;
  lastAccessed?: Date;
  isFavorite?: boolean;
  metadata?: Record<string, any>;
  url?: string;
}

export interface SearchFilters {
  domains: string[];
  tools: string[];
  types: string[];
  dateRange: 'all' | 'today' | 'week' | 'month' | 'year';
  minRelevance: number;
  favoritesOnly: boolean;
}

const DEFAULT_FILTERS: SearchFilters = {
  domains: [],
  tools: [],
  types: [],
  dateRange: 'all',
  minRelevance: 0,
  favoritesOnly: false
};

const DOMAIN_COLORS = {
  security: 'red',
  productivity: 'green',
  mtg: 'purple',
  infrastructure: 'blue',
  ai: 'orange'
} as const;

const TYPE_ICONS = {
  document: '📄',
  recipe: '🍳',
  report: '📊',
  finding: '🔍',
  card: '🃏',
  workflow: '⚡',
  data: '💾',
  configuration: '⚙️'
} as const;

interface UnifiedSearchProps {
  className?: string;
  onResultSelect?: (result: SearchResult) => void;
  placeholder?: string;
  showFilters?: boolean;
  maxResults?: number;
}

export function UnifiedSearch({ 
  className = '', 
  onResultSelect, 
  placeholder = "Search across all tools...",
  showFilters = true,
  maxResults = 50
}: UnifiedSearchProps) {
  const sharedContext = useSharedContext();
  const { measureOperation, markUIInteraction } = usePerformanceMonitor();
  
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [filters, setFilters] = useState<SearchFilters>(DEFAULT_FILTERS);
  const [isSearching, setIsSearching] = useState(false);
  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
  const [searchHistory, setSearchHistory] = useState<string[]>([]);
  const [recentResults, setRecentResults] = useState<SearchResult[]>([]);

  // Mock search data - in real implementation, this would come from actual tool APIs
  const mockSearchResults: SearchResult[] = useMemo(() => [
    // Security domain results
    {
      id: 'sec-001',
      title: 'Malware Analysis Report - SuspiciousFile.exe',
      description: 'Comprehensive analysis of detected malware sample with IOCs and mitigation strategies',
      content: 'malware executable analysis indicators compromise threat intelligence',
      tool: 'maltrail',
      domain: 'security',
      type: 'report',
      relevanceScore: 0.95,
      lastAccessed: new Date(Date.now() - 3600000),
      isFavorite: true,
      metadata: { severity: 'high', status: 'active' }
    },
    {
      id: 'sec-002',
      title: 'Network Traffic Anomaly - Suspicious Outbound Connections',
      description: 'Detected unusual network patterns indicating potential data exfiltration',
      content: 'network traffic anomaly detection suspicious connections outbound data exfiltration',
      tool: 'helk',
      domain: 'security',
      type: 'finding',
      relevanceScore: 0.88,
      lastAccessed: new Date(Date.now() - 7200000),
      metadata: { confidence: 'medium', priority: 'high' }
    },
    {
      id: 'sec-003',
      title: 'Incident Response Playbook - APT29',
      description: 'Step-by-step response procedures for APT29 attack patterns',
      content: 'incident response playbook apt29 advanced persistent threat procedures',
      tool: 'ghostwriter',
      domain: 'security',
      type: 'document',
      relevanceScore: 0.82,
      isFavorite: true,
      metadata: { classification: 'internal', version: '2.1' }
    },
    
    // Productivity domain results
    {
      id: 'prod-001',
      title: 'Weekly Meal Plan - Mediterranean Theme',
      description: 'Healthy Mediterranean-inspired meals for the week with shopping list',
      content: 'meal planning mediterranean healthy recipes shopping list nutrition',
      tool: 'mealie',
      domain: 'productivity',
      type: 'recipe',
      relevanceScore: 0.91,
      lastAccessed: new Date(Date.now() - 1800000),
      metadata: { servings: 4, prepTime: '30 min', difficulty: 'easy' }
    },
    {
      id: 'prod-002',
      title: 'Project Budget Analysis Q4',
      description: 'Quarterly budget tracking and expense analysis with forecasting',
      content: 'budget analysis quarterly expenses forecasting financial tracking',
      tool: 'actual',
      domain: 'productivity',
      type: 'report',
      relevanceScore: 0.85,
      lastAccessed: new Date(Date.now() - 14400000),
      metadata: { period: 'Q4-2024', variance: '+2.3%' }
    },
    {
      id: 'prod-003',
      title: 'Automated Data Backup Workflow',
      description: 'N8N workflow for automated daily data backups with error handling',
      content: 'automation workflow backup data daily scheduled error handling n8n',
      tool: 'n8n',
      domain: 'productivity',
      type: 'workflow',
      relevanceScore: 0.79,
      isFavorite: true,
      metadata: { status: 'active', lastRun: new Date(Date.now() - 86400000) }
    },
    
    // MTG domain results
    {
      id: 'mtg-001',
      title: 'Atraxa Superfriends Commander Deck',
      description: 'Optimized Atraxa planeswalker-focused commander deck with combo lines',
      content: 'atraxa superfriends commander planeswalkers combo deck optimization',
      tool: 'commander-spellbook',
      domain: 'mtg',
      type: 'card',
      relevanceScore: 0.93,
      lastAccessed: new Date(Date.now() - 900000),
      isFavorite: true,
      metadata: { colors: ['W', 'U', 'B', 'G'], power: 'cEDH', price: '$850' }
    },
    {
      id: 'mtg-002',
      title: 'Infinite Mana Combo Analysis',
      description: 'Comprehensive analysis of infinite mana combinations in EDH format',
      content: 'infinite mana combo analysis edh commander format optimization',
      tool: 'mtg-scripting-toolkit',
      domain: 'mtg',
      type: 'document',
      relevanceScore: 0.87,
      metadata: { format: 'EDH', combos: 47, avgCMC: 3.2 }
    },
    
    // Infrastructure domain results
    {
      id: 'infra-001',
      title: 'Kubernetes Cluster Configuration',
      description: 'Production-ready Kubernetes cluster setup with monitoring and security',
      content: 'kubernetes cluster configuration production monitoring security helm',
      tool: 'kasm-vnc',
      domain: 'infrastructure',
      type: 'configuration',
      relevanceScore: 0.84,
      metadata: { nodes: 5, resources: 'high', status: 'running' }
    },
    {
      id: 'infra-002',
      title: 'API Gateway Performance Metrics',
      description: 'Kong gateway performance analysis with optimization recommendations',
      content: 'api gateway performance metrics kong optimization recommendations latency',
      tool: 'kong',
      domain: 'infrastructure',
      type: 'report',
      relevanceScore: 0.78,
      lastAccessed: new Date(Date.now() - 10800000),
      metadata: { avgLatency: '45ms', throughput: '10K rps' }
    }
  ], []);

  // Search function with performance monitoring
  const performSearch = useCallback(async (searchQuery: string, searchFilters: SearchFilters) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    setIsSearching(true);
    markUIInteraction('unified-search-execute');

    try {
      const searchResults = await measureOperation('unified-search-query', () => {
        // Simulate search logic - in real implementation, this would query actual APIs
        const filtered = mockSearchResults.filter(result => {
          // Text relevance
          const titleMatch = result.title.toLowerCase().includes(searchQuery.toLowerCase());
          const descMatch = result.description.toLowerCase().includes(searchQuery.toLowerCase());
          const contentMatch = result.content.toLowerCase().includes(searchQuery.toLowerCase());
          const textRelevance = titleMatch || descMatch || contentMatch;

          // Apply filters
          const domainMatch = searchFilters.domains.length === 0 || searchFilters.domains.includes(result.domain);
          const toolMatch = searchFilters.tools.length === 0 || searchFilters.tools.includes(result.tool);
          const typeMatch = searchFilters.types.length === 0 || searchFilters.types.includes(result.type);
          const relevanceMatch = result.relevanceScore >= searchFilters.minRelevance;
          const favoriteMatch = !searchFilters.favoritesOnly || result.isFavorite;
          
          // Date filter
          let dateMatch = true;
          if (result.lastAccessed && searchFilters.dateRange !== 'all') {
            const now = new Date();
            const resultDate = result.lastAccessed;
            switch (searchFilters.dateRange) {
              case 'today':
                dateMatch = resultDate.toDateString() === now.toDateString();
                break;
              case 'week':
                dateMatch = (now.getTime() - resultDate.getTime()) <= 7 * 24 * 60 * 60 * 1000;
                break;
              case 'month':
                dateMatch = (now.getTime() - resultDate.getTime()) <= 30 * 24 * 60 * 60 * 1000;
                break;
              case 'year':
                dateMatch = (now.getTime() - resultDate.getTime()) <= 365 * 24 * 60 * 60 * 1000;
                break;
            }
          }

          return textRelevance && domainMatch && toolMatch && typeMatch && relevanceMatch && favoriteMatch && dateMatch;
        });

        // Sort by relevance score and recency
        filtered.sort((a, b) => {
          const scoreWeight = 0.7;
          const recencyWeight = 0.3;
          
          const aRecency = a.lastAccessed ? (Date.now() - a.lastAccessed.getTime()) / (30 * 24 * 60 * 60 * 1000) : 1;
          const bRecency = b.lastAccessed ? (Date.now() - b.lastAccessed.getTime()) / (30 * 24 * 60 * 60 * 1000) : 1;
          
          const aScore = (a.relevanceScore * scoreWeight) + ((1 - aRecency) * recencyWeight);
          const bScore = (b.relevanceScore * scoreWeight) + ((1 - bRecency) * recencyWeight);
          
          return bScore - aScore;
        });

        return filtered.slice(0, maxResults);
      }, 'productivity');

      setResults(searchResults);
      
      // Update search history
      if (searchQuery.trim() && !searchHistory.includes(searchQuery)) {
        setSearchHistory(prev => [searchQuery, ...prev.slice(0, 9)]);
      }
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setIsSearching(false);
    }
  }, [mockSearchResults, maxResults, measureOperation, markUIInteraction, searchHistory]);

  // Debounced search
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      performSearch(query, filters);
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [query, filters, performSearch]);

  const handleResultClick = (result: SearchResult) => {
    markUIInteraction('unified-search-result-select');
    
    // Add to recent results
    setRecentResults(prev => {
      const filtered = prev.filter(r => r.id !== result.id);
      return [result, ...filtered.slice(0, 4)];
    });

    // Update shared context with selected tool/domain
    if (result.tool) {
      sharedContext.setActiveTool(result.tool, result.domain);
    }

    onResultSelect?.(result);
  };

  const toggleFavorite = (resultId: string) => {
    setResults(prev => prev.map(result => 
      result.id === resultId 
        ? { ...result, isFavorite: !result.isFavorite }
        : result
    ));
    markUIInteraction('unified-search-favorite-toggle');
  };

  const clearFilters = () => {
    setFilters(DEFAULT_FILTERS);
    markUIInteraction('unified-search-clear-filters');
  };

  const availableDomains = [...new Set(mockSearchResults.map(r => r.domain))];
  const availableTools = [...new Set(mockSearchResults.map(r => r.tool))];
  const availableTypes = [...new Set(mockSearchResults.map(r => r.type))];

  return (
    <div className={`unified-search ${className}`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
        {/* Search Input */}
        <div className="relative mb-4">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder={placeholder}
            className="block w-full pl-10 pr-10 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 
                     focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          />
          {(isSearching || results.length > 0) && (
            <div className="absolute inset-y-0 right-0 flex items-center pr-3">
              {isSearching ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-600" />
              ) : (
                <span className="text-sm text-gray-500">{results.length} results</span>
              )}
            </div>
          )}
        </div>

        {/* Filters Toggle */}
        {showFilters && (
          <div className="flex items-center justify-between mb-4">
            <button
              onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
              className="flex items-center gap-2 px-3 py-1 text-sm text-gray-600 dark:text-gray-300 
                       hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
            >
              <Filter className="h-4 w-4" />
              Filters
              {Object.values(filters).some(f => Array.isArray(f) ? f.length > 0 : f !== DEFAULT_FILTERS.minRelevance && f !== DEFAULT_FILTERS.dateRange && f !== DEFAULT_FILTERS.favoritesOnly) && (
                <span className="ml-1 px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded-full">
                  Active
                </span>
              )}
            </button>
            
            {Object.values(filters).some(f => Array.isArray(f) ? f.length > 0 : f !== DEFAULT_FILTERS.minRelevance && f !== DEFAULT_FILTERS.dateRange && f !== DEFAULT_FILTERS.favoritesOnly) && (
              <button
                onClick={clearFilters}
                className="text-sm text-blue-600 hover:text-blue-700"
              >
                Clear filters
              </button>
            )}
          </div>
        )}

        {/* Advanced Filters */}
        {showAdvancedFilters && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            {/* Domain Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Domains
              </label>
              <div className="space-y-1">
                {availableDomains.map(domain => (
                  <label key={domain} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={filters.domains.includes(domain)}
                      onChange={(e) => {
                        setFilters(prev => ({
                          ...prev,
                          domains: e.target.checked 
                            ? [...prev.domains, domain]
                            : prev.domains.filter(d => d !== domain)
                        }));
                      }}
                      className="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm capitalize text-gray-700 dark:text-gray-300">
                      {domain}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Type Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Types
              </label>
              <div className="space-y-1">
                {availableTypes.map(type => (
                  <label key={type} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={filters.types.includes(type)}
                      onChange={(e) => {
                        setFilters(prev => ({
                          ...prev,
                          types: e.target.checked 
                            ? [...prev.types, type]
                            : prev.types.filter(t => t !== type)
                        }));
                      }}
                      className="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm capitalize text-gray-700 dark:text-gray-300">
                      {TYPE_ICONS[type as keyof typeof TYPE_ICONS]} {type}
                    </span>
                  </label>
                ))}
              </div>
            </div>

            {/* Date Range */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Date Range
              </label>
              <select
                value={filters.dateRange}
                onChange={(e) => setFilters(prev => ({ ...prev, dateRange: e.target.value as any }))}
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md 
                         bg-white dark:bg-gray-700 text-gray-900 dark:text-white text-sm"
              >
                <option value="all">All time</option>
                <option value="today">Today</option>
                <option value="week">This week</option>
                <option value="month">This month</option>
                <option value="year">This year</option>
              </select>
            </div>

            {/* Additional Options */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Options
              </label>
              <div className="space-y-2">
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={filters.favoritesOnly}
                    onChange={(e) => setFilters(prev => ({ ...prev, favoritesOnly: e.target.checked }))}
                    className="mr-2 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">
                    Favorites only
                  </span>
                </label>
                <div>
                  <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                    Min relevance: {Math.round(filters.minRelevance * 100)}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={filters.minRelevance}
                    onChange={(e) => setFilters(prev => ({ ...prev, minRelevance: Number(e.target.value) }))}
                    className="w-full"
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Search Results */}
        <div className="space-y-3">
          {results.map(result => (
            <div
              key={result.id}
              className="search-result group border border-gray-200 dark:border-gray-600 rounded-lg p-4 
                       hover:shadow-md hover:border-gray-300 dark:hover:border-gray-500 transition-all cursor-pointer"
              onClick={() => handleResultClick(result)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  {/* Result Header */}
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-lg">{TYPE_ICONS[result.type as keyof typeof TYPE_ICONS]}</span>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      result.domain === 'security' ? 'bg-red-100 text-red-700' :
                      result.domain === 'productivity' ? 'bg-green-100 text-green-700' :
                      result.domain === 'mtg' ? 'bg-purple-100 text-purple-700' :
                      result.domain === 'infrastructure' ? 'bg-blue-100 text-blue-700' :
                      'bg-orange-100 text-orange-700'
                    }`}>
                      {result.domain}
                    </span>
                    <span className="text-xs text-gray-500 capitalize">{result.tool}</span>
                    {result.isFavorite && <Star className="h-4 w-4 text-yellow-500 fill-current" />}
                  </div>

                  {/* Result Content */}
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-1 group-hover:text-blue-600">
                    {result.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {result.description}
                  </p>

                  {/* Result Metadata */}
                  <div className="flex items-center gap-4 text-xs text-gray-500">
                    <div className="flex items-center gap-1">
                      <Zap className="h-3 w-3" />
                      {Math.round(result.relevanceScore * 100)}% match
                    </div>
                    {result.lastAccessed && (
                      <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        {new Intl.RelativeTimeFormat('en', { numeric: 'auto' }).format(
                          Math.floor((result.lastAccessed.getTime() - Date.now()) / (1000 * 60 * 60)), 
                          'hour'
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Actions */}
                <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleFavorite(result.id);
                    }}
                    className={`p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 ${
                      result.isFavorite ? 'text-yellow-500' : 'text-gray-400'
                    }`}
                  >
                    <Star className={`h-4 w-4 ${result.isFavorite ? 'fill-current' : ''}`} />
                  </button>
                </div>
              </div>
            </div>
          ))}

          {/* No Results */}
          {query && !isSearching && results.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <Database className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>No results found for "{query}"</p>
              <p className="text-sm mt-1">Try adjusting your search terms or filters</p>
            </div>
          )}

          {/* Search History */}
          {!query && searchHistory.length > 0 && (
            <div className="border-t border-gray-200 dark:border-gray-600 pt-4">
              <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Recent Searches
              </h4>
              <div className="flex flex-wrap gap-2">
                {searchHistory.slice(0, 5).map(term => (
                  <button
                    key={term}
                    onClick={() => setQuery(term)}
                    className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 
                             rounded-full hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                  >
                    {term}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}