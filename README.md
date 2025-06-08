# 📱 Social Media API

A scalable and modular REST API for a social media platform, built with Django and Django REST Framework. It supports users, posts, comments, likes, and background task processing with Celery.

---

## 🚀 Features

- 🔐 User registration, login, and JWT-based authentication
- 📝 Full CRUD for user-generated posts
- 💬 Commenting system on posts
- ❤️ Like functionality
- 🧾 Robust validations and custom permission classes
- ⏳ Background task execution via Celery
- 🔁 Periodic tasks using Celery Beat
- 📊 Task monitoring with Flower
- 🐘 PostgreSQL and Redis integration
- 🐳 Dockerized for easy development and deployment

---

## 🧱 Model Overview

| Model     | Description                                            |
|-----------|--------------------------------------------------------|
| User      | Extended user model with authentication support       |
| Post      | User posts with title, content, and timestamps        |
| Comment   | Linked to posts and authors                           |
| Like      | Tracks which users liked which posts                  |
| Task      | Background jobs triggered by actions or periodically  |

---

## ⚙️ Key Business Logic

- ✅ **Permissions**: Object-level access control (e.g., only post authors can edit/delete)
- ⏱ **Async Task Queue**: Celery workers handle time-consuming jobs like email sending
- 🔄 **Scheduled Jobs**: Periodic tasks configured with Celery Beat
- 📬 **Email Ready**: Easily integratable SMTP settings
- 🧠 **Custom Logic**: Includes signal-based logic, clean methods, and custom filters

---

## 🛠️ Installation

### 🐳 With Docker:

```bash
git clone https://github.com/yourusername/social-media-api.git
cd social-media-api
cp .env.sample .env
docker-compose up --build
```
git clone https://github.com/yourusername/social-media-api.git
cd social-media-api

# Create a virtual environment
```
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.sample .env
# Edit `.env` and fill in your secrets

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

🧪 Technologies Used
Python 3

Django

Django REST Framework

Celery + Redis

PostgreSQL

Docker & Docker Compose

Flower (task queue monitoring)