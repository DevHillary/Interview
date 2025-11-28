# Deployment Guide - Render.com

This guide will help you deploy the CRM system to Render.com for free.

## Prerequisites

1. A GitHub account with this repository
2. A Render.com account (sign up at https://render.com)

## Step-by-Step Deployment

### Option 1: Automatic Deployment with render.yaml (Recommended)

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push
   ```

2. **Connect to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository: `DevHillary/Interview`
   - Render will automatically detect `render.yaml`
   - Click "Apply"

3. **Configure Environment Variables**
   - After the blueprint is created, go to each service
   - For the backend service, add these environment variables:
     - `ALLOWED_HOSTS`: Your backend URL (e.g., `crm-backend.onrender.com`)
     - `CORS_ALLOWED_ORIGINS`: Your frontend URL (e.g., `https://crm-frontend.onrender.com`)
   - The database and Redis connections will be automatically configured

4. **Wait for Deployment**
   - Render will build and deploy all services
   - This may take 5-10 minutes for the first deployment

5. **Initialize Database**
   - Once the backend is deployed, you need to run migrations and create sample data
   - Go to the backend service → "Shell"
   - Run:
     ```bash
     python manage.py migrate
     python manage.py createsuperuser
     python create_sample_data.py
     ```

### Option 2: Manual Deployment

#### 1. Deploy PostgreSQL Database

1. Go to Render Dashboard → "New +" → "PostgreSQL"
2. Name: `crm-database`
3. Plan: Free
4. Click "Create Database"
5. Note down the connection details (you'll need them later)

#### 2. Deploy Redis

1. Go to Render Dashboard → "New +" → "Redis"
2. Name: `crm-redis`
3. Plan: Free
4. Click "Create Redis"
5. Note down the connection string

#### 3. Deploy Django Backend

1. Go to Render Dashboard → "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `crm-backend`
   - **Environment**: Python 3
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt && cd backend && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```bash
     cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
     ```
   - **Plan**: Free

4. **Environment Variables**:
   ```
   PYTHON_VERSION=3.11.0
   SECRET_KEY=<generate-a-secret-key>
   DEBUG=False
   DB_NAME=<from-postgres-service>
   DB_USER=<from-postgres-service>
   DB_PASSWORD=<from-postgres-service>
   DB_HOST=<from-postgres-service>
   DB_PORT=5432
   CELERY_BROKER_URL=<from-redis-service>
   CELERY_RESULT_BACKEND=<from-redis-service>
   ALLOWED_HOSTS=crm-backend.onrender.com
   CORS_ALLOWED_ORIGINS=https://crm-frontend.onrender.com
   ```

5. Click "Create Web Service"

6. **After deployment, run migrations**:
   - Go to the service → "Shell"
   - Run:
     ```bash
     python manage.py migrate
     python manage.py createsuperuser
     python create_sample_data.py
     ```

#### 4. Deploy Vue.js Frontend

1. Go to Render Dashboard → "New +" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `crm-frontend`
   - **Build Command**: 
     ```bash
     cd frontend && npm install && npm run build
     ```
   - **Publish Directory**: `frontend/dist`
   - **Environment Variables**:
     ```
     NODE_VERSION=18.18.0
     VUE_APP_API_URL=https://crm-backend.onrender.com
     ```
     > **Important**: Replace `crm-backend.onrender.com` with your actual backend URL

4. Click "Create Static Site"

## Post-Deployment Steps

### 1. Update CORS Settings

After deployment, update the backend environment variable:
- `CORS_ALLOWED_ORIGINS`: Add your frontend URL (e.g., `https://crm-frontend.onrender.com`)

### 2. Create Admin User

1. Go to backend service → "Shell"
2. Run:
   ```bash
   python manage.py createsuperuser
   ```

### 3. Create Sample Data

1. In the backend shell:
   ```bash
   python create_sample_data.py
   ```

### 4. Access Your Application

- **Frontend**: `https://crm-frontend.onrender.com`
- **Backend API**: `https://crm-backend.onrender.com`
- **API Docs**: `https://crm-backend.onrender.com/swagger/`

## Demo Accounts

After running `create_sample_data.py`, you can login with:
- **Manager**: `manager` / `password123`
- **Agent**: `agent` / `password123`

## Important Notes

### Free Tier Limitations

- Services may spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Database has a 90-day retention limit on free tier
- Limited to 750 hours/month total across all services

### Celery Workers

For production use, you may want to deploy Celery workers separately:
1. Create a new "Background Worker" service
2. Use the same environment variables as the backend
3. Start command: `cd backend && celery -A config worker --loglevel=info`

### Custom Domain (Optional)

1. Go to your service settings
2. Click "Add Custom Domain"
3. Follow the DNS configuration instructions

## Troubleshooting

### Backend won't start
- Check environment variables are set correctly
- Verify database connection string
- Check logs in Render dashboard

### Frontend can't connect to backend
- Verify `VUE_APP_API_URL` is set correctly
- Check CORS settings in backend
- Ensure backend URL includes `https://`

### Database connection errors
- Verify all database environment variables
- Check that the database service is running
- Ensure IP whitelist allows connections (Render handles this automatically)

### Static files not loading
- Ensure `collectstatic` ran during build
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Verify WhiteNoise is installed and configured

## Support

For Render-specific issues, check:
- Render Documentation: https://render.com/docs
- Render Status: https://status.render.com

For application issues, check the service logs in the Render dashboard.

