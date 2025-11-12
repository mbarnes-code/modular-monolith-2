/**
 * MISP Dashboard Component
 * 
 * Main dashboard for MISP threat intelligence platform integration
 * Preserves original MISP dashboard functionality while integrating
 * with Jane's unified interface.
 */

import { useEffect, useState } from 'react';

interface MISPStats {
  events: number;
  attributes: number;
  correlations: number;
  proposals: number;
  users: number;
  organisations: number;
}

interface MISPEvent {
  id: number;
  info: string;
  date: string;
  threat_level_id: number;
  published: boolean;
  orgc_name: string;
}

interface DashboardProps {
  userRole?: string;
  permissions?: string[];
}

export default function MISPDashboard({ userRole = 'user', permissions = [] }: DashboardProps) {
  const [stats, setStats] = useState<MISPStats | null>(null);
  const [recentEvents, setRecentEvents] = useState<MISPEvent[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch statistics
        const statsResponse = await fetch('/api/v1/events/stats');
        if (statsResponse.ok) {
          const statsData = await statsResponse.json();
          setStats(statsData.data || statsData.response);
        }

        // Fetch recent events
        const eventsResponse = await fetch('/api/v1/events/restSearch', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            returnFormat: 'json',
            limit: 10,
            published: true
          })
        });
        
        if (eventsResponse.ok) {
          const eventsData = await eventsResponse.json();
          setRecentEvents(eventsData.data || eventsData.response || []);
        }
        
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const handleEventClick = (eventId: number) => {
    // Navigate to event view
    window.location.href = `/misp/events/${eventId}`;
  };

  const getThreatLevelColor = (level: number) => {
    switch (level) {
      case 1: return 'bg-red-500';
      case 2: return 'bg-orange-500';
      case 3: return 'bg-yellow-500';
      case 4: return 'bg-gray-500';
      default: return 'bg-gray-400';
    }
  };

  const getThreatLevelName = (level: number) => {
    switch (level) {
      case 1: return 'High';
      case 2: return 'Medium';
      case 3: return 'Low';
      case 4: return 'Undefined';
      default: return 'Unknown';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
          MISP Threat Intelligence Dashboard
        </h1>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
            Create Event
          </button>
          <button className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700">
            Import Data
          </button>
        </div>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-blue-600">{stats.events}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Events</div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-green-600">{stats.attributes}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Attributes</div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-purple-600">{stats.correlations}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Correlations</div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-orange-600">{stats.proposals}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Proposals</div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-red-600">{stats.users}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Users</div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
            <div className="text-2xl font-bold text-indigo-600">{stats.organisations}</div>
            <div className="text-sm text-gray-600 dark:text-gray-400">Organizations</div>
          </div>
        </div>
      )}

      {/* Recent Events */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            Recent Events
          </h2>
        </div>
        
        <div className="p-4">
          {recentEvents.length === 0 ? (
            <p className="text-gray-500 text-center py-4">No events found</p>
          ) : (
            <div className="space-y-2">
              {recentEvents.map((event) => (
                <div 
                  key={event.id}
                  className="flex items-center justify-between p-3 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md cursor-pointer"
                  onClick={() => handleEventClick(event.id)}
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-gray-900 dark:text-white">
                        #{event.id}
                      </span>
                      <span className={`px-2 py-1 text-xs rounded-full text-white ${getThreatLevelColor(event.threat_level_id)}`}>
                        {getThreatLevelName(event.threat_level_id)}
                      </span>
                      {event.published && (
                        <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                          Published
                        </span>
                      )}
                    </div>
                    
                    <div className="text-sm text-gray-900 dark:text-white mt-1">
                      {event.info}
                    </div>
                    
                    <div className="text-xs text-gray-500 mt-1">
                      {event.date} • {event.orgc_name}
                    </div>
                  </div>
                  
                  <div className="text-gray-400">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <button className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-md transition-shadow text-left">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            Search Events
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Find threat intelligence events
          </div>
        </button>
        
        <button className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-md transition-shadow text-left">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            Browse Attributes
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Explore threat indicators
          </div>
        </button>
        
        <button className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-md transition-shadow text-left">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            View Correlations
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Analyze threat relationships
          </div>
        </button>
        
        <button className="p-4 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-md transition-shadow text-left">
          <div className="text-lg font-semibold text-gray-900 dark:text-white">
            Manage Feeds
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Configure threat feeds
          </div>
        </button>
      </div>
    </div>
  );
}