import React from 'react';
import { VideoMetrics } from '../types';

interface VideoTableProps {
  videos: VideoMetrics[];
}

const VideoTable: React.FC<VideoTableProps> = ({ videos }) => {
  // Format numbers with commas
  const formatNumber = (num: number): string => {
    return num.toLocaleString();
  };

  // Format currency
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
    }).format(value);
  };

  // Format time (for average watch time)
  const formatTime = (minutes: number): string => {
    const mins = Math.floor(minutes);
    const secs = Math.round((minutes - mins) * 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Determine color class based on value
  const getHeatMapClass = (value: number, max: number): string => {
    const percentage = value / max;
    if (percentage >= 0.75) return 'bg-green-100';
    if (percentage >= 0.5) return 'bg-green-50';
    if (percentage >= 0.25) return 'bg-gray-50';
    return '';
  };

  // Find maximum values for heatmap coloring
  const maxViews = Math.max(...videos.map(v => v.views), 1);
  const maxClicks = Math.max(...videos.map(v => v.clicks), 1);
  const maxBookings = Math.max(...videos.map(v => v.bookings), 1);
  const maxRevenue = Math.max(...videos.map(v => v.revenue), 1);
  const maxLikes = Math.max(...videos.map(v => v.likes), 1);
  const maxComments = Math.max(...videos.map(v => v.comments), 1);
  const maxWatchTime = Math.max(...videos.map(v => v.avg_watch_time), 1);

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Video Performance</h2>
      
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Video Title
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Views
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Clicks
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                CTR
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Bookings
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Revenue
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Likes
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Comments
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Avg Watch
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {videos.map((video) => {
              // Calculate CTR (Click-Through Rate)
              const ctr = video.views > 0 
                ? ((video.clicks / video.views) * 100).toFixed(2) + '%'
                : '0.00%';
                
              return (
                <tr key={video.slug}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {video.title}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-500 ${getHeatMapClass(video.views, maxViews)}`}>
                    {formatNumber(video.views)}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-500 ${getHeatMapClass(video.clicks, maxClicks)}`}>
                    {formatNumber(video.clicks)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {ctr}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-500 ${getHeatMapClass(video.bookings, maxBookings)}`}>
                    {formatNumber(video.bookings)}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-500 ${getHeatMapClass(video.revenue, maxRevenue)}`}>
                    {formatCurrency(video.revenue)}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-500 ${getHeatMapClass(video.likes, maxLikes)}`}>
                    {formatNumber(video.likes)}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-500 ${getHeatMapClass(video.comments, maxComments)}`}>
                    {formatNumber(video.comments)}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-gray-500 ${getHeatMapClass(video.avg_watch_time, maxWatchTime)}`}>
                    {formatTime(video.avg_watch_time)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default VideoTable; 