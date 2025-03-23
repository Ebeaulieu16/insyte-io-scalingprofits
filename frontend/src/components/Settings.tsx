import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';

interface YouTubeAuthStatus {
  authenticated: boolean;
  message?: string;
  expires_at?: string;
  scopes?: string;
  updated_at?: string;
}

const Settings: React.FC = () => {
  const [youtubeStatus, setYoutubeStatus] = useState<YouTubeAuthStatus>({ authenticated: false });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check YouTube auth status
    const checkYouTubeAuth = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/auth/youtube/status`);
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        setYoutubeStatus(data);
        setError(null);
      } catch (err) {
        console.error('Error checking YouTube auth status:', err);
        setError('Failed to check YouTube authentication status.');
      } finally {
        setLoading(false);
      }
    };

    checkYouTubeAuth();
  }, []);

  const handleAuthorizeYouTube = () => {
    // Redirect to our backend's YouTube login route
    window.location.href = `${API_BASE_URL}/auth/youtube/login`;
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">API Settings</h2>
      
      {loading ? (
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-4 py-1">
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 text-red-600 p-4 rounded-md mb-6">
          <p className="font-medium">{error}</p>
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
          <div className="px-4 py-5 sm:px-6 bg-gray-50">
            <h3 className="text-lg leading-6 font-medium text-gray-900">YouTube API Authentication</h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Connect to YouTube API to fetch video metrics
            </p>
          </div>
          <div className="border-t border-gray-200 px-4 py-5 sm:p-6">
            <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
              <div className="sm:col-span-1">
                <dt className="text-sm font-medium text-gray-500">Authentication Status</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {youtubeStatus.authenticated ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Authenticated
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      Not Authenticated
                    </span>
                  )}
                </dd>
              </div>

              {youtubeStatus.authenticated && (
                <>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Token Expires</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {formatDate(youtubeStatus.expires_at || '')}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Last Updated</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {formatDate(youtubeStatus.updated_at || '')}
                    </dd>
                  </div>
                  <div className="sm:col-span-1">
                    <dt className="text-sm font-medium text-gray-500">Scopes</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {youtubeStatus.scopes || 'None'}
                    </dd>
                  </div>
                </>
              )}
            </dl>
            
            <div className="mt-5">
              <button
                type="button"
                onClick={handleAuthorizeYouTube}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                {youtubeStatus.authenticated ? 'Re-authorize YouTube' : 'Authorize YouTube'}
              </button>
              
              {youtubeStatus.authenticated && (
                <p className="mt-2 text-sm text-gray-500">
                  Your YouTube API connection is active. You can re-authorize if you're experiencing issues.
                </p>
              )}
              
              {!youtubeStatus.authenticated && youtubeStatus.message && (
                <p className="mt-2 text-sm text-gray-500">
                  {youtubeStatus.message}
                </p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Settings; 