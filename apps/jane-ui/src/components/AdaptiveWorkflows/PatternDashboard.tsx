/**
 * Pattern Detection Dashboard Component
 * 
 * Displays detected user behavior patterns that can be automated
 * through n8n workflow generation.
 */

import {
    AlertCircle,
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    CheckCircle,
    Clock,
    Progress,
    RefreshCw,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
    TrendingUp
} from '@/components/ui';
import React, { useEffect, useState } from 'react';

interface WorkflowPattern {
  id: string;
  pattern_name: string;
  description: string;
  category: string;
  occurrence_count: number;
  confidence_score: number;
  is_ready_for_automation: boolean;
  tool_sequence: string[];
  created_at: string;
  last_seen: string;
}

interface PatternDashboardProps {
  userId: string;
  onPatternSelected?: (pattern: WorkflowPattern) => void;
  refreshInterval?: number;
}

export const PatternDashboard: React.FC<PatternDashboardProps> = ({
  userId,
  onPatternSelected,
  refreshInterval = 30000
}) => {
  const [patterns, setPatterns] = useState<WorkflowPattern[]>([]);
  const [readyPatterns, setReadyPatterns] = useState<WorkflowPattern[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);

  // Fetch patterns from API
  const fetchPatterns = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Fetch all patterns
      const patternsResponse = await fetch('/api/adaptive-workflows/analyze-patterns', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          lookback_days: 30
        })
      });

      if (!patternsResponse.ok) {
        throw new Error(`Failed to fetch patterns: ${patternsResponse.statusText}`);
      }

      const patternsData = await patternsResponse.json();
      setPatterns(patternsData);

      // Fetch ready patterns
      const readyResponse = await fetch(
        `/api/adaptive-workflows/patterns/ready?user_id=${userId}`
      );

      if (!readyResponse.ok) {
        throw new Error(`Failed to fetch ready patterns: ${readyResponse.statusText}`);
      }

      const readyData = await readyResponse.json();
      setReadyPatterns(readyData);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  // Re-analyze patterns
  const reanalyzePatterns = async () => {
    try {
      setAnalyzing(true);
      setError(null);

      const response = await fetch('/api/adaptive-workflows/analyze-patterns', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          lookback_days: 30,
          force_reanalysis: true
        })
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.statusText}`);
      }

      // Refresh patterns after reanalysis
      await fetchPatterns();

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  useEffect(() => {
    fetchPatterns();

    // Set up refresh interval
    const interval = setInterval(fetchPatterns, refreshInterval);
    return () => clearInterval(interval);
  }, [userId, refreshInterval]);

  const getConfidenceColor = (score: number): string => {
    if (score >= 0.8) return 'bg-green-100 text-green-800';
    if (score >= 0.6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getCategoryColor = (category: string): string => {
    const colors = {
      security: 'bg-red-100 text-red-800',
      productivity: 'bg-blue-100 text-blue-800',
      mtg: 'bg-purple-100 text-purple-800',
      infrastructure: 'bg-green-100 text-green-800',
      general: 'bg-gray-100 text-gray-800'
    };
    return colors[category as keyof typeof colors] || colors.general;
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <RefreshCw className="animate-spin h-8 w-8 text-blue-600" />
        <span className="ml-2 text-lg">Analyzing patterns...</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Pattern Detection Dashboard</h2>
          <p className="text-gray-600">
            Detected workflow patterns ready for automation
          </p>
        </div>
        <Button
          onClick={reanalyzePatterns}
          disabled={analyzing}
          className="flex items-center gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${analyzing ? 'animate-spin' : ''}`} />
          {analyzing ? 'Analyzing...' : 'Re-analyze'}
        </Button>
      </div>

      {/* Error Display */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-4">
            <div className="flex items-center gap-2 text-red-700">
              <AlertCircle className="h-5 w-5" />
              <span>{error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-blue-600" />
              <div>
                <p className="text-sm text-gray-600">Total Patterns</p>
                <p className="text-2xl font-bold">{patterns.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <div>
                <p className="text-sm text-gray-600">Ready for Automation</p>
                <p className="text-2xl font-bold text-green-600">
                  {readyPatterns.length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-orange-600" />
              <div>
                <p className="text-sm text-gray-600">High Confidence</p>
                <p className="text-2xl font-bold text-orange-600">
                  {patterns.filter(p => p.confidence_score >= 0.8).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-4">
            <div className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-yellow-600" />
              <div>
                <p className="text-sm text-gray-600">Automation Rate</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {patterns.length > 0 
                    ? Math.round((readyPatterns.length / patterns.length) * 100)
                    : 0}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Ready Patterns Section */}
      {readyPatterns.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              Ready for Automation ({readyPatterns.length})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {readyPatterns.map((pattern) => (
                <div
                  key={pattern.id}
                  className="border rounded-lg p-4 hover:bg-gray-50 cursor-pointer"
                  onClick={() => onPatternSelected?.(pattern)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h4 className="font-semibold">{pattern.pattern_name}</h4>
                      <p className="text-sm text-gray-600 mt-1">
                        {pattern.description}
                      </p>
                      <div className="flex items-center gap-4 mt-2">
                        <Badge className={getCategoryColor(pattern.category)}>
                          {pattern.category}
                        </Badge>
                        <span className="text-sm text-gray-500">
                          {pattern.occurrence_count} occurrences
                        </span>
                        <span className="text-sm text-gray-500">
                          {pattern.tool_sequence.length} tools
                        </span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium">
                        {Math.round(pattern.confidence_score * 100)}% confidence
                      </div>
                      <Progress 
                        value={pattern.confidence_score * 100} 
                        className="w-20 mt-1"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* All Patterns Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Detected Patterns</CardTitle>
        </CardHeader>
        <CardContent>
          {patterns.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <TrendingUp className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No patterns detected yet.</p>
              <p className="text-sm">Start using tools to build patterns for automation.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Pattern</TableHead>
                  <TableHead>Category</TableHead>
                  <TableHead>Occurrences</TableHead>
                  <TableHead>Confidence</TableHead>
                  <TableHead>Tools</TableHead>
                  <TableHead>Last Seen</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {patterns.map((pattern) => (
                  <TableRow 
                    key={pattern.id}
                    className={pattern.is_ready_for_automation ? 'bg-green-50' : ''}
                  >
                    <TableCell>
                      <div>
                        <div className="font-medium">{pattern.pattern_name}</div>
                        <div className="text-sm text-gray-500 truncate max-w-xs">
                          {pattern.description}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getCategoryColor(pattern.category)}>
                        {pattern.category}
                      </Badge>
                    </TableCell>
                    <TableCell>{pattern.occurrence_count}</TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <span className="text-sm">
                          {Math.round(pattern.confidence_score * 100)}%
                        </span>
                        <Progress 
                          value={pattern.confidence_score * 100} 
                          className="w-16"
                        />
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm">
                        {pattern.tool_sequence.slice(0, 3).join(', ')}
                        {pattern.tool_sequence.length > 3 && '...'}
                      </div>
                    </TableCell>
                    <TableCell className="text-sm text-gray-500">
                      {formatDate(pattern.last_seen)}
                    </TableCell>
                    <TableCell>
                      {pattern.is_ready_for_automation ? (
                        <Badge className="bg-green-100 text-green-800">
                          Ready
                        </Badge>
                      ) : (
                        <Badge className="bg-gray-100 text-gray-800">
                          Developing
                        </Badge>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default PatternDashboard;