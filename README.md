# CRM System

A full-stack Customer Relationship Management (CRM) system built with Django REST Framework and Vue.js.

## Features

- **Lead Management**: Track and manage sales leads through the pipeline
- **Contact Management**: Maintain contact information linked to leads
- **Notes**: Add notes to leads for better tracking
- **Reminders**: Schedule and manage reminders with Celery
- **Correspondence Tracking**: Log emails, calls, and meetings with contacts
- **Role-Based Access**: Manager and Agent roles with different permissions
- **Audit Trail**: Complete history of changes to leads and contacts
- **Dashboard**: Real-time statistics and activity overview
- **Filtering & Search**: Advanced filtering and search capabilities

## Technology Stack

**Backend:**
- Django 4.2
- Django REST Framework
- PostgreSQL
- Celery + Redis
- JWT Authentication

**Frontend:**
- Vue.js 3
- Vuex (State Management)
- Vue Router
- Axios

**DevOps:**
- Docker & Docker Compose

## Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd interview
```

2. **Start with Docker Compose**
```bash
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/swagger/

4. **Login with demo accounts**
- Manager: `manager` / `password123`
- Agent: `agent` / `password123`

## Project Structure

```
├── backend/              # Django backend
│   ├── config/          # Project settings
│   ├── crm/             # CRM app (leads, contacts, etc.)
│   └── users/           # User authentication
├── frontend/            # Vue.js frontend
│   └── src/
│       ├── components/  # Vue components
│       ├── views/       # Page views
│       ├── store/       # Vuex store
│       └── services/    # API services
└── docker-compose.yml   # Docker orchestration
```

## API Endpoints

- `/api/leads/` - Lead management
- `/api/contacts/` - Contact management
- `/api/notes/` - Notes for leads
- `/api/reminders/` - Reminder management
- `/api/correspondences/` - Correspondence tracking
- `/api/auditlogs/` - Audit trail (Manager only)
- `/api/dashboard-stats/` - Dashboard statistics
- `/api/auth/login/` - User authentication
- `/api/auth/register/` - User registration

## Permissions

**Manager Role:**
- Full CRUD access to all resources
- Can delete leads and contacts
- Access to audit logs

**Agent Role:**
- Can create and update leads/contacts
- Cannot delete leads or contacts
- Cannot access audit logs

## Development Setup

### Backend Setup (without Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup (without Docker)

```bash
cd frontend
npm install
npm run serve
```

### Environment Variables

Create a `.env` file in the backend directory:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=crm_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
```

## Sample Data

The system automatically creates sample data with Kenyan-based information on first startup.

## License

This project is for assessment purposes.
