<div align="center">

# 🛒 BackendCommerce API

**A production-style RESTful e-commerce backend built with Django REST Framework**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.17-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![Tested with pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Stripe](https://img.shields.io/badge/Payments-Stripe-635BFF?logo=stripe&logoColor=white)](https://stripe.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[**Live API Docs (Swagger UI)**](https://backend-commerce-api.onrender.com/api/schema/swagger-ui/) · [ReDoc](https://backend-commerce-api.onrender.com/api/schema/redoc/) · [Report an Issue](../../issues)

</div>

---

## 📖 Overview

**BackendCommerce** is a fully-featured e-commerce REST API designed to demonstrate production-grade backend engineering practices, not just CRUD. It covers authentication, catalog browsing, order processing with **race-condition-safe stock management**, **Stripe payments**, **async email delivery via Celery**, and **Redis-backed caching**, all documented with an interactive OpenAPI schema and backed by an automated **CI test pipeline**.

This project was built as a portfolio piece to demonstrate real-world Django/DRF backend development skills for a remote backend developer role.

---

## ✨ Features

### 🔐 Authentication & Accounts
- JWT authentication (access + refresh tokens) via `djangorestframework-simplejwt`
- Registration, login, logout with refresh-token blacklisting
- Authenticated profile retrieval and update
- Secure password change for logged-in users
- Forgot-password / reset-password flow via emailed tokenized links
- Per-endpoint request throttling (scoped rate limits)

### 🗂️ Categories
- Self-referencing hierarchical category tree (parent → children)
- Aggregated product counts per category
- Response caching with automatic invalidation via Django signals

### 📦 Products
- Full-text search across name, description, and category
- Filtering by category, price range, and stock availability
- Ordering (price, name, stock, newest) and pagination
- Admin-only create/update/delete, public read access
- Response caching with automatic invalidation via Django signals

### 🧾 Orders
- Customer order creation with **atomic, row-locked stock validation** (`select_for_update`) to prevent overselling under concurrent requests
- Automatic total price calculation from live product prices
- Customers can modify items only while an order is `PENDING`
- Admins can manage order status (`CONFIRMED`, `DELIVERED`, `CANCELED`) and view all orders
- Customers are scoped to their own orders; admins see everything
- Rich filtering (status, payment status, date range, price range) and ordering

### 💳 Payments
- Stripe **PaymentIntent** creation tied to a specific order
- Idempotent — re-requesting a payment intent for the same order returns the existing one
- Signed **Stripe webhook** handler that updates order/payment status on success or failure
- Guards against paying for already-paid or canceled orders

### ⚙️ Background Processing
- **Celery** for asynchronous, non-blocking task execution
- **Redis** (Upstash) as the Celery broker and result backend
- Async emails: welcome email, password reset, order confirmation, order status updates
- Automatic retry with backoff on transient email task failures

### 🚀 Performance & Reliability
- Redis-based response caching for catalog endpoints
- Signal-based cache invalidation on data changes
- Query optimization via `select_related` / `prefetch_related`
- Database-level row locking to prevent stock race conditions on concurrent orders
- Scoped API throttling to protect against abuse

### 🧪 Quality & Tooling
- Automated test suite with `pytest` + `pytest-django` + `factory_boy` (models, serializers, views, permissions, edge cases)
- Continuous Integration via **GitHub Actions** (runs the full test suite with a live Redis service container on every push)
- Request/response profiling in development via `django-silk`
- Interactive OpenAPI 3 schema with Swagger UI and ReDoc (`drf-spectacular`)
- `.http` request collection for manual endpoint testing in VS Code (REST Client)

---

## 🛠️ Tech Stack

| Layer                | Technology                                                   |
|-----------------------|---------------------------------------------------------------|
| **Language**          | Python 3.12                                                   |
| **Framework**         | Django 6.0, Django REST Framework                              |
| **Auth**              | JWT (`djangorestframework-simplejwt`)                          |
| **Database**          | PostgreSQL (hosted on Supabase)                                |
| **Cache / Broker**    | Redis (hosted on Upstash) via `django-redis`                   |
| **Async Tasks**       | Celery                                                          |
| **Payments**          | Stripe API + Webhooks                                          |
| **API Docs**          | drf-spectacular (OpenAPI 3, Swagger UI, ReDoc)                 |
| **Filtering**         | django-filter                                                  |
| **Testing**           | pytest, pytest-django, factory_boy, coverage                   |
| **CI/CD**             | GitHub Actions                                                 |
| **Static Files**      | WhiteNoise                                                      |
| **Profiling**         | django-silk                                                     |
| **Deployment**        | Render (API) · Supabase (DB) · Upstash (Redis)                 |

---

## 🏗️ Architecture

The project follows a modular, app-per-domain Django structure:

```
backendcommerce-api/
├── config/                 # Project settings, root URLs, WSGI/ASGI, Celery app
├── apps/
│   ├── users/               # Auth, JWT, profile, password reset (+ tasks, tests)
│   ├── categories/          # Category tree, caching, signals
│   ├── products/            # Catalog, filters, search, caching, signals
│   ├── orders/               # Order lifecycle, stock locking, filters, tasks, tests
│   └── payments/             # Stripe PaymentIntent + webhook handling, tests
├── api.http.example         # Sample REST Client request collection
├── build.sh                  # Render build script
├── docker-compose.yml        # Local Redis container for development
├── pytest.ini
├── requirements.txt
└── manage.py
```

Each app follows a consistent internal layout: `models.py`, `serializers.py`, `views.py`, `urls.py`, `filters.py` (where relevant), `tasks.py` (where relevant), `signals.py` (where relevant), and a `tests/` module (`test_models.py`, `test_serializers.py`, `test_views.py`).

---

## 📡 API Documentation

Full interactive documentation is available live:

- **Swagger UI:** https://backend-commerce-api.onrender.com/api/schema/swagger-ui/
- **ReDoc:** https://backend-commerce-api.onrender.com/api/schema/redoc/

### Endpoint Summary

| Resource      | Endpoint                                    | Description                              |
|---------------|----------------------------------------------|-------------------------------------------|
| Auth          | `POST /api/users/register/`                   | Register a new customer                    |
| Auth          | `POST /api/users/login/`                       | Obtain JWT access & refresh tokens         |
| Auth          | `POST /api/users/token/refresh/`               | Refresh an access token                    |
| Auth          | `POST /api/users/logout/`                      | Blacklist a refresh token                  |
| Auth          | `GET/PUT/PATCH /api/users/profile/`            | Retrieve or update the current user        |
| Auth          | `PUT /api/users/change-password/`               | Change password (authenticated)            |
| Auth          | `POST /api/users/forget-password/`             | Request a password reset email             |
| Auth          | `POST /api/users/reset-password/<uid>/<token>/`| Reset password via emailed link            |
| Categories    | `GET /api/categories/`                          | List categories with nested children       |
| Products      | `GET /api/products/`                            | List/search/filter/paginate products       |
| Products      | `POST /api/products/`                           | Create a product *(admin only)*            |
| Products      | `GET/PUT/PATCH/DELETE /api/products/<slug>/`   | Retrieve/update/delete a product           |
| Orders        | `GET/POST /api/orders/`                         | List own orders / create an order          |
| Orders        | `GET/PUT/PATCH/DELETE /api/orders/<order_id>/` | Manage a single order                      |
| Payments      | `POST /api/payments/create-payment-intent/`     | Create a Stripe PaymentIntent for an order |
| Payments      | `POST /api/payments/webhook/`                   | Stripe webhook receiver                    |

See `api.http.example` for ready-to-run sample requests covering every endpoint (VS Code REST Client extension).

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL database (e.g. a free [Supabase](https://supabase.com/) project)
- Redis instance (e.g. a free [Upstash](https://upstash.com/) database, or run locally via Docker)
- A [Stripe](https://stripe.com/) account (test mode keys)
- An SMTP-capable email account for sending transactional emails

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/backendcommerce-api.git
cd backendcommerce-api
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=postgres://user:password@host:port/dbname

REDIS_URL=redis://localhost:6379/0

EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@example.com

STRIPE_SECRET_KEY=sk_test_xxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxx

TIME_ZONE=UTC
TESTING=False
```

> 📌 **Environment variable reference**

| Variable                 | Required | Description                                              |
|---------------------------|:--------:|------------------------------------------------------------|
| `SECRET_KEY`               | ✅       | Django secret key                                           |
| `DEBUG`                    | ✅       | `True`/`False`                                              |
| `ALLOWED_HOSTS`             | ✅       | Comma-separated list of allowed hosts                       |
| `DATABASE_URL`              | ✅       | PostgreSQL connection string                                 |
| `REDIS_URL`                 | ✅       | Redis connection string (cache + Celery broker/backend)     |
| `EMAIL_HOST` / `EMAIL_PORT` / `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD` / `EMAIL_USE_TLS` | ✅ | SMTP configuration for transactional email |
| `DEFAULT_FROM_EMAIL`         | ✅       | Sender address for outgoing emails                          |
| `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY` | ✅ | Stripe API keys                                        |
| `STRIPE_WEBHOOK_SECRET`      | ⛔ optional | Required to verify incoming Stripe webhook signatures     |
| `TIME_ZONE`                  | ⛔ optional | Defaults to `UTC`                                          |
| `TESTING`                    | ⛔ optional | Set `True` to run Celery tasks synchronously in tests     |

### 4. Run database migrations

```bash
python manage.py migrate
```

### 5. (Optional) Seed sample data

```bash
python manage.py seed_users
python manage.py seed_categories
python manage.py seed_products
python manage.py seed_orders
```

### 6. Start Redis locally (if not using a hosted instance)

```bash
docker compose up -d
```

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Run the Celery worker (in a separate terminal)

```bash
celery -A config worker -l info
```

The API will be available at `http://127.0.0.1:8000/`, with interactive docs at `http://127.0.0.1:8000/api/schema/swagger-ui/`.

---

## 🧪 Running Tests

The project uses `pytest` with `factory_boy` for fixtures and `pytest-django` for Django integration.

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=apps
```

Tests are automatically run on every push via **GitHub Actions**, using a live Redis service container to match production caching/Celery behavior.

---

## 🌐 Deployment

| Service     | Provider  |
|--------------|-----------|
| API hosting  | [Render](https://render.com/) |
| Database     | [Supabase](https://supabase.com/) (PostgreSQL) |
| Cache/Broker | [Upstash](https://upstash.com/) (Redis) |

Render runs `build.sh` on deploy, which installs dependencies and collects static files (served via WhiteNoise). Production security settings (SSL redirect, HSTS, secure cookies) are automatically enabled when `DEBUG=False`.

**Live demo:** https://backend-commerce-api.onrender.com/api/schema/swagger-ui/

> ⚠️ The free-tier instance may spin down after inactivity — the first request can take up to ~30–60 seconds to respond.

---

## 🗺️ Roadmap

- [ ] Shopping cart persistence (pre-checkout)
- [ ] Product reviews and ratings
- [ ] Order refund flow via Stripe
- [ ] Rate-limit dashboards / observability
- [ ] Dockerized full local dev environment (API + DB + Redis + Celery)

---

## 👩‍💻 Author

**Athika** -- Self-taught Django/DRF backend developer focused on building clean, well-tested, production-style APIs

- 🌐 [Portfolio](https://athikadev.netlify.app/)
- 🔗 [LinkedIn](https://www.linkedin.com/in/athika-chowdhury-priya-a37318289/)
- 📫 [Email](mailto:athika.web@gmail.com)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
