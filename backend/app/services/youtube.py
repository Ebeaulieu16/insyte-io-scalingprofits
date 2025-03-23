import requests
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.config import YOUTUBE_API_KEY, YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET
from app.models import YouTubeToken

# Set up logging
logger = logging.getLogger(__name__)

# YouTube API base URL
YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"

def get_active_token(db: Session) -> Optional[YouTubeToken]:
    """
    Get the most recent active OAuth token.
    
    Args:
        db: Database session
        
    Returns:
        YouTubeToken object or None if no active token
    """
    return db.query(YouTubeToken).filter(YouTubeToken.is_active == True).order_by(YouTubeToken.updated_at.desc()).first()

def refresh_token_if_needed(db: Session, token: YouTubeToken) -> Optional[YouTubeToken]:
    """
    Refresh the token if it's expired.
    
    Args:
        db: Database session
        token: YouTubeToken object
        
    Returns:
        Updated YouTubeToken or None if refresh failed
    """
    if not token.is_expired():
        return token
        
    try:
        # Get new tokens using the refresh token
        refresh_url = "https://oauth2.googleapis.com/token"
        refresh_data = {
            "client_id": YOUTUBE_CLIENT_ID,
            "client_secret": YOUTUBE_CLIENT_SECRET,
            "refresh_token": token.refresh_token,
            "grant_type": "refresh_token"
        }
        
        response = requests.post(refresh_url, data=refresh_data)
        response.raise_for_status()
        
        tokens = response.json()
        
        # Update token
        token.access_token = tokens["access_token"]
        # The response might not include a new refresh token
        if "refresh_token" in tokens:
            token.refresh_token = tokens["refresh_token"]
        token.expires_at = datetime.utcnow() + timedelta(seconds=tokens["expires_in"])
        token.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(token)
        
        return token
    except Exception as e:
        logger.error(f"Failed to refresh token: {e}")
        return None

def get_authorization_header(db: Session = None) -> Dict[str, str]:
    """
    Get authorization header for API requests.
    Tries to use OAuth token first, falls back to API key.
    
    Args:
        db: Database session (optional)
        
    Returns:
        Dict with authorization header
    """
    if db:
        token = get_active_token(db)
        if token:
            token = refresh_token_if_needed(db, token)
            if token:
                return {"Authorization": f"Bearer {token.access_token}"}
    
    # Fall back to API key
    if YOUTUBE_API_KEY:
        return {"X-Key-For-Fallback": "Using API key instead of OAuth token"}
    
    return {}

def get_video_statistics(video_id: str, db: Session = None) -> Optional[Dict[str, Any]]:
    """
    Get statistics for a single YouTube video using the API
    
    Args:
        video_id: YouTube video ID
        db: Database session for OAuth token (optional)
        
    Returns:
        Dict containing video statistics or None if request fails
    """
    try:
        url = f"{YOUTUBE_API_BASE_URL}/videos"
        
        # Try to use OAuth first, fallback to API key
        auth_header = get_authorization_header(db)
        
        if "Authorization" in auth_header:
            # Using OAuth token
            params = {
                "part": "statistics,contentDetails,snippet",
                "id": video_id
            }
            headers = {
                "Authorization": auth_header["Authorization"],
                "Content-Type": "application/json"
            }
            response = requests.get(url, params=params, headers=headers)
        else:
            # Fallback to API key
            if not YOUTUBE_API_KEY:
                logger.error("No YouTube authentication method available (neither OAuth token nor API key)")
                return None
                
            params = {
                "part": "statistics,contentDetails,snippet",
                "id": video_id,
                "key": YOUTUBE_API_KEY
            }
            response = requests.get(url, params=params)
        
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("items"):
            logger.warning(f"No data found for video ID: {video_id}")
            return None
            
        video_data = data["items"][0]
        
        # Extract relevant statistics
        stats = video_data["statistics"]
        details = video_data["contentDetails"]
        snippet = video_data["snippet"]
        
        # Parse duration
        duration = details["duration"]  # In ISO 8601 format
        
        return {
            "title": snippet["title"],
            "views": int(stats.get("viewCount", 0)),
            "likes": int(stats.get("likeCount", 0)),
            "dislikes": int(stats.get("dislikeCount", 0)) if "dislikeCount" in stats else 0,
            "comments": int(stats.get("commentCount", 0)),
            "duration": duration,
            "published_at": snippet["publishedAt"],
            "channel_title": snippet["channelTitle"],
            "description": snippet["description"]
        }
        
    except requests.RequestException as e:
        logger.error(f"YouTube API request failed: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing YouTube API response: {e}")
        return None

def get_channel_statistics(channel_id: str) -> Optional[Dict[str, Any]]:
    """
    Get statistics for a YouTube channel
    
    Args:
        channel_id: YouTube channel ID
        
    Returns:
        Dict containing channel statistics or None if request fails
    """
    if not YOUTUBE_API_KEY:
        logger.error("YouTube API key is not configured")
        return None
        
    try:
        url = f"{YOUTUBE_API_BASE_URL}/channels"
        params = {
            "part": "statistics,snippet,contentDetails",
            "id": channel_id,
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("items"):
            logger.warning(f"No data found for channel ID: {channel_id}")
            return None
            
        channel_data = data["items"][0]
        
        return {
            "title": channel_data["snippet"]["title"],
            "description": channel_data["snippet"]["description"],
            "subscriber_count": int(channel_data["statistics"].get("subscriberCount", 0)),
            "video_count": int(channel_data["statistics"].get("videoCount", 0)),
            "view_count": int(channel_data["statistics"].get("viewCount", 0)),
            "published_at": channel_data["snippet"]["publishedAt"]
        }
        
    except requests.RequestException as e:
        logger.error(f"YouTube API request failed: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing YouTube API response: {e}")
        return None 