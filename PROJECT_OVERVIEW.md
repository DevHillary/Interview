# CRM System - Project Overview

## Introduction

This is a comprehensive Customer Relationship Management (CRM) system designed to help businesses manage leads, contacts, and customer interactions efficiently. The system features a modern tech stack with Django REST Framework backend and Vue.js frontend, all containerized with Docker for easy deployment.

## Technologies Used

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - RESTful API development
- **PostgreSQL 15** - Relational database
- **Celery** - Asynchronous task queue
- **Redis** - Message broker and caching
- **JWT Authentication** - Secure token-based authentication

### Frontend
- **Vue.js 3** - Progressive JavaScript framework
- **Vuex** - State management
- **Vue Router** - Client-side routing
- **Axios** - HTTP client

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server (production)

## Core Features Implemented

### 1. Lead Management
- Create, read, update, and delete leads
- Track lead status (New, Contacted, Qualified, Lost, Converted)
- Set priority levels (Low, Medium, High)
- Estimate deal value
- Filter and search leads
- Export leads to CSV

### 2. Contact Management
- Multiple contacts per lead
- Mark primary contact
- Track contact position and details
- Link correspondence to contacts

### 3. Notes
- Add notes to leads
- Track note author and timestamp
- View complete note history

### 4. Reminders
- Schedule reminders for leads
- Automated email notifications (via Celery)
- Track reminder status (Pending, Sent, Cancelled)
- View upcoming and overdue reminders

### 5. Correspondence Tracking
- Log emails, phone calls, and meetings
- Associate correspondence with contacts
- View complete communication history
- Date and description tracking

### 6. Authentication & Authorization
- JWT-based secure authentication
- Two user roles:
  - **Manager**: Full access to all features
  - **Agent**: Cannot delete leads or contacts
- Role-based UI elements
- Secure password hashing

### 7. Audit Trail
- Automatic logging of all changes
- Track who made changes and when
- JSON storage of before/after values
- Manager-only access to audit logs

### 8. Dashboard
- Real-time statistics overview
- Lead distribution by status and priority
- Total estimated value tracking
- Recent activity feed
- Upcoming reminders
- Contact count

### 9. Advanced Features
- Filtering by multiple fields
- Full-text search
- Sorting and ordering
- Pagination
- API documentation (Swagger/ReDoc)
- CORS configuration
- Export to CSV

## Project Structure

```
interview/
├── backend/
│   ├── config/          # Django settings
│   ├── crm/             # Main CRM app
│   │   ├── models.py    # Database models
│   │   ├── views.py     # API views
│   │   ├── serializers.py
│   │   ├── permissions.py
│   │   ├── tasks.py     # Celery tasks
│   │   └── utils.py
│   ├── users/           # Authentication
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/  # Reusable components
│   │   ├── views/       # Page components
│   │   ├── store/       # Vuex state management
│   │   ├── services/    # API services
│   │   └── router/      # Route configuration
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml   # Container orchestration
└── README.md
```

## Getting Started

### Prerequisites
- Docker Desktop installed and running
- Git

### Quick Start

1. Clone the repository
2. Run `docker-compose up --build`
3. Access the application at http://localhost:8080
4. Login with demo credentials:
   - Manager: `manager` / `password123`
   - Agent: `agent` / `password123`

### API Documentation
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Sample Data

The system includes pre-populated sample data with Kenyan context:
- 2 users (manager and agent roles)
- 10 sample leads with realistic Kenyan names and companies
- Contacts for each lead
- Sample notes, reminders, and correspondence
- Kenyan phone number formats and company names

## API Highlights

All API endpoints follow REST conventions and include:
- Proper HTTP status codes
- JSON request/response format
- Error handling with descriptive messages
- Query parameter support for filtering
- Authentication via JWT tokens

Key endpoints:
- `/api/leads/` - Lead management
- `/api/contacts/` - Contact management
- `/api/notes/` - Note management
- `/api/reminders/` - Reminder scheduling
- `/api/correspondences/` - Communication tracking
- `/api/dashboard-stats/` - Dashboard data
- `/api/auth/login/` - User authentication

## Security Features

- Password hashing using Django's PBKDF2
- JWT tokens with 1-hour expiration
- CORS configuration for frontend-backend communication
- Environment variable management for sensitive data
- Permission classes on all API endpoints
- SQL injection protection via Django ORM
- XSS protection via Vue.js sanitization

## Code Quality

- Comprehensive comments throughout the codebase
- Clear separation of concerns
- Modular architecture
- Error handling at all levels
- Consistent naming conventions
- RESTful API design
- Vue.js best practices

## Testing

The application has been manually tested for:
- User authentication flow
- All CRUD operations
- Permission enforcement
- Dashboard statistics accuracy
- CSV export functionality
- Filtering and search
- Background task execution

## Performance Optimizations

- Database indexing on frequently queried fields
- Query optimization with select_related and prefetch_related
- Pagination to limit result sets
- Redis for Celery message queue
- Static file serving optimization

## Future Enhancements

Potential areas for expansion:
- Real email integration (SendGrid, AWS SES)
- File attachments for correspondence
- Advanced analytics and reporting
- Calendar integration
- Mobile application
- WebSocket support for real-time updates
- Unit and integration test suite
- CI/CD pipeline

## Conclusion

This CRM system demonstrates a full-stack application with modern architecture, clean code, and production-ready features. It's designed to be scalable, maintainable, and user-friendly while showcasing best practices in both frontend and backend development.


