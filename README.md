# MetroVPS-Task


````markdown
# 🚀 MetroVPS-Task

A Django-based project for SMS subscription management, with full Docker support, Celery background tasks, and RESTful API.

---

## 📁 Project Structure

- `web`: Django application
- `celery`: Celery worker (background task processor)
- `celery-beat`: Scheduler for periodic tasks
- `redis`: Message broker for Celery

---

## 🛠️ Local Setup (with Docker)

### 1. Clone the repository

```bash
git clone https://github.com/faysalhassantorjo/MetroVPS-Task.git
cd MetroVPS-Task
````

### 2. Build and start the app

```bash
docker compose build
docker compose up
```

### 3. Access the app

* Go to: [http://localhost:8000](http://localhost:8000)

---

## 🐳 Docker Usage

* **Start the project**

  ```bash
  docker compose up
  ```

* **Stop the project**

  ```bash
  docker compose down
  ```

* **Rebuild after changes**

  ```bash
  docker compose build
  ```

> All services (Django, Redis, Celery, Celery Beat) are automatically managed via Docker Compose.

---

## ⏱️ Celery Integration

No need to run Celery manually.

When you run `docker compose up`, the following services start automatically:

* `web`: Django app
* `celery`: Celery worker
* `celery-beat`: Periodic task scheduler
* `redis`: Celery broker

✅ Background and periodic tasks will run out of the box.

---

## 📮 API Endpoints

All API routes are under the `/api/` prefix.

### 🔐 Auth

* `POST /api/register/`
  Register a new user

* `POST /api/login/`
  Login and receive auth token

---

### 💱 Exchange Rates

* `GET /api/exchange-rate/?base=USD&target=BDT`
  Get exchange rate between currencies

---

### 📦 Subscription System

* `POST /api/subscribe/`
  Subscribe to a plan
  **Request Body:**

  ```json
  {
    "plan_id": 1
  }
  ```

* `GET /api/subscriptions/`
  View all your subscriptions

* `POST /api/cancel-subscription/`
  Cancel a subscription
  *(expects current subscription to be active)*

---

## ✅ Submission Checklist

* [x] Full source code pushed to [GitHub Repo](https://github.com/faysalhassantorjo/MetroVPS-Task)
* [x] README with setup steps
* [x] Docker usage instructions
* [x] Celery setup info
* [x] All API endpoints documented

---



* Default port: `8000`


---

