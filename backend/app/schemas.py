from pydantic import BaseModel, HttpUrl, Field, EmailStr
from typing import List, Optional
from datetime import datetime

# Link schemas
class LinkBase(BaseModel):
    title: str
    slug: str
    destination_url: HttpUrl

class LinkCreate(LinkBase):
    pass

class Link(LinkBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

# Video metrics schemas
class VideoMetricsBase(BaseModel):
    slug: str
    title: str
    views: int = 0
    likes: int = 0
    comments: int = 0
    avg_watch_time: float = 0.0

class VideoMetricsCreate(VideoMetricsBase):
    pass

class VideoMetrics(VideoMetricsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

# Extended video metrics with funnel data
class VideoMetricsResponse(VideoMetricsBase):
    clicks: int = 0
    bookings: int = 0
    sales: int = 0
    revenue: float = 0.0

# Click event schemas
class ClickEventBase(BaseModel):
    ip_address: str
    user_agent: str
    referrer: Optional[str] = None

class ClickEventCreate(ClickEventBase):
    video_id: int

class ClickEvent(ClickEventBase):
    id: int
    video_id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

# Booking event schemas
class BookingEventBase(BaseModel):
    email: EmailStr
    name: str

class BookingEventCreate(BookingEventBase):
    click_id: int

class BookingEvent(BookingEventBase):
    id: int
    click_id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

# Sale event schemas
class SaleEventBase(BaseModel):
    amount: float

class SaleEventCreate(SaleEventBase):
    booking_id: int

class SaleEvent(SaleEventBase):
    id: int
    booking_id: int
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }

# Dashboard response schema
class DashboardResponse(BaseModel):
    total_clicks: int
    total_bookings: int
    total_sales: int
    total_revenue: float
    show_up_rate: float
    closing_rate: float
    average_order_value: float
    videos: List[VideoMetricsResponse] 