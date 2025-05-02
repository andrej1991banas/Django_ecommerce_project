# Andrej Banas Ecommerce Django project - portfolio

![Python](https://img.shields.io/badge/python-3.x-blue.svg) - 4.2.20
![Django](https://img.shields.io/badge/django-4.x-green.svg) - 3.12.5.
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## Description

**Flyfishing Ecommerce** is a Django-based web application that demonstrates backend and frontend development skills. The project simulates a real-world ecommerce application featuring:

- User registration, authentication, and profile management.
- Data storage, retrieval, and CRUD operations for Users, members, products and categories.
- Shopping cart functionality (with persistence for logged-in users).
- Integration of AI (used to generate product descriptions dynamically).
- Product search functionality and responsive UI design
- Admin Analytics Dashboard for sales tracking

This project showcases practical experience in handling **real-time scenarios**, collecting **data-driven demands**, and creating a **user-friendly environment**.

For visuals please check 
Eshop/images/...
or 
Visuals from test with Selenium and Playwright
Eshop/eshop/test/tests_screenshots/...

## Features

- **Authentication System**:
  - User login and logout.
  - 
  - Password management & user profile updates.

- **Product Management**:
  - Add, edit, and delete products and categories (CRUD operations).
  - Category-wise product filtering using dynamic dropdowns.
  - AI-assisted automatic product description generation.
    
- **Shopping Cart**:
  - Add/update/delete products from the cart.
  - Persistence: remembers the cart across sessions.
  - Updated cart summary for logged-in and guest users.
  - Cart total and product listing for easy checkout.

- **Frontend Design**:
  - Fully responsive and built using **Bootstrap**.
  - Dynamic navigation system based on product categories.
 
- **Other Features**:
  - Product details page.
  - Empty cart and category-specific fallbacks.
  - Secure redirections when accessing logged-in user resources (e.g., dashboards).
  - Search bar functionality to quickly find products.

---
###  **Test coverage**
- May/2/2025 82% coverage of whole project

### 1. **Model Testing**
- Ensures correctness of models like `User`, `Member`, `Category`, `Product`,  `Order` and `OrderItems`.
- Verifies the `create`, `read`, `update`, and `delete` operations for all models.
- Tests string representations (`__str__`) for clarity in admin panels.

### 2. **View Testing**
- Confirms HTTP status codes (e.g., 200 OK, 404 Not Found, or 302 Redirect) for several views including:
  - Homepage (`/index`)
  - Category search (`/category/<id>`)
  - Product details (`/product/<id>`)
  - Cart summary (`/cart-summary`)
- Validates rendered content such as buttons, titles, links, or category items using `assertContains`.

### 3. **Cart Functionality**
- Tests cart-related logic and ensures:
  - Products can be added and deleted from the cart.
  - The correct cart total is calculated.
  - The cart allows for user sessions and product persistency.

### 4. **Authentication Flow**
- Verifies redirections for unauthenticated users attempting to access sensitive pages:
  - Dashboard (`/dashboard`)
  - 
  - Update profile (`/update-user`)
  - Password update (`/update-password`)
- Confirms that error messages and redirects function as expected.

### 5. **Category Search**
- Tests dynamic dropdowns and category links.
- Ensures correct product listings and filters are returned for each selected category.
- Handles empty or non-existent categories gracefully (e.g., fallback messages or 404 views).

All test cases can be found in 
Eshop/eshop/test - Unittest, 
Eshop/eshop/test/tests_selenium - test cases with Selenium, 
Eshop/eshop/test/tests_playwright - test cases with Playwright

All screenshots for test cases from the client can be found in Eshop/eshop/test/tests_screenshots

Here is a snippet of some Main Test Cases:

#### Example: Testing Product Details
```python
def test_product_details(self):
    """Test rendering of product details based on their id."""
    url = reverse('product-details', args=[1])
    response = self.client.get(url)

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Fly Rod A')  # Ensures correct product renders
```

## Requirements

- **Python**: Version 3.8 or higher.
- **Framework**: Django 4.2 or higher.
- **Database**: PostgreSQL (SQLite can be used for local development).
- Other dependencies you can install via `Requirements.txt`.



## Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/andrej1991banas/Django_ecommerce_project.git
   cd Django_ecommerce_project
   ```

2. **Create a Virtual Environment (if required)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database**:
   - Modify `DATABASES` in your `settings.py` if needed.
   - Migrate the tables:
     ```bash
     python manage.py migrate
     ```

5. **Run Tests** (Optional):
   ```bash
   python manage.py test
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

   Navigate to `http://127.0.0.1:8000/`.

---


## Future Enhancements

- Add a **Payment Gateway** (e.g., PayPal or Stripe).
- Add a **Imagine Engine** for creating product images with AI tool ComfyUI

- Provide Admin Analytics Dashboard for sales tracking.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

- **Andrej Banas**: Backend & frontend developer passionate about building scalable, user-friendly applications.
