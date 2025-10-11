from .books import books_bp
from .notifications import notifications_bp
from .purchases import purchases_bp
from .rentals import rentals_bp
from .users import users_bp
from .wallets import wallets_bp

blueprints = {
    "books": books_bp,
    "notifications": notifications_bp,
    "purchases": purchases_bp,
    "rentals": rentals_bp,
    "users": users_bp,
    "wallets": wallets_bp,
}
