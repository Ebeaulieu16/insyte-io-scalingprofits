import stripe
import logging
from typing import Dict, Any, List, Optional

from app.config import STRIPE_API_KEY, STRIPE_WEBHOOK_SECRET

# Set up logging
logger = logging.getLogger(__name__)

# Configure Stripe with API key
if STRIPE_API_KEY:
    stripe.api_key = STRIPE_API_KEY
else:
    logger.warning("Stripe API key not configured")

def get_customer(customer_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a Stripe customer by ID
    
    Args:
        customer_id: Stripe customer ID
        
    Returns:
        Customer data or None if request fails
    """
    if not STRIPE_API_KEY:
        logger.error("Stripe API key is not configured")
        return None
        
    try:
        customer = stripe.Customer.retrieve(customer_id)
        return customer
    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error: {e}")
        return None

def get_payment(payment_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a Stripe payment intent by ID
    
    Args:
        payment_id: Stripe payment intent ID
        
    Returns:
        Payment data or None if request fails
    """
    if not STRIPE_API_KEY:
        logger.error("Stripe API key is not configured")
        return None
        
    try:
        payment = stripe.PaymentIntent.retrieve(payment_id)
        return payment
    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error: {e}")
        return None

def list_recent_payments(limit: int = 10) -> List[Dict[str, Any]]:
    """
    List recent Stripe payments
    
    Args:
        limit: Maximum number of payments to return
        
    Returns:
        List of payment data or empty list if request fails
    """
    if not STRIPE_API_KEY:
        logger.error("Stripe API key is not configured")
        return []
        
    try:
        payments = stripe.PaymentIntent.list(limit=limit)
        return payments.get("data", [])
    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error: {e}")
        return []

def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """
    Verify a Stripe webhook signature
    
    Args:
        payload: Raw webhook payload
        signature: Signature header from Stripe
        
    Returns:
        True if signature is valid, False otherwise
    """
    if not STRIPE_WEBHOOK_SECRET:
        logger.error("Stripe webhook secret is not configured")
        return False
        
    try:
        stripe.Webhook.construct_event(
            payload, signature, STRIPE_WEBHOOK_SECRET
        )
        return True
    except (stripe.error.SignatureVerificationError, ValueError) as e:
        logger.error(f"Invalid webhook signature: {e}")
        return False

def create_checkout_session(
    price_id: str,
    success_url: str,
    cancel_url: str,
    customer_email: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None
) -> Optional[str]:
    """
    Create a Stripe Checkout session
    
    Args:
        price_id: Stripe Price ID
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect after cancelled payment
        customer_email: Optional customer email
        metadata: Optional metadata to attach to the checkout session
        
    Returns:
        Checkout session URL or None if creation fails
    """
    if not STRIPE_API_KEY:
        logger.error("Stripe API key is not configured")
        return None
        
    try:
        checkout_params = {
            "payment_method_types": ["card"],
            "line_items": [{"price": price_id, "quantity": 1}],
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
        }
        
        if customer_email:
            checkout_params["customer_email"] = customer_email
            
        if metadata:
            checkout_params["metadata"] = metadata
            
        session = stripe.checkout.Session.create(**checkout_params)
        return session.url
    except stripe.error.StripeError as e:
        logger.error(f"Stripe API error: {e}")
        return None 