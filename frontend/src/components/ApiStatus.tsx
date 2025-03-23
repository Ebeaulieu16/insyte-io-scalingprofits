import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../types';

interface ApiStatusItem {
  service: string;
  status: 'ok' | 'error' | 'not_configured';
  message: string;
}

interface ApiStatusResponse {
  overall_status: string;
  apis: ApiStatusItem[];
  summary: {
    ok: number;
    error: number;
    not_configured: number;
  };
}

const ApiStatus: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<ApiStatusResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<boolean>(false);

  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/status/api-status`);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch API status: ${response.status}`);
        }
        
        const data = await response.json();
        setApiStatus(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching API status:', err);
        setError('Could not check API integration status');
      } finally {
        setLoading(false);
      }
    };

    checkApiStatus();
  }, []);

  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ok':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'error':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'not_configured':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ok':
        return '✅';
      case 'error':
        return '❌';
      case 'not_configured':
        return '⚠️';
      default:
        return '❓';
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse bg-gray-100 p-4 rounded-md shadow">
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md shadow">
        <p className="font-medium">API Status Error</p>
        <p className="text-sm">{error}</p>
      </div>
    );
  }

  if (!apiStatus) {
    return null;
  }

  return (
    <div className="bg-white rounded-md shadow overflow-hidden">
      <div 
        className="p-4 flex justify-between items-center cursor-pointer border-b"
        onClick={toggleExpanded}
      >
        <div>
          <h3 className="font-medium text-gray-900">API Integrations Status</h3>
          <p className="text-sm text-gray-500">
            {apiStatus.summary.ok} working, {apiStatus.summary.error} errors, {apiStatus.summary.not_configured} not configured
          </p>
        </div>
        <div className={`px-2 py-1 rounded-full ${getStatusColor(apiStatus.overall_status)}`}>
          {apiStatus.overall_status === 'ok' ? 'All Systems Go' : 'Attention Needed'}
        </div>
      </div>

      {expanded && (
        <div className="p-4 bg-gray-50">
          <div className="grid gap-2">
            {apiStatus.apis.map((api) => (
              <div 
                key={api.service}
                className={`p-3 border rounded-md ${getStatusColor(api.status)}`}
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium">{api.service}</span>
                  <span>{getStatusIcon(api.status)}</span>
                </div>
                <p className="text-sm mt-1">{api.message}</p>
              </div>
            ))}
          </div>
          
          {apiStatus.summary.not_configured > 0 && (
            <div className="mt-4 text-sm text-gray-700 bg-yellow-50 p-3 rounded-md border border-yellow-200">
              <p className="font-medium">Configuration Needed</p>
              <p className="mt-1">
                Some API integrations are not configured. Edit the <code>.env</code> file in the backend directory to add your API keys.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ApiStatus; 