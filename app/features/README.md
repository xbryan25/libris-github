## 🧠 Notes for Developers

### 🏗️ Architecture Overview

The application follows a **feature-based architecture** with clear separation of concerns:
routes → controllers → services → repository → database

Each feature folder represents a business domain (e.g., Users, Books, Wallets) and contains its own logic stack.

### 🧩 Feature Folder Structure

Each feature may include the following layers:

- **`routes.py`** → Defines Flask Blueprints and API endpoints.  
- **`controllers.py`** → Handles request validation, response formatting, and coordinates with the service layer.  
- **`services.py`** → Contains business logic; coordinates between controllers and repository.  
- **`repository.py`** → Handles direct database queries using **raw SQL**.  

This structure allows each feature to be developed, tested, and maintained independently.

### ⚙️ Common Folder

The **`common/`** folder contains reusable logic shared across features:

- **`/dataclasses`** → Shared dataclasses used across multiple features.  
- **`/constants`** → Feature-wide constants and enums.  
- 
### 🧩 Feature Folder Structure

Each feature includes the following layers:

- **`routes.py`** → Defines Flask Blueprints and API endpoints.  
- **`controllers.py`** → Handles request validation, response formatting, and coordinates with the service layer.  
- **`services.py`** → Contains business logic; coordinates between controllers and repository.  
- **`repository.py`** → Handles direct database queries using **raw SQL**.  

Each feature can be developed, tested, and maintained independently.

#### ⚙️ Class-Based Structure

All `.py` files **except** for `routes.py` are implemented using **classes with static methods** for clean organization and easier importing across features.

Example pattern:

```python
# controllers.py
class UserController:
    @staticmethod
    def create_user(data):
        # service call
        return UserService.create_user(data)
```

### 🔄 Data Flow Example

Client Request

routes.py → Receives request and maps to controller

↓

controllers.py → Validates input, calls service layer

↓

services.py → Applies business logic, calls repository

↓

repository.py → Executes raw SQL from `app/features/queries` and returns results

↓

Response → Returned to controller, formatted for API

### 💡 Development Notes

- Keep **SQL queries** inside the `app/features/queries`, which will be called by the `repository` layer — never mix raw queries in controllers or services.  
- Always perform **input validation** in controllers even if frontend already validates it. This is done because the routes may be called using cURL or Postman. 
- Use **dataclasses** to pass structured data between layers cleanly.  
- The **common** folder should remain framework-agnostic and reusable.  
- All features should follow the same file naming convention for consistency.

## 🧩 Feature-to-Database Mapping

### 🧑‍💻 Users
- **users** – Stores user credentials and profile info  
- **user_address** – Linked one-to-one with users for address details  
- **user_ratings** – Stores feedback and ratings between users  

### 📚 Books
- **books** – Main book data (title, author, price, etc.)  
- **book_images** – Images associated with each book  

### 📦 Rentals
- **rented_books** – Tracks books currently or previously rented by users  

### 🛒 Purchases
- **purchased_books** – Records books purchased by users  

### 💰 Wallets
- **wallets** – Tracks each user's balance  
- **transactions** – Logs all balance changes (top-ups, deductions, etc.)  

### 🔔 Notifications
- **notifications** – Stores in-app notifications for users

### Dashboard
- **dashboard** - Displays users' stats (e.g count of books borrowed, currently lengind, etc) in dashboard page
  