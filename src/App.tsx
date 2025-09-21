import React from 'react';
import { useState, useEffect } from 'react';
import { Database, Download, Play, CheckCircle, AlertCircle, Clock, FileText, BarChart3, Settings } from 'lucide-react';

interface PipelineStatus {
  status: string;
  last_run?: string;
  records_processed?: number;
  message?: string;
}

interface AnalyticsSummary {
  total_users: number;
  total_posts: number;
  total_comments: number;
  avg_posts_per_user: number;
  most_active_user: string;
  post_engagement_rate: number;
}

interface Report {
  id: string;
  filename: string;
  created_at: string;
  size: number;
  type: string;
}

function App() {
  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus>({ status: 'unknown' });
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningPipeline, setRunningPipeline] = useState(false);

  useEffect(() => {
    fetchPipelineStatus();
    fetchAnalytics();
    fetchReports();
  }, []);

  const fetchPipelineStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/pipeline/status');
      if (response.ok) {
        const data = await response.json();
        setPipelineStatus(data);
      }
    } catch (error) {
      console.error('Failed to fetch pipeline status:', error);
      setPipelineStatus({ status: 'error', message: 'Backend not available' });
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('http://localhost:8000/analytics/summary');
      if (response.ok) {
        const data = await response.json();
        setAnalytics(data);
      }
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchReports = async () => {
    try {
      const response = await fetch('http://localhost:8000/reports/');
      if (response.ok) {
        const data = await response.json();
        setReports(data.reports || []);
      }
    } catch (error) {
      console.error('Failed to fetch reports:', error);
    }
  };

  const runPipeline = async () => {
    setRunningPipeline(true);
    try {
      const response = await fetch('http://localhost:8000/pipeline/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const result = await response.json();
        setPipelineStatus({ status: 'running', message: result.message });
        
        // Poll for status updates
        const pollStatus = setInterval(async () => {
          await fetchPipelineStatus();
          await fetchAnalytics();
          await fetchReports();
        }, 2000);

        // Stop polling after 30 seconds
        setTimeout(() => {
          clearInterval(pollStatus);
          setRunningPipeline(false);
        }, 30000);
      }
    } catch (error) {
      console.error('Failed to run pipeline:', error);
      setPipelineStatus({ status: 'error', message: 'Failed to start pipeline' });
    } finally {
      setRunningPipeline(false);
    }
  };

  const downloadReport = async (reportId: string) => {
    try {
      const response = await fetch(`http://localhost:8000/reports/${reportId}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = reportId;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Failed to download report:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'running':
        return <Clock className="h-5 w-5 text-yellow-500 animate-spin" />;
      case 'error':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Settings className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'running':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'error':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading pipeline dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <Database className="h-8 w-8 text-indigo-600 mr-3" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Data Engineering Pipeline</h1>
                <p className="text-sm text-gray-500">ETL Pipeline • JSONPlaceholder API • Clean Architecture</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center px-3 py-1 rounded-full border ${getStatusColor(pipelineStatus.status)}`}>
                {getStatusIcon(pipelineStatus.status)}
                <span className="ml-2 text-sm font-medium capitalize">{pipelineStatus.status}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Pipeline Control */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center">
              <Play className="h-5 w-5 text-indigo-600 mr-2" />
              Pipeline Control
            </h2>
          </div>
          <div className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 mb-2">
                  Extract data from JSONPlaceholder API → Transform → Load to Database → Generate Analytics
                </p>
                {pipelineStatus.last_run && (
                  <p className="text-xs text-gray-500">
                    Last run: {new Date(pipelineStatus.last_run).toLocaleString()}
                  </p>
                )}
                {pipelineStatus.records_processed && (
                  <p className="text-xs text-gray-500">
                    Records processed: {pipelineStatus.records_processed}
                  </p>
                )}
              </div>
              <button
                onClick={runPipeline}
                disabled={runningPipeline || pipelineStatus.status === 'running'}
                className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg font-medium flex items-center"
              >
                {runningPipeline || pipelineStatus.status === 'running' ? (
                  <>
                    <Clock className="h-4 w-4 mr-2 animate-spin" />
                    Running...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Run Pipeline
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Analytics Summary */}
        {analytics && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900 flex items-center">
                <BarChart3 className="h-5 w-5 text-indigo-600 mr-2" />
                Analytics Summary
              </h2>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-indigo-600">{analytics.total_users}</div>
                  <div className="text-sm text-gray-500">Total Users</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{analytics.total_posts}</div>
                  <div className="text-sm text-gray-500">Total Posts</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">{analytics.total_comments}</div>
                  <div className="text-sm text-gray-500">Total Comments</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">{analytics.avg_posts_per_user.toFixed(1)}</div>
                  <div className="text-sm text-gray-500">Avg Posts/User</div>
                </div>
                <div className="text-center">
                  <div className="text-lg font-bold text-blue-600">{analytics.most_active_user}</div>
                  <div className="text-sm text-gray-500">Most Active User</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-pink-600">{(analytics.post_engagement_rate * 100).toFixed(1)}%</div>
                  <div className="text-sm text-gray-500">Engagement Rate</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Generated Reports */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900 flex items-center">
              <FileText className="h-5 w-5 text-indigo-600 mr-2" />
              Generated Reports
            </h2>
          </div>
          <div className="p-6">
            {reports.length > 0 ? (
              <div className="space-y-3">
                {reports.map((report) => (
                  <div key={report.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <FileText className="h-5 w-5 text-gray-400 mr-3" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">{report.filename}</p>
                        <p className="text-xs text-gray-500">
                          {new Date(report.created_at).toLocaleString()} • {(report.size / 1024).toFixed(1)} KB • {report.type.toUpperCase()}
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => downloadReport(report.id)}
                      className="flex items-center text-indigo-600 hover:text-indigo-800 text-sm font-medium"
                    >
                      <Download className="h-4 w-4 mr-1" />
                      Download
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">No reports generated yet</p>
                <p className="text-sm text-gray-400">Run the pipeline to generate analytics reports</p>
              </div>
            )}
          </div>
        </div>

        {/* Data Flow Diagram */}
        <div className="mt-8 bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">ETL Data Flow</h3>
          <div className="flex items-center justify-between text-sm">
            <div className="text-center">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-2">
                <Database className="h-6 w-6 text-blue-600" />
              </div>
              <p className="font-medium">Extract</p>
              <p className="text-gray-500">JSONPlaceholder API</p>
            </div>
            <div className="flex-1 h-px bg-gray-300 mx-4"></div>
            <div className="text-center">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-2">
                <Settings className="h-6 w-6 text-green-600" />
              </div>
              <p className="font-medium">Transform</p>
              <p className="text-gray-500">Clean & Enrich</p>
            </div>
            <div className="flex-1 h-px bg-gray-300 mx-4"></div>
            <div className="text-center">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-2">
                <Database className="h-6 w-6 text-purple-600" />
              </div>
              <p className="font-medium">Load</p>
              <p className="text-gray-500">SQLite/PostgreSQL</p>
            </div>
            <div className="flex-1 h-px bg-gray-300 mx-4"></div>
            <div className="text-center">
              <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mb-2">
                <BarChart3 className="h-6 w-6 text-orange-600" />
              </div>
              <p className="font-medium">Analyze</p>
              <p className="text-gray-500">SQL Queries</p>
            </div>
            <div className="flex-1 h-px bg-gray-300 mx-4"></div>
            <div className="text-center">
              <div className="w-12 h-12 bg-pink-100 rounded-full flex items-center justify-center mb-2">
                <FileText className="h-6 w-6 text-pink-600" />
              </div>
              <p className="font-medium">Report</p>
              <p className="text-gray-500">CSV/JSON</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;