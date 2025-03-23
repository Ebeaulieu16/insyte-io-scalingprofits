from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random
from datetime import datetime, timedelta

# Updated imports to use models from app.models instead of app.models.models
from app.database import get_db
from app.models import VideoMetrics, ClickEvent, BookingEvent, SaleEvent
from app.schemas import VideoMetricsResponse, DashboardResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)

@router.get("/", response_model=DashboardResponse)
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Get aggregated dashboard data including:
    - Total clicks, bookings, sales, revenue
    - Show-up rate, closing rate, average order value
    - Metrics for each video
    """
    
    # Get all videos with their metrics
    videos = db.query(VideoMetrics).all()
    
    if not videos:
        # If no data exists, return empty dashboard
        return DashboardResponse(
            total_clicks=0,
            total_bookings=0,
            total_sales=0,
            total_revenue=0,
            show_up_rate=0,
            closing_rate=0,
            average_order_value=0,
            videos=[]
        )
    
    # Count total clicks
    total_clicks = db.query(ClickEvent).count()
    
    # Count total bookings
    total_bookings = db.query(BookingEvent).count()
    
    # Get sales data
    sales = db.query(SaleEvent).all()
    total_sales = len(sales)
    total_revenue = sum(sale.amount for sale in sales) if sales else 0
    
    # Calculate rates
    show_up_rate = (total_bookings * 0.75) / total_bookings * 100 if total_bookings > 0 else 0
    closing_rate = (total_sales / (total_bookings * 0.75)) * 100 if total_bookings > 0 else 0
    average_order_value = total_revenue / total_sales if total_sales > 0 else 0
    
    # Format video metrics
    video_metrics = []
    for video in videos:
        # Get clicks for this video
        clicks = db.query(ClickEvent).filter(ClickEvent.video_id == video.id).count()
        
        # Get bookings for this video
        bookings = db.query(BookingEvent).join(
            ClickEvent, BookingEvent.click_id == ClickEvent.id
        ).filter(ClickEvent.video_id == video.id).count()
        
        # Get sales for this video
        sales_query = db.query(SaleEvent).join(
            BookingEvent, SaleEvent.booking_id == BookingEvent.id
        ).join(
            ClickEvent, BookingEvent.click_id == ClickEvent.id
        ).filter(ClickEvent.video_id == video.id).all()
        
        sales_count = len(sales_query)
        revenue = sum(sale.amount for sale in sales_query) if sales_query else 0
        
        video_metrics.append(VideoMetricsResponse(
            slug=video.slug,
            title=video.title,
            views=video.views,
            likes=video.likes,
            comments=video.comments,
            avg_watch_time=video.avg_watch_time,
            clicks=clicks,
            bookings=bookings,
            sales=sales_count,
            revenue=revenue
        ))
    
    return DashboardResponse(
        total_clicks=total_clicks,
        total_bookings=total_bookings,
        total_sales=total_sales,
        total_revenue=total_revenue,
        show_up_rate=show_up_rate,
        closing_rate=closing_rate,
        average_order_value=average_order_value,
        videos=video_metrics
    )

@router.post("/mock-data/", status_code=201)
def create_mock_data(db: Session = Depends(get_db)):
    """
    Generate mock data for demonstration purposes
    """
    # Clear existing data
    db.query(SaleEvent).delete()
    db.query(BookingEvent).delete()
    db.query(ClickEvent).delete()
    db.query(VideoMetrics).delete()
    
    # Create sample videos
    video_titles = [
        "How to 10x Your Sales with Content Marketing",
        "The Ultimate Guide to B2B Lead Generation",
        "5 Client Acquisition Strategies That Actually Work",
        "Why Most Sales Funnels Fail (And How to Fix It)",
        "Secrets of High-Ticket Sales Closing"
    ]
    
    videos = []
    for title in video_titles:
        slug = title.lower().replace(" ", "-").replace("(", "").replace(")", "")
        
        # Random video metrics
        views = random.randint(5000, 50000)
        likes = int(views * random.uniform(0.02, 0.08))
        comments = int(views * random.uniform(0.005, 0.02))
        avg_watch_time = random.uniform(120, 600)  # in seconds
        
        video = VideoMetrics(
            slug=slug,
            title=title,
            views=views,
            likes=likes,
            comments=comments,
            avg_watch_time=avg_watch_time
        )
        db.add(video)
        videos.append(video)
    
    db.commit()
    
    # Refresh videos with IDs
    for video in videos:
        db.refresh(video)
    
    # Generate clicks
    clicks = []
    for video in videos:
        # Create between 100-500 clicks per video
        num_clicks = int(video.views * random.uniform(0.01, 0.03))
        for _ in range(num_clicks):
            click_date = datetime.now() - timedelta(days=random.randint(0, 60))
            click = ClickEvent(
                video_id=video.id,
                ip_address=f"192.168.1.{random.randint(1, 255)}",
                user_agent="Mozilla/5.0 (Mock Data)",
                referrer="youtube.com",
                timestamp=click_date
            )
            db.add(click)
            clicks.append(click)
    
    db.commit()
    
    # Refresh clicks with IDs
    for click in clicks:
        db.refresh(click)
    
    # Generate bookings (30-50% of clicks lead to bookings)
    bookings = []
    for click in clicks:
        if random.random() < random.uniform(0.3, 0.5):
            booking_date = click.timestamp + timedelta(hours=random.randint(1, 48))
            booking = BookingEvent(
                click_id=click.id,
                email=f"user{random.randint(1, 999)}@example.com",
                name=f"User {random.randint(1, 999)}",
                timestamp=booking_date
            )
            db.add(booking)
            bookings.append(booking)
    
    db.commit()
    
    # Refresh bookings with IDs
    for booking in bookings:
        db.refresh(booking)
    
    # Generate sales (20-40% of bookings lead to sales)
    for booking in bookings:
        if random.random() < random.uniform(0.2, 0.4):
            sale_date = booking.timestamp + timedelta(days=random.randint(1, 7))
            amount = random.choice([997, 1997, 2997, 4997])
            
            sale = SaleEvent(
                booking_id=booking.id,
                amount=amount,
                timestamp=sale_date
            )
            db.add(sale)
    
    db.commit()
    
    return {"message": "Mock data created successfully"} 