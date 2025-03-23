import React from 'react';
import { DashboardData } from '../types';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface ChartsProps {
  data: DashboardData;
}

const Charts: React.FC<ChartsProps> = ({ data }) => {
  // Format for funnel chart
  const funnelData = {
    labels: ['Clicks', 'Bookings', 'Sales'],
    datasets: [
      {
        label: 'Conversion Funnel',
        data: [data.total_clicks, data.total_bookings, data.total_sales],
        backgroundColor: [
          'rgba(99, 102, 241, 0.8)',
          'rgba(79, 70, 229, 0.8)',
          'rgba(67, 56, 202, 0.8)',
        ],
        borderColor: [
          'rgba(99, 102, 241, 1)',
          'rgba(79, 70, 229, 1)',
          'rgba(67, 56, 202, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  // Format for revenue by video chart
  const revenueData = {
    labels: data.videos.map(video => video.title),
    datasets: [
      {
        label: 'Revenue ($)',
        data: data.videos.map(video => video.revenue),
        backgroundColor: 'rgba(99, 102, 241, 0.8)',
        borderColor: 'rgba(99, 102, 241, 1)',
        borderWidth: 1,
      },
    ],
  };

  // Mock data for line chart (cash collected over time)
  // In a real app, this would come from actual dated sales data
  const cashCollectedData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Revenue Over Time',
        data: [
          data.total_revenue * 0.1,
          data.total_revenue * 0.2,
          data.total_revenue * 0.3,
          data.total_revenue * 0.5,
          data.total_revenue * 0.8,
          data.total_revenue,
        ],
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4,
      },
    ],
  };

  // Calculate booking status counts for donut chart
  const completed = data.videos.reduce((sum, video) => sum + Math.round(video.bookings * 0.65), 0);
  const noShow = data.videos.reduce((sum, video) => sum + Math.round(video.bookings * 0.20), 0);
  const rescheduled = data.videos.reduce((sum, video) => sum + Math.round(video.bookings * 0.15), 0);

  const statusData = {
    labels: ['Completed', 'No-show', 'Rescheduled'],
    datasets: [
      {
        label: 'Booking Status',
        data: [completed, noShow, rescheduled],
        backgroundColor: [
          'rgba(34, 197, 94, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(234, 179, 8, 0.8)',
        ],
        borderColor: [
          'rgba(34, 197, 94, 1)',
          'rgba(239, 68, 68, 1)',
          'rgba(234, 179, 8, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  // Chart options
  const barOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Revenue by Video',
      },
    },
  };

  const lineOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Revenue Over Time',
      },
    },
  };

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Performance Charts</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Funnel Chart */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Conversion Funnel</h3>
          <Bar data={funnelData} options={barOptions} height={300} />
        </div>
        
        {/* Revenue by Video */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Revenue by Video</h3>
          <Bar data={revenueData} options={barOptions} height={300} />
        </div>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Revenue Over Time */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Revenue Over Time</h3>
          <Line data={cashCollectedData} options={lineOptions} height={300} />
        </div>
        
        {/* Booking Status */}
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Call Status</h3>
          <div className="flex justify-center">
            <div style={{ maxWidth: '300px' }}>
              <Doughnut data={statusData} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Charts; 