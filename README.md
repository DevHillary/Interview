# Interview CRM System

A modern, full-stack Customer Relationship Management (CRM) system built with Django REST Framework and Vue.js. This system provides comprehensive lead and contact management capabilities with role-based access control, automated reminders, and complete audit trails.

**Developed by:** Hillary Chege  
**Purpose:** Interview assessment project

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [User Roles & Permissions](#-user-roles--permissions)
- [Development Setup](#-development-setup)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Sample Data](#-sample-data)
- [License](#-license)

## ✨ Features

### Core Functionality
- **Lead Management**: Complete pipeline tracking from initial contact to conversion
- **Contact Management**: Comprehensive contact database with relationship tracking
- **Notes System**: Add and manage notes for leads and contacts
- **Reminder System**: Automated reminders powered by Celery task scheduler
- **Correspondence Tracking**: Log emails, calls, and meetings with detailed history
- **Audit Trail**: Complete change history for all leads and contacts (Manager access)

### User Experience
- **Dashboard**: Real-time statistics and activity overview
- **Advanced Filtering**: Powerful search and filter capabilities
- **Role-Based Access Control**: Manager and Agent roles with granular permissions
- **Responsive Design**: Modern, intuitive user interface

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Authentication**: JWT (JSON Web Tokens)

### Frontend
- **Framework**: Vue.js 3
- **State Management**: Vuex
- **Routing**: Vue Router
- **HTTP Client**: Axios

### DevOps
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Docker Compose for multi-container setup

## 📦 Prerequisites

Before you begin, ensure you have the following installed:
- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)

For local development without Docker:
- Python 3.9+ 
- Node.js 16+ and npm
- PostgreSQL 12+

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/DevHillary/Interview.git
   cd Interview
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - **Frontend**: http://localhost:8080
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/swagger/

4. **Login with demo accounts**
   - **Manager**: `manager` / `password123`
   - **Agent**: `agent` / `password123`

The application will automatically:
- Set up the database
- Run migrations
- Create sample data
- Start all required services

## 📁 Project Structure

```
Interview/
├── backend/                    # Django backend application
│   ├── config/                # Django project configuration
│   │   ├── settings.py        # Project settings
│   │   ├── urls.py            # Main URL configuration
│   │   ├── wsgi.py            # WSGI configuration
│   │   └── celery.py          # Celery configuration
│   ├── crm/                   # CRM application
│   │   ├── models.py          # Lead, Contact, Note models
│   │   ├── views.py           # API views
│   │   ├── serializers.py     # DRF serializers
│   │   ├── permissions.py     # Custom permissions
│   │   ├── tasks.py           # Celery tasks
│   │   └── urls.py            # CRM URL routes
│   ├── users/                 # User authentication app
│   │   ├── models.py          # User model
│   │   ├── views.py           # Auth views
│   │   └── serializers.py     # User serializers
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Backend Docker image
│   └── entrypoint.sh          # Container entrypoint script
│
├── frontend/                   # Vue.js frontend application
│   ├── src/
│   │   ├── views/             # Page components
│   │   │   ├── Dashboard.vue
│   │   │   ├── Leads.vue
│   │   │   ├── Contacts.vue
│   │   │   └── Reminders.vue
│   │   ├── store/             # Vuex store modules
│   │   │   ├── modules/
│   │   │   │   ├── auth.js
│   │   │   │   ├── leads.js
│   │   │   │   ├── contacts.js
│   │   │   │   └── reminders.js
│   │   │   └── index.js
│   │   ├── services/          # API service layer
│   │   │   └── api.js
│   │   ├── router/            # Vue Router configuration
│   │   │   └── index.js
│   │   └── App.vue            # Root component
│   ├── package.json           # Node.js dependencies
│   ├── Dockerfile             # Frontend Docker image
│   └── vue.config.js          # Vue CLI configuration
│
└── docker-compose.yml         # Docker Compose configuration
```

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration

### CRM Endpoints
- `GET/POST /api/leads/` - List and create leads
- `GET/PUT/DELETE /api/leads/{id}/` - Retrieve, update, or delete a lead
- `GET/POST /api/contacts/` - List and create contacts
- `GET/PUT/DELETE /api/contacts/{id}/` - Retrieve, update, or delete a contact
- `GET/POST /api/notes/` - List and create notes
- `GET/PUT/DELETE /api/notes/{id}/` - Retrieve, update, or delete a note
- `GET/POST /api/reminders/` - List and create reminders
- `GET/PUT/DELETE /api/reminders/{id}/` - Retrieve, update, or delete a reminder
- `GET/POST /api/correspondences/` - List and create correspondence records
- `GET /api/auditlogs/` - View audit trail (Manager only)
- `GET /api/dashboard-stats/` - Get dashboard statistics

### Interactive API Documentation
Visit http://localhost:8000/swagger/ for interactive API documentation with Swagger UI.

## 👥 User Roles & Permissions

### Manager Role
- ✅ Full CRUD access to all resources (Leads, Contacts, Notes, Reminders, Correspondences)
- ✅ Can delete leads and contacts
- ✅ Access to audit logs and system history
- ✅ View dashboard statistics

### Agent Role
- ✅ Create and update leads and contacts
- ✅ Create and manage notes and reminders
- ✅ View assigned leads and contacts
- ❌ Cannot delete leads or contacts
- ❌ Cannot access audit logs

## 💻 Development Setup

### Backend Setup (Local Development)

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the `backend` directory (see [Environment Variables](#-environment-variables))

6. **Run migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (Local Development)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run serve
   ```

4. **Build for production**
   ```bash
   npm run build
   ```

### Running Celery Worker (Local Development)

In a separate terminal:
```bash
cd backend
celery -A config worker -l info
```

For Celery Beat (scheduler):
```bash
cd backend
celery -A config beat -l info
```

## 🔐 Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DB_NAME=crm_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0

# CORS Settings (if needed)
CORS_ALLOWED_ORIGINS=http://localhost:8080
```

> **Note**: For production, set `DEBUG=False` and use a strong `SECRET_KEY`. Never commit `.env` files to version control.

## 🚀 Deployment

This application can be deployed to Render.com for free. See the [DEPLOYMENT.md](DEPLOYMENT.md) file for detailed deployment instructions.

### Quick Deploy to Render.com

1. **Push your code to GitHub** (already done if you're reading this)

2. **Connect to Render**
   - Sign up at https://render.com
   - Go to Dashboard → "New +" → "Blueprint"
   - Connect your GitHub repository: `DevHillary/Interview`
   - Render will automatically detect `render.yaml` and configure all services

3. **Configure Environment Variables**
   - After deployment, update the backend service environment variables:
     - `ALLOWED_HOSTS`: Your backend URL (e.g., `crm-backend.onrender.com`)
     - `CORS_ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://crm-frontend.onrender.com`)

4. **Initialize Database**
   - Go to backend service → "Shell"
   - Run:
     ```bash
     python manage.py migrate
     python manage.py createsuperuser
     python create_sample_data.py
     ```

5. **Access Your Application**
   - Frontend: `https://crm-frontend.onrender.com`
   - Backend API: `https://crm-backend.onrender.com`
   - API Docs: `https://crm-backend.onrender.com/swagger/`

For detailed deployment instructions, troubleshooting, and alternative hosting options, see [DEPLOYMENT.md](DEPLOYMENT.md).

## 📊 Sample Data

The system automatically creates sample data on first startup, including:
- Sample leads with various statuses
- Contact information
- Notes and reminders
- Correspondence records

All sample data uses Kenyan-based information for realistic testing scenarios.

## 📄 License

This project is developed by **Hillary Chege** for interview-related purposes.

---

**Repository**: [https://github.com/DevHillary/Interview](https://github.com/DevHillary/Interview)
