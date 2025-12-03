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
        logger.info("SCHEDULER LOOP STARTED")
        logger.info(f"Current time: {datetime.now()}")
        logger.info("Next run in: 1 minute (60 seconds)")
        logger.info("=" * 60)

        while True:
            try:
                # Wait 1 minute (60 seconds)
                eventlet.sleep(60)

                print("\n" + "=" * 60)
                print(f"SCHEDULER RUN - {datetime.now()}")
                print("=" * 60)

                # Run cleanup and status updates
                with app.app_context():
                    from app.tasks import (
                        RentalCleanupTask,
                        RentalStatusTask,
                        PurchaseCleanupTask,
                        PurchaseStatusTask,
                    )

                    # === RENTAL TASKS ===
                    print("\nRENTAL TASKS:")
                    print("-" * 60)

                    # 1. Clean up expired rentals
                    logger.info("Running cleanup_expired_rentals job...")
                    rental_cleanup_result = RentalCleanupTask.cleanup_expired_rentals()
                    print(f"   • Cleanup: {rental_cleanup_result}")
                    logger.info(f"Rental cleanup completed: {rental_cleanup_result}")

                    # 2. Update approved rentals to pickup confirmation
                    logger.info("Updating rentals to pickup confirmation...")
                    rental_pickup_result = (
                        RentalStatusTask.update_approved_to_pickup_confirmation()
                    )
                    print(f"   • Pickup confirmation: {rental_pickup_result}")
                    logger.info(
                        f"Rental pickup confirmation update: {rental_pickup_result}"
                    )

                    # 3. Update ongoing rentals to return confirmation
                    logger.info("Updating rentals to return confirmation...")
                    rental_return_result = (
                        RentalStatusTask.update_ongoing_to_return_confirmation()
                    )
                    print(f"   • Return confirmation: {rental_return_result}")
                    logger.info(
                        f"Rental return confirmation update: {rental_return_result}"
                    )

                    # === PURCHASE TASKS ===
                    print("\nPURCHASE TASKS:")
                    print("-" * 60)

                    # 4. Clean up expired purchases
                    logger.info("Running cleanup_expired_purchases job...")
                    purchase_cleanup_result = (
                        PurchaseCleanupTask.cleanup_expired_purchases()
                    )
                    print(f"   • Cleanup: {purchase_cleanup_result}")
                    logger.info(
                        f"Purchase cleanup completed: {purchase_cleanup_result}"
                    )

                    # 5. Update approved purchases to pickup confirmation
                    logger.info("Updating purchases to pickup confirmation...")
                    purchase_pickup_result = (
                        PurchaseStatusTask.update_approved_to_pickup_confirmation()
                    )
                    print(f"   • Pickup confirmation: {purchase_pickup_result}")
                    logger.info(
                        f"Purchase pickup confirmation update: {purchase_pickup_result}"
                    )

                    print("\n" + "=" * 60 + "\n")

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
    print("   RENTALS:")
    print("      • Cleanup expired rentals")
    print("      • Update to pickup confirmation (1hr before meetup)")
    print("      • Update to return confirmation (1hr before return)")
    print("   PURCHASES:")
    print("      • Cleanup expired purchases")
    print("      • Update to pickup confirmation (1hr before meetup)")
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
        from app.tasks import RentalCleanupTask, PurchaseCleanupTask

        logger.info("Manually running cleanups...")

        rental_result = RentalCleanupTask.cleanup_expired_rentals()
        logger.info(f"Manual rental cleanup completed: {rental_result}")

        purchase_result = PurchaseCleanupTask.cleanup_expired_purchases()
        logger.info(f"Manual purchase cleanup completed: {purchase_result}")

        return {"rental_cleanup": rental_result, "purchase_cleanup": purchase_result}


def run_status_update_now(app: Flask):
    """
    Manually trigger status updates immediately (useful for testing).
    """
    with app.app_context():
        from app.tasks import RentalStatusTask, PurchaseStatusTask

        print("\n" + "=" * 60)
        print("MANUAL STATUS UPDATE TEST")
        print("=" * 60)

        logger.info("Manually running status updates...")

        # Rental updates
        print("\nRENTAL UPDATES:")
        print("-" * 60)

        print("\nTesting rental pickup confirmation updates...")
        rental_pickup_result = RentalStatusTask.update_approved_to_pickup_confirmation()
        print(f"Result: {rental_pickup_result}")
        logger.info(f"Rental pickup confirmation update: {rental_pickup_result}")

        print("\nTesting rental return confirmation updates...")
        rental_return_result = RentalStatusTask.update_ongoing_to_return_confirmation()
        print(f"Result: {rental_return_result}")
        logger.info(f"Rental return confirmation update: {rental_return_result}")

        # Purchase updates
        print("\nPURCHASE UPDATES:")
        print("-" * 60)

        print("\nTesting purchase pickup confirmation updates...")
        purchase_pickup_result = (
            PurchaseStatusTask.update_approved_to_pickup_confirmation()
        )
        print(f"Result: {purchase_pickup_result}")
        logger.info(f"Purchase pickup confirmation update: {purchase_pickup_result}")

        print("=" * 60 + "\n")

        return {
            "rental_pickup_updates": rental_pickup_result,
            "rental_return_updates": rental_return_result,
            "purchase_pickup_updates": purchase_pickup_result,
        }
