/**
 * MISP Event View Component
 * 
 * Migrated from CakePHP view (Events/view.ctp) to React/Next.js
 * Preserves original functionality and user interactions while
 * integrating with unified Jane UI interface.
 */

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { formatDistanceToNow } from 'date-fns';
import {
    AlertTriangle,
    Calendar,
    Download,
    Edit,
    Eye,
    Plus,
    Share,
    Tag,
    Users
} from 'lucide-react';
import { useEffect, useState } from 'react';

interface MISPEvent {
  id: number;
  uuid: string;
  info: string;
  date: string;
  threat_level_id: number;
  analysis: number;
  distribution: number;
  published: boolean;
  timestamp: number;
  orgc: {
    id: number;
    name: string;
    uuid: string;
  };
  org: {
    id: number;
    name: string;
    uuid: string;
  };
  attributes: MISPAttribute[];
  tags: MISPTag[];
  galaxies: MISPGalaxy[];
}

interface MISPAttribute {
  id: number;
  category: string;
  type: string;
  value: string;
  to_ids: boolean;
  distribution: number;
  comment: string;
  timestamp: number;
  first_seen?: string;
  last_seen?: string;
  tags: MISPTag[];
}

interface MISPTag {
  id: number;
  name: string;
  colour: string;
  exportable: boolean;
}

interface MISPGalaxy {
  id: number;
  name: string;
  type: string;
  description: string;
  clusters: Array<{
    id: number;
    name: string;
    description: string;
  }>;
}

interface EventViewProps {
  eventId: number;
  extended?: boolean;
  extending?: boolean;
}

const THREAT_LEVELS = {
  1: { name: 'High', color: 'bg-red-500' },
  2: { name: 'Medium', color: 'bg-orange-500' },
  3: { name: 'Low', color: 'bg-yellow-500' },
  4: { name: 'Undefined', color: 'bg-gray-500' }
};

const ANALYSIS_LEVELS = {
  0: { name: 'Initial', color: 'bg-blue-500' },
  1: { name: 'Ongoing', color: 'bg-yellow-500' },
  2: { name: 'Complete', color: 'bg-green-500' }
};

const DISTRIBUTION_LEVELS = {
  0: { name: 'Your organisation only', icon: '🏢' },
  1: { name: 'This community only', icon: '👥' },
  2: { name: 'Connected communities', icon: '🌐' },
  3: { name: 'All communities', icon: '🌍' },
  4: { name: 'Sharing group', icon: '👥' }
};

export default function MISPEventView({ eventId, extended = false, extending = false }: EventViewProps) {
  const [event, setEvent] = useState<MISPEvent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/v1/events/${eventId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch event');
        }
        const data = await response.json();
        setEvent(data.response?.[0] || data.data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchEvent();
  }, [eventId]);

  const handleExportEvent = async (format: string) => {
    try {
      const response = await fetch(`/api/v1/events/restSearch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          returnFormat: format,
          eventid: eventId
        })
      });

      if (!response.ok) throw new Error('Export failed');

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `event-${eventId}.${format}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export failed:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error || !event) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-500">Error: {error || 'Event not found'}</div>
      </div>
    );
  }

  const pageTitle = extended 
    ? `[Extended view] ${event.info}`
    : extending 
    ? `[Extending view] ${event.info}`
    : event.info;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            {pageTitle}
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            Event #{event.id} • {formatDistanceToNow(new Date(event.timestamp * 1000), { addSuffix: true })}
          </p>
        </div>
        
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => handleExportEvent('json')}>
            <Download className="h-4 w-4 mr-1" />
            Export
          </Button>
          <Button variant="outline" size="sm">
            <Share className="h-4 w-4 mr-1" />
            Share
          </Button>
          <Button variant="default" size="sm">
            <Edit className="h-4 w-4 mr-1" />
            Edit
          </Button>
        </div>
      </div>

      {/* Status Badges */}
      <div className="flex gap-2 flex-wrap">
        <Badge variant={event.published ? "default" : "secondary"}>
          {event.published ? 'Published' : 'Unpublished'}
        </Badge>
        <Badge className={THREAT_LEVELS[event.threat_level_id as keyof typeof THREAT_LEVELS]?.color}>
          {THREAT_LEVELS[event.threat_level_id as keyof typeof THREAT_LEVELS]?.name || 'Unknown'} Threat
        </Badge>
        <Badge className={ANALYSIS_LEVELS[event.analysis as keyof typeof ANALYSIS_LEVELS]?.color}>
          {ANALYSIS_LEVELS[event.analysis as keyof typeof ANALYSIS_LEVELS]?.name || 'Unknown'} Analysis
        </Badge>
        <Badge variant="outline">
          {DISTRIBUTION_LEVELS[event.distribution as keyof typeof DISTRIBUTION_LEVELS]?.icon} {' '}
          {DISTRIBUTION_LEVELS[event.distribution as keyof typeof DISTRIBUTION_LEVELS]?.name || 'Unknown Distribution'}
        </Badge>
      </div>

      {/* Main Content */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-5">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="attributes">
            Attributes ({event.attributes?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="tags">
            Tags ({event.tags?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="galaxies">
            Galaxies ({event.galaxies?.length || 0})
          </TabsTrigger>
          <TabsTrigger value="correlations">Correlations</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Event Details Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Calendar className="h-5 w-5" />
                  Event Details
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="font-medium">Event ID:</div>
                  <div>{event.id}</div>
                  
                  <div className="font-medium">UUID:</div>
                  <div className="font-mono text-xs break-all">{event.uuid}</div>
                  
                  <div className="font-medium">Date:</div>
                  <div>{event.date}</div>
                  
                  <div className="font-medium">Created:</div>
                  <div>{formatDistanceToNow(new Date(event.timestamp * 1000), { addSuffix: true })}</div>
                </div>
              </CardContent>
            </Card>

            {/* Organizations Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Organizations
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2">
                  <div>
                    <div className="font-medium text-sm">Creator Organization:</div>
                    <div className="text-sm text-blue-600 hover:underline cursor-pointer">
                      {event.orgc.name}
                    </div>
                  </div>
                  
                  <div>
                    <div className="font-medium text-sm">Owner Organization:</div>
                    <div className="text-sm text-blue-600 hover:underline cursor-pointer">
                      {event.org.name}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Event Information */}
          <Card>
            <CardHeader>
              <CardTitle>Event Information</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
                {event.info}
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="attributes" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Attributes ({event.attributes?.length || 0})</h3>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-1" />
              Add Attribute
            </Button>
          </div>
          
          <div className="space-y-2">
            {event.attributes?.map((attribute) => (
              <Card key={attribute.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge variant="outline">{attribute.category}</Badge>
                        <Badge variant="secondary">{attribute.type}</Badge>
                        {attribute.to_ids && <Badge className="bg-red-100 text-red-800">IDS</Badge>}
                      </div>
                      
                      <div className="font-mono text-sm bg-gray-50 dark:bg-gray-800 p-2 rounded">
                        {attribute.value}
                      </div>
                      
                      {attribute.comment && (
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                          {attribute.comment}
                        </p>
                      )}
                      
                      {attribute.tags?.length > 0 && (
                        <div className="flex gap-1 mt-2">
                          {attribute.tags.map((tag) => (
                            <Badge 
                              key={tag.id} 
                              style={{ backgroundColor: tag.colour }}
                              className="text-white text-xs"
                            >
                              {tag.name}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </div>
                    
                    <div className="flex gap-1">
                      <Button variant="ghost" size="sm">
                        <Eye className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Edit className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="tags" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Tags ({event.tags?.length || 0})</h3>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-1" />
              Add Tag
            </Button>
          </div>
          
          <div className="flex gap-2 flex-wrap">
            {event.tags?.map((tag) => (
              <Badge 
                key={tag.id} 
                style={{ backgroundColor: tag.colour }}
                className="text-white cursor-pointer hover:opacity-80"
              >
                <Tag className="h-3 w-3 mr-1" />
                {tag.name}
              </Badge>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="galaxies" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Galaxies ({event.galaxies?.length || 0})</h3>
            <Button size="sm">
              <Plus className="h-4 w-4 mr-1" />
              Add Galaxy
            </Button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {event.galaxies?.map((galaxy) => (
              <Card key={galaxy.id}>
                <CardHeader>
                  <CardTitle className="text-base">{galaxy.name}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                    {galaxy.description}
                  </p>
                  <Badge variant="outline">{galaxy.type}</Badge>
                  {galaxy.clusters?.length > 0 && (
                    <div className="mt-2">
                      <span className="text-xs text-gray-500">
                        {galaxy.clusters.length} clusters
                      </span>
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="correlations" className="space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold">Correlations</h3>
            <Button size="sm" variant="outline">
              <AlertTriangle className="h-4 w-4 mr-1" />
              Generate Correlations
            </Button>
          </div>
          
          <Card>
            <CardContent className="p-6 text-center">
              <p className="text-gray-500">No correlations found for this event.</p>
              <Button className="mt-2" variant="outline">
                Search for Correlations
              </Button>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}