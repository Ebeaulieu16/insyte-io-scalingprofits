import logging
from typing import Dict, List, Any, Optional
import requests
import json

from app.config import (
    YOUTUBE_API_KEY,
    STRIPE_API_KEY,
    CALENDLY_API_KEY,
    CALCOM_API_KEY
)

# Set up logging
logger = logging.getLogger(__name__)

def check_youtube_api() -> Dict[str, Any]:
    """
    Check if the YouTube API key is valid and working
    
    Returns:
        Dict with status and details
    """
    if not YOUTUBE_API_KEY:
        return {
            "service": "YouTube API",
            "status": "not_configured",
            "message": "API key not configured"
        }
    
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet",
            "chart": "mostPopular",
            "maxResults": "1",
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return {
                "service": "YouTube API",
                "status": "ok",
                "message": "API connection successful"
            }
        elif response.status_code == 403:
            return {
                "service": "YouTube API",
                "status": "error",
                "message": "Invalid API key or quota exceeded"
            }
        else:
            return {
                "service": "YouTube API",
                "status": "error",
                "message": f"API error: {response.status_code}"
            }
    except Exception as e:
        return {
            "service": "YouTube API",
            "status": "error",
            "message": f"Connection error: {str(e)}"
        }

def check_stripe_api() -> Dict[str, Any]:
    """
    Check if the Stripe API key is valid and working
    
    Returns:
        Dict with status and details
    """
    if not STRIPE_API_KEY:
        return {
            "service": "Stripe API",
            "status": "not_configured",
            "message": "API key not configured"
        }
    
    try:
        # We'll just check a simple endpoint that requires authentication
        url = "https://api.stripe.com/v1/balance"
        headers = {
            "Authorization": f"Bearer {STRIPE_API_KEY}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return {
                "service": "Stripe API",
                "status": "ok",
                "message": "API connection successful"
            }
        elif response.status_code == 401:
            return {
                "service": "Stripe API",
                "status": "error",
                "message": "Invalid API key"
            }
        else:
            return {
                "service": "Stripe API",
                "status": "error",
                "message": f"API error: {response.status_code}"
            }
    except Exception as e:
        return {
            "service": "Stripe API",
            "status": "error",
            "message": f"Connection error: {str(e)}"
        }

def check_calendly_api() -> Dict[str, Any]:
    """
    Check if the Calendly API key is valid and working
    
    Returns:
        Dict with status and details
    """
    if not CALENDLY_API_KEY:
        return {
            "service": "Calendly API",
            "status": "not_configured",
            "message": "API key not configured"
        }
    
    try:
        url = "https://api.calendly.com/users/me"
        headers = {
            "Authorization": f"Bearer {CALENDLY_API_KEY}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return {
                "service": "Calendly API",
                "status": "ok",
                "message": "API connection successful"
            }
        elif response.status_code == 401:
            return {
                "service": "Calendly API",
                "status": "error",
                "message": "Invalid API key"
            }
        else:
            return {
                "service": "Calendly API",
                "status": "error",
                "message": f"API error: {response.status_code}"
            }
    except Exception as e:
        return {
            "service": "Calendly API",
            "status": "error",
            "message": f"Connection error: {str(e)}"
        }

def check_calcom_api() -> Dict[str, Any]:
    """
    Check if the Cal.com API key is valid and working
    
    Returns:
        Dict with status and details
    """
    if not CALCOM_API_KEY:
        return {
            "service": "Cal.com API",
            "status": "not_configured",
            "message": "API key not configured"
        }
    
    try:
        # Cal.com API endpoint might vary, this is a placeholder
        url = "https://api.cal.com/v1/me"
        headers = {
            "Authorization": f"Bearer {CALCOM_API_KEY}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return {
                "service": "Cal.com API",
                "status": "ok",
                "message": "API connection successful"
            }
        elif response.status_code == 401:
            return {
                "service": "Cal.com API",
                "status": "error",
                "message": "Invalid API key"
            }
        else:
            return {
                "service": "Cal.com API",
                "status": "error",
                "message": f"API error: {response.status_code}"
            }
    except Exception as e:
        return {
            "service": "Cal.com API",
            "status": "error", 
            "message": f"Connection error: {str(e)}"
        }

def check_all_apis() -> List[Dict[str, Any]]:
    """
    Check all configured APIs and return their status
    
    Returns:
        List of API status dictionaries
    """
    results = []
    
    results.append(check_youtube_api())
    results.append(check_stripe_api())
    results.append(check_calendly_api())
    results.append(check_calcom_api())
    
    return results 