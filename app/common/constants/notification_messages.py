class NotificationMessages:
    # --------------- Rent related

    RENTAL_REQUEST_HEADER = "Rental Request"
    RENTAL_REQUEST_MESSAGE = """{username} has submitted a request to rent
    the book '{title}'. This request is now awaiting your confirmation.
    Please review the borrowers details before proceeding. You may accept
    or decline the request in the Lend Requests section."""

    RENTAL_REQUEST_EXPIRED_HEADER = "Rental Request Expired"
    RENTAL_REQUEST_EXPIRED_MESSAGE = """Your request to rent '{title}' from {username} has expired
    because it was not approved in time. If you are still interested in this book, feel
    free to send a new request or explore similar titles available for rent."""

    RENTAL_REQUEST_APPROVED_HEADER = "Rental Request Approved"
    RENTAL_REQUEST_APPROVED_MESSAGE = """Good news! Your request to rent '{title}' from <owner>
    has been approved. You can now proceed with the next steps to coordinate pickup or delivery.
    We hope you enjoy the book!"""

    PICKUP_REMINDER_HEADER = "Pickup Reminder"
    PICKUP_REMINDER_RENTER_MESSAGE = """Your scheduled pickup for '{title}' is just 1 hour away!
    Please prepare to meet {username} (the owner) at {meetup_location} at the agreed time. Remember
    to bring any necessary identification. We hope you have a smooth exchange and enjoy your reading
    experience!"""
    PICKUP_REMINDER_OWNER_MESSAGE = """The scheduled pickup for '{title}' is just 1 hour away! Please
    prepare to meet {username} (the renter) at {meetup_location} at the agreed time. Remember to bring
    any necessary identification. We hope you have a smooth exchange!"""

    CONFIRM_BOOK_PICKUP_HEADER = "Confirm Book Pickup"
    CONFIRM_BOOK_PICKUP_MESSAGE = """Great news! {username} has confirmed that they have received or
    handed over '{title}' during your scheduled meetup. To complete the pickup process and officially
    start your rental period, we need your confirmation too. Please verify that the book exchange has
    taken place successfully."""

    RENTAL_STARTED_HEADER = "Rental Started"
    RENTAL_STARTED_MESSAGE = """Perfect! Both you and {username} have confirmed the pickup of '{title}'.
    Your rental period is now officially active! The book is in your care until the scheduled return date.
    Enjoy your reading journey, and don't forget to take good care of the book!"""

    RETURN_REMINDER_HEADER = "Return Reminder"
    RETURN_REMINDER_RENTER_MESSAGE = """Your rental period for '{title}' is coming to an end! The
    scheduled return is in just 1 hour at {meetup_location}. Please ensure the book is in the same
    condition as when you received it, and be ready to meet {username} (the owner) for a smooth return
    process."""
    RETURN_REMINDER_OWNER_MESSAGE = """The rental period for '{title}' is coming to an end. The
    scheduled return is in just 1 hour at {meetup_location}. Please ensure the book is in the same
    condition as when you have given it, and be ready to meet {username} (the renter) for a smooth
    return process."""

    RETURN_VERIFICATION_NEEDED_HEADER = "Return Verification Needed"
    RETURN_VERIFICATION_NEEDED_RENTER_MESSAGE = """{username} (the owner) has confirmed that they
    have received '{title}' back during your return meetup. To complete the rental transaction, we
    need your confirmation that the return was successful."""
    RETURN_VERIFICATION_NEEDED_OWNER_MESSAGE = """{username} (the renter) has confirmed that they
    have given '{title}' back during your return meetup. To complete the rental transaction, we
    need your confirmation that the return was successful. Please verify that the book has been
    returned in good condition."""

    RENTAL_COMPLETED_HEADER = "Rental Completed"
    RETURN_COMPLETED_RENTER_MESSAGE = """Excellent! Both parties have confirmed the return of
    '{title}'. Your rental transaction is now complete! We hope you enjoyed the book and had a
    positive experience. Any held funds have been processed, and you can now leave reviews for
    {username} (the owner) to help build our community trust."""
    RETURN_COMPLETED_OWNER_MESSAGE = """Excellent! Both parties have confirmed the return of
    '{title}'. The rental transaction is now complete! Any held funds have been processed, and
    you can now leave reviews for {username} (the renter) to help build our community trust."""

    # --------------- Purchase related
