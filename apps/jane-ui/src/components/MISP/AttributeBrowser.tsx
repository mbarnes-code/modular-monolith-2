/**
 * MISP Attribute Browser Component
 * 
 * Converts critical MISP attribute browsing functionality from CakePHP views
 * to React components while maintaining original functionality and UX patterns.
 */

import { useEffect, useState } from 'react';

interface Attribute {
  id: number;
  event_id: number;
  category: string;
  type: string;
  value: string;
  to_ids: boolean;
  distribution: number;
  comment: string;
  timestamp: number;
  first_seen?: string;
  last_seen?: string;
  tags: Tag[];
}

interface Tag {
  id: number;
  name: string;
  colour: string;
  exportable: boolean;
}

interface AttributeBrowserProps {
  eventId?: number;
  filters?: AttributeFilters;
  onAttributeClick?: (attribute: Attribute) => void;
}

interface AttributeFilters {
  category?: string;
  type?: string;
  to_ids?: boolean;
  distribution?: number;
  tags?: string[];
  search?: string;
}

const ATTRIBUTE_CATEGORIES = [
  'Antivirus detection',
  'Artifacts dropped',
  'Attribution',
  'External analysis',
  'Financial fraud',
  'Internal reference',
  'Network activity',
  'Other',
  'Payload delivery',
  'Payload installation',
  'Payload type',
  'Persistence mechanism',
  'Person',
  'Social network',
  'Support Tool',
  'Targeting data'
];

const DISTRIBUTION_LEVELS = {
  0: { name: 'Your organisation only', color: 'bg-red-100 text-red-800' },
  1: { name: 'This community only', color: 'bg-orange-100 text-orange-800' },
  2: { name: 'Connected communities', color: 'bg-yellow-100 text-yellow-800' },
  3: { name: 'All communities', color: 'bg-green-100 text-green-800' },
  4: { name: 'Sharing group', color: 'bg-blue-100 text-blue-800' }
};

export default function MISPAttributeBrowser({ 
  eventId, 
  filters = {}, 
  onAttributeClick 
}: AttributeBrowserProps) {
  const [attributes, setAttributes] = useState<Attribute[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [searchFilters, setSearchFilters] = useState<AttributeFilters>(filters);
  const [showFilters, setShowFilters] = useState(false);

  const ITEMS_PER_PAGE = 50;

  useEffect(() => {
    fetchAttributes();
  }, [eventId, currentPage, searchFilters]);

  const fetchAttributes = async () => {
    try {
      setLoading(true);
      setError(null);

      const searchParams: any = {
        returnFormat: 'json',
        page: currentPage,
        limit: ITEMS_PER_PAGE,
        ...searchFilters
      };

      if (eventId) {
        searchParams.eventid = eventId;
      }

      const response = await fetch('/api/v1/attributes/restSearch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(searchParams)
      });

      if (!response.ok) {
        throw new Error('Failed to fetch attributes');
      }

      const data = await response.json();
      const attributeData = data.response || data.data || [];
      
      setAttributes(attributeData);
      setTotalPages(Math.ceil((data.total || attributeData.length) / ITEMS_PER_PAGE));
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load attributes');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters: Partial<AttributeFilters>) => {
    setSearchFilters(prev => ({ ...prev, ...newFilters }));
    setCurrentPage(1);
  };

  const handleAttributeClick = (attribute: Attribute) => {
    if (onAttributeClick) {
      onAttributeClick(attribute);
    } else {
      // Default behavior - navigate to attribute view
      window.location.href = `/misp/attributes/view/${attribute.id}`;
    }
  };

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleDateString();
  };

  const getDistributionInfo = (level: number) => {
    return DISTRIBUTION_LEVELS[level as keyof typeof DISTRIBUTION_LEVELS] || 
           { name: 'Unknown', color: 'bg-gray-100 text-gray-800' };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">
            Attributes
            {eventId && ` for Event #${eventId}`}
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            {attributes.length} attributes found
          </p>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`px-3 py-2 text-sm rounded-md ${
              showFilters 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            Filters
          </button>
          
          <button className="px-3 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700">
            Add Attribute
          </button>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="bg-white dark:bg-gray-800 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Category
              </label>
              <select
                value={searchFilters.category || ''}
                onChange={(e) => handleFilterChange({ category: e.target.value || undefined })}
                className="w-full p-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="">All Categories</option>
                {ATTRIBUTE_CATEGORIES.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Type
              </label>
              <input
                type="text"
                value={searchFilters.type || ''}
                onChange={(e) => handleFilterChange({ type: e.target.value || undefined })}
                placeholder="e.g., ip-dst, domain, hash"
                className="w-full p-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Search Value
              </label>
              <input
                type="text"
                value={searchFilters.search || ''}
                onChange={(e) => handleFilterChange({ search: e.target.value || undefined })}
                placeholder="Search attribute values..."
                className="w-full p-2 border border-gray-300 rounded-md text-sm"
              />
            </div>
          </div>
          
          <div className="flex items-center gap-4 mt-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={searchFilters.to_ids || false}
                onChange={(e) => handleFilterChange({ to_ids: e.target.checked || undefined })}
                className="rounded"
              />
              <span className="text-sm text-gray-700 dark:text-gray-300">IDS signatures only</span>
            </label>
            
            <button
              onClick={() => {
                setSearchFilters({});
                setCurrentPage(1);
              }}
              className="px-3 py-1 bg-gray-500 text-white text-sm rounded-md hover:bg-gray-600"
            >
              Clear Filters
            </button>
          </div>
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      )}

      {/* Attributes Table */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Category / Type
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Value
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Distribution
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Tags
                </th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                  Date
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {attributes.map((attribute) => {
                const distributionInfo = getDistributionInfo(attribute.distribution);
                
                return (
                  <tr 
                    key={attribute.id}
                    className="hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer"
                    onClick={() => handleAttributeClick(attribute)}
                  >
                    <td className="px-4 py-3">
                      <div>
                        <div className="text-sm font-medium text-gray-900 dark:text-white">
                          {attribute.category}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {attribute.type}
                        </div>
                      </div>
                    </td>
                    
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-sm text-gray-900 dark:text-white break-all">
                          {attribute.value}
                        </span>
                        {attribute.to_ids && (
                          <span className="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full">
                            IDS
                          </span>
                        )}
                      </div>
                      {attribute.comment && (
                        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                          {attribute.comment}
                        </div>
                      )}
                    </td>
                    
                    <td className="px-4 py-3">
                      <span className={`px-2 py-1 text-xs rounded-full ${distributionInfo.color}`}>
                        {distributionInfo.name}
                      </span>
                    </td>
                    
                    <td className="px-4 py-3">
                      <div className="flex gap-1 flex-wrap">
                        {attribute.tags?.slice(0, 3).map((tag) => (
                          <span
                            key={tag.id}
                            style={{ backgroundColor: tag.colour }}
                            className="px-2 py-1 text-white text-xs rounded-full"
                          >
                            {tag.name}
                          </span>
                        ))}
                        {attribute.tags?.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                            +{attribute.tags.length - 3}
                          </span>
                        )}
                      </div>
                    </td>
                    
                    <td className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                      {formatTimestamp(attribute.timestamp)}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <div className="text-sm text-gray-700 dark:text-gray-300">
            Page {currentPage} of {totalPages}
          </div>
          
          <div className="flex gap-2">
            <button
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
              className="px-3 py-2 bg-gray-200 text-gray-700 text-sm rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <button
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
              className="px-3 py-2 bg-gray-200 text-gray-700 text-sm rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}