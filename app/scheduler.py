import eventlet
from flask import Flask
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Global variable to track if scheduler is running
_scheduler_greenthread = None


def init_scheduler(app: Flask):
    """
    Initialize cleanup scheduler using eventlet (compatible with SocketIO).
    """
    global _scheduler_greenthread

    def scheduler_loop():
        """Run cleanup every minute."""
        logger.info("=" * 60)
        logger.info("🚀 SCHEDULER LOOP STARTED")
        logger.info(f"⏰ Current time: {datetime.now()}")
        logger.info("⏱️  Next cleanup in: 1 minute (60 seconds)")
        logger.info("=" * 60)

        while True:
            try:
                # Wait 1 minute (60 seconds)
                eventlet.sleep(60)

                # Run cleanup
                with app.app_context():
                    from app.tasks import RentalCleanupTask

                    logger.info("🧹 Running cleanup_expired_rentals job...")
                    result = RentalCleanupTask.cleanup_expired_rentals()
                    logger.info(f"✅ Cleanup job completed: {result}")
            except Exception as e:
                logger.error(f"❌ Cleanup job failed: {str(e)}")

    # Start the scheduler in a greenthread
    _scheduler_greenthread = eventlet.spawn(scheduler_loop)

    # Print to console (not just log)
    print("\n" + "=" * 60)
    print("✅ EVENTLET SCHEDULER STARTED SUCCESSFULLY")
    print("⏰ Cleanup job will run every minute")
    print(
        f"🕐 First run at: {datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=1)}"
    )
    print("=" * 60 + "\n")

    logger.info("✅ Eventlet scheduler started - Cleanup runs every minute")

    return _scheduler_greenthread


def run_cleanup_now(app: Flask):
    """
    Manually trigger cleanup immediately (useful for testing).
    """
    with app.app_context():
        from app.tasks import RentalCleanupTask

        logger.info("🧹 Manually running cleanup_expired_rentals...")
        result = RentalCleanupTask.cleanup_expired_rentals()
        logger.info(f"✅ Manual cleanup completed: {result}")
        return result
