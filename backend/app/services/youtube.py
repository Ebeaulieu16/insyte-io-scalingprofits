import requests
import logging
from typing import Dict, Any, List, Optional

from app.config import YOUTUBE_API_KEY

# Set up logging
logger = logging.getLogger(__name__)

# YouTube API base URL
YOUTUBE_API_BASE_URL = "https://www.googleapis.com/youtube/v3"

def get_video_statistics(video_id: str) -> Optional[Dict[str, Any]]:
    """
    Get statistics for a single YouTube video using the API
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dict containing video statistics or None if request fails
    """
    if not YOUTUBE_API_KEY:
        logger.error("YouTube API key is not configured")
        return None
        
    try:
        url = f"{YOUTUBE_API_BASE_URL}/videos"
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