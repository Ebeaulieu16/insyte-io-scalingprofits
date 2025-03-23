import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Link, VideoMetrics, ClickEvent, BookingEvent, SaleEvent
from app.database import get_db

# Set up logging
logger = logging.getLogger(__name__)

class UTMTracker:
    """
    Service to handle UTM tracking throughout the user journey
    """
    
    # Standard UTM parameters
    UTM_PARAMS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]
    
    @staticmethod
    def add_utm_params(url: str, params: Dict[str, str]) -> str:
        """
        Add UTM parameters to a URL
        
        Args:
            url: Base URL
            params: Dict of UTM parameters
            
        Returns:
            URL with UTM parameters added
        """
        # Parse the URL
        parsed_url = urlparse(url)
        
        # Get existing query parameters
        query_params = parse_qs(parsed_url.query)
        
        # Add UTM parameters
        for key, value in params.items():
            query_params[key] = [value]
        
        # Rebuild the query string
        new_query = urlencode(query_params, doseq=True)
        
        # Reconstruct the URL
        return urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))
    
    @staticmethod
    def extract_utm_params(url: str) -> Dict[str, str]:
        """
        Extract UTM parameters from a URL
        
        Args:
            url: URL with UTM parameters
            
        Returns:
            Dict of UTM parameters
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        utm_params = {}
        for param in UTMTracker.UTM_PARAMS:
            if param in query_params:
                utm_params[param] = query_params[param][0]
                
        return utm_params
    
    @staticmethod
    def get_default_utm_params(slug: str) -> Dict[str, str]:
        """
        Get default UTM parameters for a video
        
        Args:
            slug: Video slug
            
        Returns:
            Dict of UTM parameters
        """
        return {
            "utm_source": "youtube",
            "utm_medium": "video",
            "utm_campaign": slug,
            "utm_content": "description"
        }
    
    @staticmethod
    def track_click(db: Session, slug: str, ip_address: str, user_agent: str, 
                   referrer: Optional[str] = None) -> ClickEvent:
        """
        Track a click event
        
        Args:
            db: Database session
            slug: Video slug
            ip_address: Client IP address
            user_agent: User agent string
            referrer: Referrer URL
            
        Returns:
            Created ClickEvent object
        """
        # Find video metrics for this slug
        video = db.query(VideoMetrics).filter(VideoMetrics.slug == slug).first()
        
        if not video:
            # Try to find the link to get the title
            link = db.query(Link).filter(Link.slug == slug).first()
            title = link.title if link else slug
            
            # Create video metrics if they don't exist
            video = VideoMetrics(
                slug=slug,
                title=title
            )
            db.add(video)
            db.commit()
            db.refresh(video)
        
        # Record click
        click = ClickEvent(
            video_id=video.id,
            ip_address=ip_address,
            user_agent=user_agent,
            referrer=referrer,
            timestamp=datetime.utcnow()
        )
        
        db.add(click)
        db.commit()
        db.refresh(click)
        
        return click
    
    @staticmethod
    def track_booking(db: Session, click_id: int, email: str, name: str) -> BookingEvent:
        """
        Track a booking event
        
        Args:
            db: Database session
            click_id: ID of the associated click event
            email: User email
            name: User name
            
        Returns:
            Created BookingEvent object
        """
        booking = BookingEvent(
            click_id=click_id,
            email=email,
            name=name,
            timestamp=datetime.utcnow()
        )
        
        db.add(booking)
        db.commit()
        db.refresh(booking)
        
        return booking
    
    @staticmethod
    def track_sale(db: Session, booking_id: int, amount: float) -> SaleEvent:
        """
        Track a sale event
        
        Args:
            db: Database session
            booking_id: ID of the associated booking event
            amount: Sale amount
            
        Returns:
            Created SaleEvent object
        """
        sale = SaleEvent(
            booking_id=booking_id,
            amount=amount,
            timestamp=datetime.utcnow()
        )
        
        db.add(sale)
        db.commit()
        db.refresh(sale)
        
        return sale
    
    @staticmethod
    def get_attribution_chain(db: Session, sale_id: int) -> Dict[str, Any]:
        """
        Get the complete attribution chain for a sale
        
        Args:
            db: Database session
            sale_id: Sale event ID
            
        Returns:
            Dict with the complete attribution chain
        """
        sale = db.query(SaleEvent).filter(SaleEvent.id == sale_id).first()
        if not sale:
            return None
            
        booking = db.query(BookingEvent).filter(BookingEvent.id == sale.booking_id).first()
        if not booking:
            return None
            
        click = db.query(ClickEvent).filter(ClickEvent.id == booking.click_id).first()
        if not click:
            return None
            
        video = db.query(VideoMetrics).filter(VideoMetrics.id == click.video_id).first()
        if not video:
            return None
            
        # Build the attribution chain
        return {
            "sale": {
                "id": sale.id,
                "amount": sale.amount,
                "timestamp": sale.timestamp
            },
            "booking": {
                "id": booking.id,
                "email": booking.email,
                "name": booking.name,
                "timestamp": booking.timestamp
            },
            "click": {
                "id": click.id,
                "ip_address": click.ip_address,
                "user_agent": click.user_agent,
                "referrer": click.referrer,
                "timestamp": click.timestamp
            },
            "video": {
                "id": video.id,
                "slug": video.slug,
                "title": video.title,
                "views": video.views,
                "likes": video.likes,
                "comments": video.comments
            }
        } 