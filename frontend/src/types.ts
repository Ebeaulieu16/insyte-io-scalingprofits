// Video Metrics interface
export interface VideoMetrics {
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

// Dashboard Data interface
export interface DashboardData {
  total_clicks: number;
  total_bookings: number;
  total_sales: number;
  total_revenue: number;
  show_up_rate: number;
  closing_rate: number;
  average_order_value: number;
  videos: VideoMetrics[];
}

// Link interface
export interface Link {
  id: number;
  slug: string;
  title: string;
  destination_url: string;
  created_at: string;
}

// New Link interface for creating links
export interface NewLink {
  title: string;
  destination_url: string;
  slug?: string;
}

// API configuration
export const API_BASE_URL = 'http://127.0.0.1:8001'; 