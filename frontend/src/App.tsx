import { useState, useEffect } from 'react'
import './App.css'
import { API_BASE_URL } from './types'
import ApiStatus from './components/ApiStatus';
import UTMGenerator from './components/UTMGenerator';

// Types
interface VideoMetrics {
  slug: string;
  title: string;
  views: number;
  likes: number;
  comments: number;
  avg_watch_time: number;
  clicks: number;
  bookings: number;
  sales: number;
  revenue: number;
}

interface DashboardData {
  total_clicks: number;
  total_bookings: number;
  total_sales: number;
  total_revenue: number;
  show_up_rate: number;
  closing_rate: number;
  average_order_value: number;
  videos: VideoMetrics[];
}

function App() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Fetch dashboard data from API
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${API_BASE_URL}/dashboard/`);
        
        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        setDashboardData(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const createMockData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/dashboard/mock-data/`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }
      
      // Reload dashboard data
      const dashboardResponse = await fetch(`${API_BASE_URL}/dashboard/`);
      const data = await dashboardResponse.json();
      setDashboardData(data);
      setError(null);
    } catch (err) {
      console.error('Error creating mock data:', err);
      setError('Failed to create mock data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Format currency
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(value);
  };

  // Format percentage
  const formatPercentage = (value: number): string => {
    return `${value.toFixed(1)}%`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Insyte.io Dashboard</h1>
          
          {/* Mock Data Button */}
          <button
            onClick={createMockData}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md"
          >
            Load Demo Data
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* API Status Component */}
        <div className="mb-8">
          <ApiStatus />
        </div>
      
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600 mb-4"></div>
            <p className="text-gray-500">Loading dashboard data...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 text-red-600 p-4 rounded-md">
            <p className="font-medium">{error}</p>
          </div>
        ) : dashboardData && (
          <>
            {/* Dashboard Content */}
            <div className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Overview</h2>
              <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
                        {/* Icon would go here */}
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Total Clicks</dt>
                          <dd className="text-2xl font-semibold text-gray-900">{dashboardData.total_clicks}</dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
                        {/* Icon would go here */}
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate">Total Revenue</dt>
                          <dd className="text-2xl font-semibold text-gray-900">{formatCurrency(dashboardData.total_revenue)}</dd>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* Video Performance Table */}
            <div className="bg-white shadow overflow-hidden sm:rounded-md mb-8">
              <div className="px-4 py-5 sm:px-6">
                <h2 className="text-lg font-medium text-gray-900">Video Performance</h2>
                <p className="mt-1 text-sm text-gray-500">Overview of your YouTube videos and their conversion metrics.</p>
              </div>
              <div className="border-t border-gray-200">
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Video Title</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Views</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Clicks</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">CTR</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bookings</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Revenue</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {dashboardData.videos.length === 0 ? (
                        <tr>
                          <td colSpan={6} className="px-6 py-4 text-center text-sm text-gray-500">
                            No video data available. Click "Load Demo Data" to generate sample data.
                          </td>
                        </tr>
                      ) : (
                        dashboardData.videos.map((video) => {
                          // Calculate CTR (Click-Through Rate)
                          const ctr = video.views > 0 
                            ? ((video.clicks / video.views) * 100).toFixed(2) + '%'
                            : '0.00%';
                            
                          return (
                            <tr key={video.slug}>
                              <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                {video.title}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {video.views.toLocaleString()}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {video.clicks.toLocaleString()}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {ctr}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {video.bookings.toLocaleString()}
                              </td>
                              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                {formatCurrency(video.revenue)}
                              </td>
                            </tr>
                          );
                        })
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </>
        )}
        
        {/* UTM Generator */}
        <UTMGenerator baseUrl={window.location.origin} />
      </main>
    </div>
  );
}

export default App
