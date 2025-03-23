from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import json
import logging

from app.database import get_db
from app.models import Link, VideoMetrics, ClickEvent, BookingEvent, SaleEvent
from app.services.utm import UTMTracker
from app.services.calendly import verify_webhook_signature as verify_calendly_signature
from app.services.stripe import verify_webhook_signature as verify_stripe_signature

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
)

@router.post("/calendly")
async def calendly_webhook(
    request: Request,
    signature: Optional[str] = Header(None, alias="Calendly-Webhook-Signature"),
    db: Session = Depends(get_db)
):
    """
    Handle Calendly webhook events
    """
    body = await request.body()
    
    # Verify signature if provided
    if signature and not verify_calendly_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        data = json.loads(body)
        event_type = data.get("event")
        payload = data.get("payload", {})
        
        if event_type == "invitee.created":
            # This means a booking was created
            
            # Extract booking info
            invitee = payload.get("invitee", {})
            email = invitee.get("email")
            name = invitee.get("name")
            
            # Try to find UTM parameters in custom questions or tracking
            utm_source = None
            utm_campaign = None
            
            # Look in tracking parameters
            tracking = payload.get("tracking", {})
            utm_source = tracking.get("utm_source")
            utm_campaign = tracking.get("utm_campaign")
            
            # Look in questions for tracking info
            questions_and_answers = invitee.get("questions_and_answers", [])
            for qa in questions_and_answers:
                question = qa.get("question", "").lower()
                answer = qa.get("answer", "")
                
                if "how did you hear" in question or "referral" in question:
                    if not utm_source:
                        utm_source = answer
                
            # If we have UTM info, try to find the click event
            if utm_campaign:
                # Find the video by slug/campaign
                video = db.query(VideoMetrics).filter(VideoMetrics.slug == utm_campaign).first()
                
                if video:
                    # Find the most recent click from this email if possible
                    # This is a simplified attribution - in a real system you'd use cookies/user IDs
                    
                    # For now, just get the most recent click for this video
                    click = db.query(ClickEvent).filter(
                        ClickEvent.video_id == video.id
                    ).order_by(ClickEvent.timestamp.desc()).first()
                    
                    if click:
                        # Record the booking and link it to this click
                        UTMTracker.track_booking(db, click.id, email, name)
                        
                        return {"status": "success", "message": "Booking tracked successfully"}
            
            # If we couldn't find a click to attribute to, log it
            logger.warning(f"Couldn't attribute booking from {email} to a specific click")
            
            return {"status": "success", "message": "Webhook received, but couldn't attribute booking"}
            
        return {"status": "success", "message": "Webhook received"}
        
    except Exception as e:
        logger.error(f"Error processing Calendly webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    signature: Optional[str] = Header(None, alias="Stripe-Signature"),
    db: Session = Depends(get_db)
):
    """
    Handle Stripe webhook events
    """
    body = await request.body()
    
    # Verify signature if provided
    if signature and not verify_stripe_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        data = json.loads(body)
        event_type = data.get("type")
        
        if event_type == "checkout.session.completed" or event_type == "payment_intent.succeeded":
            # Extract customer email
            payload = data.get("data", {}).get("object", {})
            customer_email = payload.get("customer_email") or payload.get("receipt_email")
            amount = payload.get("amount_total") or payload.get("amount")
            
            if amount:
                # Convert from cents to dollars for Stripe
                amount = amount / 100
            
            # Get metadata to look for UTM or tracking info
            metadata = payload.get("metadata", {})
            booking_id = metadata.get("booking_id")
            
            if booking_id:
                # If we have a booking ID in the metadata, use it directly
                booking = db.query(BookingEvent).filter(BookingEvent.id == booking_id).first()
                
                if booking:
                    # Record the sale
                    UTMTracker.track_sale(db, booking.id, amount)
                    return {"status": "success", "message": "Sale tracked successfully"}
            
            # If we don't have booking ID, try to find by email
            if customer_email:
                # Find the most recent booking with this email
                booking = db.query(BookingEvent).filter(
                    BookingEvent.email == customer_email
                ).order_by(BookingEvent.timestamp.desc()).first()
                
                if booking:
                    # Record the sale
                    UTMTracker.track_sale(db, booking.id, amount)
                    return {"status": "success", "message": "Sale tracked successfully"}
            
            # If we couldn't find a booking to attribute to, log it
            logger.warning(f"Couldn't attribute sale of ${amount} to a specific booking")
            
            return {"status": "success", "message": "Webhook received, but couldn't attribute sale"}
            
        return {"status": "success", "message": "Webhook received"}
        
    except Exception as e:
        logger.error(f"Error processing Stripe webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing webhook: {str(e)}")

@router.get("/attribution/{sale_id}")
async def get_attribution(
    sale_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the complete attribution chain for a sale
    """
    attribution = UTMTracker.get_attribution_chain(db, sale_id)
    
    if not attribution:
        raise HTTPException(status_code=404, detail="Sale not found or attribution chain incomplete")
        
    return attribution 