# Setup Guide

This guide will help you set up and run the CRM system on your local machine.

## Prerequisites

- Docker Desktop installed and running
- Git

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd interview
```

### 2. Start the Application

The easiest way to run the application is using Docker Compose:

```bash
docker-compose up --build
```

This command will:
- Build the Docker images for backend and frontend
- Start PostgreSQL database
- Start Redis for Celery
- Run Django migrations
- Create sample data automatically
- Start Celery workers for background tasks
- Start the development servers

### 3. Access the Application

Once all containers are running, you can access:

- **Frontend Application**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/swagger/
- **API Documentation (ReDoc)**: http://localhost:8000/redoc/

### 4. Login

Use one of these demo accounts:

**Manager Account:**
- Username: `manager`
- Password: `password123`
- Permissions: Full access to all features

**Agent Account:**
- Username: `agent`
- Password: `password123`
- Permissions: Can create and update, but cannot delete

## Stopping the Application

To stop all containers:

```bash
docker-compose down
```

To stop and remove all data (including database):

```bash
docker-compose down -v
```

## Troubleshooting

### Containers not starting

Make sure Docker Desktop is running and ports 8000, 8080, 5432, and 6379 are not in use.

### Database connection errors

Wait a few seconds after starting the containers. The backend waits for the database to be ready before starting.

### Frontend not loading

Check frontend logs:
```bash
docker-compose logs frontend
```

### Backend errors

Check backend logs:
```bash
docker-compose logs backend
```

## Development

### Running without Docker

If you prefer to run the application without Docker:

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your settings
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run serve
```

You'll also need to run PostgreSQL, Redis, and Celery separately.

## Features

- Lead Management (CRUD operations)
- Contact Management linked to leads
- Notes for leads
- Reminders with Celery scheduling
- Correspondence tracking (emails, calls, meetings)
- Dashboard with statistics
- Role-based permissions (Manager/Agent)
- Audit trail for all changes
- Search and filtering
- Export to CSV

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework, PostgreSQL, Celery, Redis
- **Frontend**: Vue.js 3, Vuex, Vue Router, Axios
- **DevOps**: Docker, Docker Compose


