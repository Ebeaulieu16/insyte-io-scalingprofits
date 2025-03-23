import asyncio
import schedule
import time
import logging
from datetime import datetime
import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to allow absolute imports
parent_dir = str(Path(__file__).resolve().parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("worker.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import app modules after setting up path
from app.config import YOUTUBE_REFRESH_INTERVAL
from app.services.youtube import get_video_statistics

async def refresh_youtube_data():
    """Refresh all YouTube video data"""
    try:
        # Here we would query the database for all tracked videos
        # and update their metrics
        # This is a simplified placeholder
        logger.info("Starting YouTube data refresh")
        
        # For now, just log that we would update data
        # In the real implementation, you would:
        # 1. Query all VideoMetrics from the database
        # 2. For each video, call get_video_statistics
        # 3. Update the database with new metrics
        
        logger.info(f"YouTube metrics refreshed at {datetime.now().isoformat()}")
        return True
    except Exception as e:
        logger.error(f"Error refreshing YouTube metrics: {e}")
        return False

def run_async_task(coroutine):
    """Run an async task from a sync context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coroutine)
    finally:
        loop.close()

def youtube_refresh_job():
    """Wrapper to run the async refresh job"""
    logger.info("Running scheduled YouTube refresh job")
    success = run_async_task(refresh_youtube_data())
    if success:
        logger.info("YouTube refresh completed successfully")
    else:
        logger.error("YouTube refresh failed")

def start_scheduler():
    """Start the scheduler for periodic tasks"""
    logger.info("Starting scheduler")
    
    # Schedule YouTube refresh
    interval_hours = YOUTUBE_REFRESH_INTERVAL
    logger.info(f"Scheduling YouTube refresh every {interval_hours} hours")
    
    schedule.every(interval_hours).hours.do(youtube_refresh_job)
    
    # Run once at startup
    youtube_refresh_job()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    logger.info("Worker process starting")
    try:
        start_scheduler()
    except KeyboardInterrupt:
        logger.info("Worker process stopped by user")
    except Exception as e:
        logger.error(f"Worker process failed with error: {e}") 