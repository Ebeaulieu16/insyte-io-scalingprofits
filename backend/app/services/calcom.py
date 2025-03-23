import requests
import logging
from typing import Dict, Any, List, Optional

from app.config import CALCOM_API_KEY

# Set up logging
logger = logging.getLogger(__name__)

# Cal.com API base URL - adjust based on whether you're using Cal.com cloud or self-hosted
CALCOM_API_BASE_URL = "https://api.cal.com/v1"

def get_user_events(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get scheduled events for a Cal.com user
    
    Args:
        user_id: Cal.com user ID
        limit: Maximum number of events to return
        
    Returns:
        List of event data or empty list if request fails
    """
    if not CALCOM_API_KEY:
        logger.error("Cal.com API key is not configured")
        return []
        
    try:
        url = f"{CALCOM_API_BASE_URL}/users/{user_id}/bookings"
        headers = {
            "Authorization": f"Bearer {CALCOM_API_KEY}",
            "Content-Type": "application/json"
        }
        params = {
            "limit": limit
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("bookings", [])
    except requests.RequestException as e:
        logger.error(f"Cal.com API request failed: {e}")
        return []
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Cal.com API response: {e}")
        return []

def get_booking_details(booking_id: str) -> Optional[Dict[str, Any]]:
    """
    Get details for a specific Cal.com booking
    
    Args:
        booking_id: Cal.com booking ID
        
    Returns:
        Booking details or None if request fails
    """
    if not CALCOM_API_KEY:
        logger.error("Cal.com API key is not configured")
        return None
        
    try:
        url = f"{CALCOM_API_BASE_URL}/bookings/{booking_id}"
        headers = {
            "Authorization": f"Bearer {CALCOM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Cal.com API request failed: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Cal.com API response: {e}")
        return None

def get_event_types(user_id: str) -> List[Dict[str, Any]]:
    """
    Get available event types for a Cal.com user
    
    Args:
        user_id: Cal.com user ID
        
    Returns:
        List of event type data or empty list if request fails
    """
    if not CALCOM_API_KEY:
        logger.error("Cal.com API key is not configured")
        return []
        
    try:
        url = f"{CALCOM_API_BASE_URL}/users/{user_id}/event-types"
        headers = {
            "Authorization": f"Bearer {CALCOM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        return data.get("event_types", [])
    except requests.RequestException as e:
        logger.error(f"Cal.com API request failed: {e}")
        return []
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Cal.com API response: {e}")
        return []

def create_booking_questions(event_type_id: str, questions: List[Dict[str, Any]]) -> bool:
    """
    Add custom questions to an event type
    
    Args:
        event_type_id: Cal.com event type ID
        questions: List of question objects
        
    Returns:
        True if successful, False otherwise
    """
    if not CALCOM_API_KEY:
        logger.error("Cal.com API key is not configured")
        return False
        
    try:
        url = f"{CALCOM_API_BASE_URL}/event-types/{event_type_id}"
        headers = {
            "Authorization": f"Bearer {CALCOM_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Add a UTM tracking question
        data = {
            "metadata": {
                "smartContractAddress": "",
                "blockchainId": ""
            },
            "bookingFields": questions
        }
        
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        
        return True
    except requests.RequestException as e:
        logger.error(f"Cal.com API request failed: {e}")
        return False
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Cal.com API response: {e}")
        return False

def create_utm_questions(event_type_id: str) -> bool:
    """
    Add UTM tracking questions to an event type
    
    Args:
        event_type_id: Cal.com event type ID
        
    Returns:
        True if successful, False otherwise
    """
    # Define UTM tracking questions
    utm_questions = [
        {
            "type": "text",
            "name": "utm_source",
            "label": "How did you hear about us?",
            "placeholder": "e.g. YouTube, Google, Referral",
            "required": False
        },
        {
            "type": "hidden",
            "name": "utm_campaign",
            "label": "Campaign",
            "required": False
        },
        {
            "type": "hidden",
            "name": "utm_medium",
            "label": "Medium",
            "required": False
        },
        {
            "type": "hidden",
            "name": "utm_content",
            "label": "Content",
            "required": False
        }
    ]
    
    return create_booking_questions(event_type_id, utm_questions) 