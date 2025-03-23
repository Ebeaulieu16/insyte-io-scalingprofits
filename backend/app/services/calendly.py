import requests
import logging
import hmac
import hashlib
from typing import Dict, Any, List, Optional

from app.config import CALENDLY_API_KEY, CALENDLY_WEBHOOK_SECRET

# Set up logging
logger = logging.getLogger(__name__)

# Calendly API base URL
CALENDLY_API_BASE_URL = "https://api.calendly.com"

def get_user_events(user_uri: str, count: int = 10) -> List[Dict[str, Any]]:
    """
    Get scheduled events for a Calendly user
    
    Args:
        user_uri: Calendly user URI
        count: Maximum number of events to return
        
    Returns:
        List of event data or empty list if request fails
    """
    if not CALENDLY_API_KEY:
        logger.error("Calendly API key is not configured")
        return []
        
    try:
        url = f"{CALENDLY_API_BASE_URL}/scheduled_events"
        headers = {
            "Authorization": f"Bearer {CALENDLY_API_KEY}",
            "Content-Type": "application/json"
        }
        params = {
            "user": user_uri,
            "count": count,
            "status": "active"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("collection", [])
    except requests.RequestException as e:
        logger.error(f"Calendly API request failed: {e}")
        return []
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Calendly API response: {e}")
        return []

def get_event_details(event_uuid: str) -> Optional[Dict[str, Any]]:
    """
    Get details for a specific Calendly event
    
    Args:
        event_uuid: Calendly event UUID
        
    Returns:
        Event details or None if request fails
    """
    if not CALENDLY_API_KEY:
        logger.error("Calendly API key is not configured")
        return None
        
    try:
        url = f"{CALENDLY_API_BASE_URL}/scheduled_events/{event_uuid}"
        headers = {
            "Authorization": f"Bearer {CALENDLY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json().get("resource")
    except requests.RequestException as e:
        logger.error(f"Calendly API request failed: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Calendly API response: {e}")
        return None

def get_event_invitees(event_uuid: str) -> List[Dict[str, Any]]:
    """
    Get invitees for a specific Calendly event
    
    Args:
        event_uuid: Calendly event UUID
        
    Returns:
        List of invitee data or empty list if request fails
    """
    if not CALENDLY_API_KEY:
        logger.error("Calendly API key is not configured")
        return []
        
    try:
        url = f"{CALENDLY_API_BASE_URL}/scheduled_events/{event_uuid}/invitees"
        headers = {
            "Authorization": f"Bearer {CALENDLY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json().get("collection", [])
    except requests.RequestException as e:
        logger.error(f"Calendly API request failed: {e}")
        return []
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Calendly API response: {e}")
        return []

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify a Calendly webhook signature
    
    Args:
        payload: Raw webhook payload
        signature: Signature header from Calendly
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not CALENDLY_WEBHOOK_SECRET:
        logger.error("Calendly webhook secret is not configured")
        return False
        
    try:
        computed_signature = hmac.new(
            CALENDLY_WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(computed_signature, signature)
    except Exception as e:
        logger.error(f"Error verifying Calendly webhook signature: {e}")
        return False 