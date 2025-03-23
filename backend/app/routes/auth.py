from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import requests
import os
from typing import Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.config import YOUTUBE_API_KEY, FRONTEND_URL
from app.models import YouTubeToken

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

# YouTube OAuth settings
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", "http://localhost:8001/api/v1/auth/youtube/callback")

def store_youtube_tokens(db: Session, tokens: dict):
    """
    Store YouTube OAuth tokens in the database.
    
    Args:
        db: Database session
        tokens: Token data from the OAuth response
    """
    # Set all existing tokens to inactive
    db.query(YouTubeToken).filter(YouTubeToken.is_active == True).update({"is_active": False})
    
    # Calculate when the token expires
    expires_at = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
    
    # Create a new token record
    token = YouTubeToken(
        access_token=tokens.get("access_token"),
        refresh_token=tokens.get("refresh_token"),
        token_type=tokens.get("token_type", "Bearer"),
        expires_at=expires_at,
        scope=tokens.get("scope", ""),
        is_active=True
    )
    
    db.add(token)
    db.commit()
    db.refresh(token)
    
    return token

@router.get("/youtube/login")
async def youtube_login():
    """
    Redirect to YouTube OAuth login page
    """
    if not YOUTUBE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="YouTube OAuth client ID not configured")
    
    # Google OAuth2 authorization URL
    auth_url = "https://accounts.google.com/o/oauth2/auth"
    
    # Query parameters
    params = {
        "client_id": YOUTUBE_CLIENT_ID,
        "redirect_uri": YOUTUBE_REDIRECT_URI,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/youtube.readonly",
        "access_type": "offline",
        "prompt": "consent"
    }
    
    # Build the authorization URL with parameters
    auth_url_with_params = f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    # Redirect to Google's authorization page
    return RedirectResponse(url=auth_url_with_params)

@router.get("/youtube/callback")
async def youtube_callback(code: Optional[str] = None, error: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Handle callback from YouTube OAuth
    """
    if error:
        # Redirect to frontend with error message
        return RedirectResponse(url=f"{FRONTEND_URL}/settings?error={error}")
    
    if not code:
        # Redirect to frontend with error message
        return RedirectResponse(url=f"{FRONTEND_URL}/settings?error=no_code")
    
    # Exchange authorization code for access token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": YOUTUBE_CLIENT_ID,
        "client_secret": YOUTUBE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": YOUTUBE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    try:
        # Make the token request
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        
        # Get the tokens
        tokens = token_response.json()
        
        # Store tokens in the database
        store_youtube_tokens(db, tokens)
        
        # Redirect back to frontend with success message
        return RedirectResponse(url=f"{FRONTEND_URL}/settings?success=true")
        
    except requests.RequestException as e:
        # Log the error and redirect with error message
        print(f"Error exchanging code for tokens: {e}")
        return RedirectResponse(url=f"{FRONTEND_URL}/settings?error=token_exchange_failed")

@router.get("/youtube/status")
async def youtube_auth_status(db: Session = Depends(get_db)):
    """
    Check if we have a valid YouTube OAuth token
    """
    from app.services.youtube import get_active_token, refresh_token_if_needed
    
    token = get_active_token(db)
    if not token:
        return {"authenticated": False, "message": "No YouTube OAuth token found"}
    
    if token.is_expired():
        token = refresh_token_if_needed(db, token)
        if not token:
            return {"authenticated": False, "message": "YouTube token expired and refresh failed"}
    
    return {
        "authenticated": True, 
        "expires_at": token.expires_at,
        "scopes": token.scope,
        "updated_at": token.updated_at
    } 