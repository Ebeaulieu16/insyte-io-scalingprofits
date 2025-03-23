from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.api_health import check_all_apis

router = APIRouter(
    prefix="/status",
    tags=["status"],
)

@router.get("/health")
def health_check():
    """
    Simple health check to verify that the API is up and running
    """
    return {"status": "ok", "message": "API is running"}

@router.get("/api-status")
def api_status() -> Dict[str, Any]:
    """
    Check the status of all integrated APIs
    """
    api_statuses = check_all_apis()
    
    # Count statuses
    status_counts = {"ok": 0, "error": 0, "not_configured": 0}
    
    for api in api_statuses:
        if api["status"] in status_counts:
            status_counts[api["status"]] += 1
    
    return {
        "overall_status": "ok" if status_counts["error"] == 0 else "error",
        "apis": api_statuses,
        "summary": status_counts
    }

@router.get("/database")
def database_status(db: Session = Depends(get_db)):
    """
    Check if the database connection is working
    """
    try:
        # Execute a simple query to check the database connection
        db.execute("SELECT 1").fetchall()
        return {"status": "ok", "message": "Database connection is working"}
    except Exception as e:
        return {"status": "error", "message": f"Database error: {str(e)}"} 