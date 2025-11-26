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
        """Run cleanup and status updates every minute."""
        logger.info("=" * 60)
        logger.info("🚀 SCHEDULER LOOP STARTED")
        logger.info(f"⏰ Current time: {datetime.now()}")
        logger.info("⏱️  Next run in: 1 minute (60 seconds)")
        logger.info("=" * 60)

        while True:
            try:
                # Wait 1 minute (60 seconds)
                eventlet.sleep(60)

                print("\n" + "=" * 60)
                print(f"⏰ SCHEDULER RUN - {datetime.now()}")
                print("=" * 60)

                # Run cleanup and status updates
                with app.app_context():
                    from app.tasks import RentalCleanupTask, RentalStatusTask

                    # 1. Clean up expired rentals
                    print("\n Running cleanup_expired_rentals job...")
                    logger.info("Running cleanup_expired_rentals job...")
                    cleanup_result = RentalCleanupTask.cleanup_expired_rentals()
                    print(f"Cleanup job completed: {cleanup_result}")
                    logger.info(f"Cleanup job completed: {cleanup_result}")

                    # 2. Update approved rentals to pickup confirmation
                    print("\nUpdating rentals to pickup confirmation...")
                    logger.info("Updating rentals to pickup confirmation...")
                    pickup_result = (
                        RentalStatusTask.update_approved_to_pickup_confirmation()
                    )
                    print(f"Pickup confirmation update: {pickup_result}")
                    logger.info(f"Pickup confirmation update: {pickup_result}")

                    # 3. Update ongoing rentals to return confirmation
                    print("\nUpdating rentals to return confirmation...")
                    logger.info("Updating rentals to return confirmation...")
                    return_result = (
                        RentalStatusTask.update_ongoing_to_return_confirmation()
                    )
                    print(f"Return confirmation update: {return_result}")
                    logger.info(f"Return confirmation update: {return_result}")

                    print("=" * 60 + "\n")

            except Exception as e:
                print(f"Scheduler job failed: {str(e)}")
                logger.error(f"Scheduler job failed: {str(e)}")
                import traceback

                traceback.print_exc()

    # Start the scheduler in a greenthread
    _scheduler_greenthread = eventlet.spawn(scheduler_loop)

    # Print to console (not just log)
    print("\n" + "=" * 60)
    print("EVENTLET SCHEDULER STARTED SUCCESSFULLY")
    print("Jobs will run every minute:")
    print("   • Cleanup expired rentals")
    print("   • Update to pickup confirmation (1hr before meetup)")
    print("   • Update to return confirmation (1hr before return)")
    print(
        f"First run at: {datetime.now().replace(second=0, microsecond=0) + timedelta(minutes=1)}"
    )
    print("=" * 60 + "\n")

    logger.info("Eventlet scheduler started - Jobs run every minute")

    return _scheduler_greenthread


def run_cleanup_now(app: Flask):
    """
    Manually trigger cleanup immediately (useful for testing).
    """
    with app.app_context():
        from app.tasks import RentalCleanupTask

        logger.info("Manually running cleanup_expired_rentals...")
        result = RentalCleanupTask.cleanup_expired_rentals()
        logger.info(f"Manual cleanup completed: {result}")
        return result


def run_status_update_now(app: Flask):
    """
    Manually trigger status updates immediately (useful for testing).
    """
    with app.app_context():
        from app.tasks import RentalStatusTask

        print("\n" + "=" * 60)
        print("MANUAL STATUS UPDATE TEST")
        print("=" * 60)

        logger.info("Manually running status updates...")

        print("\nTesting pickup confirmation updates...")
        pickup_result = RentalStatusTask.update_approved_to_pickup_confirmation()
        print(f"Result: {pickup_result}")
        logger.info(f"Pickup confirmation update: {pickup_result}")

        print("\nTesting return confirmation updates...")
        return_result = RentalStatusTask.update_ongoing_to_return_confirmation()
        print(f"Result: {return_result}")
        logger.info(f"Return confirmation update: {return_result}")

        print("=" * 60 + "\n")

        return {"pickup_updates": pickup_result, "return_updates": return_result}
