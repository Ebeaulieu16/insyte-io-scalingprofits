from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
import re
from datetime import datetime

from app.database import get_db
from app.models import Link, ClickEvent, VideoMetrics
from app.schemas import LinkCreate, Link as LinkSchema, LinkBase

router = APIRouter(
    prefix="/links",
    tags=["links"],
)

# Helper function to generate a slug from title
def generate_slug(title: str) -> str:
    # Remove special characters and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug

@router.post("/", response_model=LinkSchema, status_code=201)
def create_link(link: LinkCreate, db: Session = Depends(get_db)):
    """
    Create a new tracking link
    """
    # Check if slug already exists
    db_link = db.query(Link).filter(Link.slug == link.slug).first()
    if db_link:
        raise HTTPException(status_code=400, detail="Slug already in use")
    
    # Create new link
    db_link = Link(
        title=link.title,
        slug=link.slug,
        destination_url=str(link.destination_url)
    )
    
    # Also create video metrics entry
    db_video = VideoMetrics(
        slug=link.slug,
        title=link.title
    )
    
    db.add(db_link)
    db.add(db_video)
    db.commit()
    db.refresh(db_link)
    
    return db_link

@router.get("/", response_model=List[LinkSchema])
def get_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all tracking links
    """
    links = db.query(Link).offset(skip).limit(limit).all()
    return links

@router.get("/{slug}", response_model=LinkSchema)
def get_link(slug: str, db: Session = Depends(get_db)):
    """
    Get a specific tracking link by slug
    """
    db_link = db.query(Link).filter(Link.slug == slug).first()
    if db_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    
    return db_link

@router.get("/go/{slug}")
async def redirect_link(slug: str, request: Request, db: Session = Depends(get_db)):
    """
    Redirect to the destination URL with UTM parameters.
    This endpoint also logs the click.
    """
    # Find the link by slug
    db_link = db.query(Link).filter(Link.slug == slug).first()
    if db_link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    
    # Get the associated video metrics
    video = db.query(VideoMetrics).filter(VideoMetrics.slug == slug).first()
    if not video:
        # If video metrics don't exist, create them
        video = VideoMetrics(
            slug=slug,
            title=db_link.title
        )
        db.add(video)
        db.commit()
        db.refresh(video)
    
    # Log the click
    client_host = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    referrer = request.headers.get("referer")
    
    click = ClickEvent(
        video_id=video.id,
        ip_address=client_host,
        user_agent=user_agent,
        referrer=referrer,
        timestamp=datetime.utcnow()
    )
    db.add(click)
    db.commit()
    
    # Build the destination URL with UTM parameters
    destination = db_link.destination_url
    separator = "&" if "?" in destination else "?"
    utm_params = f"utm_source=youtube&utm_medium=video&utm_content={slug}"
    redirect_url = f"{destination}{separator}{utm_params}"
    
    # Return a redirect response
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=redirect_url) 