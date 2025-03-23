import React from 'react';
import { DashboardData } from '../types';

// KPI Card component
const KPICard: React.FC<{
  title: string;
  value: string | number;
  description?: string;
  icon?: React.ReactNode;
}> = ({ title, value, description, icon }) => {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="flex items-center">
          {icon && <div className="flex-shrink-0 mr-3">{icon}</div>}
          <div>
            <dt className="text-sm font-medium text-gray-500 truncate">
              {title}
            </dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">
              {value}
            </dd>
            {description && (
              <p className="mt-2 text-sm text-gray-500">{description}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Dashboard component
interface DashboardProps {
  data: DashboardData;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
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
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard KPIs</h2>
      
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {/* KPI Cards */}
        <KPICard 
          title="Total Clicks" 
          value={data.total_clicks.toLocaleString()} 
          description="Total tracked clicks from YouTube"
        />
        
        <KPICard 
          title="Booked Calls" 
          value={data.total_bookings.toLocaleString()} 
          description="Total scheduled calls"
        />
        
        <KPICard 
          title="Closed Deals" 
          value={data.total_sales.toLocaleString()} 
          description="Total successful conversions"
        />
        
        <KPICard 
          title="Revenue" 
          value={formatCurrency(data.total_revenue)} 
          description="Total revenue generated"
        />
        
        <KPICard 
          title="Show-Up Rate" 
          value={formatPercentage(data.show_up_rate)} 
          description="% of calls that attended"
        />
        
        <KPICard 
          title="Closing Rate" 
          value={formatPercentage(data.closing_rate)} 
          description="% of calls that purchased"
        />
        
        <KPICard 
          title="Average Order Value" 
          value={formatCurrency(data.average_order_value)} 
          description="Average revenue per sale"
        />
        
        <KPICard 
          title="Total YouTube Views" 
          value={data.videos.reduce((sum, video) => sum + video.views, 0).toLocaleString()} 
          description="Total views across videos"
        />
      </div>
    </div>
  );
};

export default Dashboard; 