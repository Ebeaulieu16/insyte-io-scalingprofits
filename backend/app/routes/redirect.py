from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

from app.database import get_db
from app.models import Link, VideoMetrics, ClickEvent
from app.services.utm import UTMTracker

router = APIRouter(
    prefix="/go",
    tags=["redirect"],
)

@router.get("/{slug}")
async def redirect_to_destination(
    slug: str, 
    request: Request, 
    db: Session = Depends(get_db)
):
    """
    Redirect to the destination URL with UTM parameters.
    Tracks the click event.
    """
    # Get link by slug
    link = db.query(Link).filter(Link.slug == slug).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Get client info
    client_host = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    referrer = request.headers.get("referer", None)
    
    # Track the click using our UTM tracker service
    UTMTracker.track_click(db, slug, client_host, user_agent, referrer)
    
    # Get default UTM parameters for this slug
    utm_params = UTMTracker.get_default_utm_params(slug)
    
    # Add UTM parameters to the destination URL
    new_url = UTMTracker.add_utm_params(link.destination_url, utm_params)
    
    # Redirect to the destination with UTM parameters
    return RedirectResponse(url=new_url) 