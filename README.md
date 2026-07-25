# BackendCommerce API

A RESTful e-commerce backend built with **Django** and **Django REST Framework**. It provides JWT-authenticated endpoints for managing product categories, products, and customer orders, with interactive API documentation powered by **drf-spectacular**.

> ⚠️ **Status:** This project is a work in progress. Features, endpoints, and models may still change.

---

## Features

- **JWT Authentication** via `rest_framework_simplejwt`
- **Category management** with parent/child hierarchy and product counts per category
- **Product catalog** with:
  - Search, filtering (by category, price range, stock, name), and ordering
  - Pagination (configurable page size)
  - Admin-only create/update/delete, public read access
- **Order management**:
  - Stock validation before order creation
  - Automatic stock deduction and total price calculation
  - Customers can only view/modify their own orders; admins have full access
  - Only `PENDING` orders can have their items modified
  - Order filtering by status, date, and total price
- **Interactive API docs** with Swagger UI and ReDoc (via `drf-spectacular`)
- **Request profiling** with `django-silk`
- **Environment-based configuration** using `python-decouple`

---

## Tech Stack

| Component        | Technology                          |
|-------------------|--------------------------------------|
| Framework         | Django 6.0                          |
| API               | Django REST Framework               |
| Auth              | Simple JWT                          |
| Filtering         | django-filter                       |
| API Docs          | drf-spectacular + sidecar           |
| Profiling         | django-silk                         |
| Database          | SQLite (development)                |
| Config management | python-decouple                     |

---

## Project Structure

```
backendCommerce-api/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/          # Custom user model, seed data
│   ├── categories/     # Category model, API, seed command
│   ├── products/       # Product model, filters, API
│   └── orders/         # Order & OrderItem models, API, filters
├── db.sqlite3           # (ignored by git)
└── manage.py
```

Each app follows a consistent layout: `models.py`, `serializers.py`, `views.py`, and (where applicable) `filters.py` and a `management/commands/seed_*.py` command for seeding sample data.

---

## Getting Started

### Prerequisites

- Python 3.11+
- pip / virtualenv

### Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd backendCommerce-api
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   TIME_ZONE=UTC
   ```

5. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

6. **Seed sample data** (optional, but recommended for local testing)
   ```bash
   python manage.py seed_users
   python manage.py seed_categories
   python manage.py seed_products
   python manage.py seed_orders
   ```

7. **Create a superuser** (for admin-only endpoints)
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

---

## API Documentation

Once the server is running, interactive documentation is available at:

- **Swagger UI:** `/api/docs/` *(path depends on your `urls.py` configuration)*
- **ReDoc:** `/api/redoc/`
- **Schema (raw):** `/api/schema/`

> Note: Confirm the exact doc URLs against your project's `urls.py`, since `SERVE_INCLUDE_SCHEMA` is currently set to `False` in settings.

---

## Key Endpoints (overview)

| Resource     | Endpoint              | Notes                                             |
|--------------|------------------------|----------------------------------------------------|
| Categories   | `GET /categories/`     | Parent categories with children & product counts   |
| Products     | `GET /products/`       | Search, filter, order, paginate                     |
| Products     | `POST /products/`      | Admin only                                          |
| Products     | `GET/PUT/PATCH/DELETE /products/<slug>/` | Update/delete restricted to admins    |
| Orders       | `GET /orders/`         | Customers see own orders, admins see all            |
| Orders       | `POST /orders/`        | Validates stock, deducts inventory, computes total  |
| Orders       | `PUT/PATCH /orders/<order_id>/` | Only allowed while order is `PENDING`      |
| Orders       | `DELETE /orders/<order_id>/`    | Admin only                                 |

Authentication is required for order endpoints (JWT `Authorization: Bearer <token>` header).

---

## Notes

- `db.sqlite3` is excluded from version control via `.gitignore`; each environment should run migrations and seed commands locally.
- Access tokens expire after 30 minutes; refresh tokens last 7 days (see `SIMPLE_JWT` settings).
- This README will be updated as new apps/features (e.g., payments, reviews, cart) are added.

---

## License

This project is currently unlicensed / private, pending further development.