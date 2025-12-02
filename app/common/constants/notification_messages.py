class NotificationMessages:
    RENTAL_REQUEST_HEADER = "Rental Request"
    RENTAL_REQUEST_MESSAGE = """{username} has submitted a request to rent
    the book '{title}'. This request is now awaiting your confirmation.
    Please review the borrowers details before proceeding. You may accept
    or decline the request in the Lend Requests section."""

    RENTAL_REQUEST_EXPIRED_HEADER = "Rental Request Expired"
    RENTAL_REQUEST_EXPIRED_MESSAGE = """Your request to rent '{title}' from {username} has expired
    because it wasn’t approved in time. If you’re still interested in this book, feel
    free to send a new request or explore similar titles available for rent."""
