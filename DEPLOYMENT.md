# Deployment Guide - Render.com

This guide will help you deploy the CRM system to Render.com for free.

## Prerequisites

1. A GitHub account with this repository
2. A Render.com account (sign up at https://render.com)

## Step-by-Step Deployment

### Option 1: Deployment with render.yaml (Recommended)

**Note:** Databases and Redis need to be created manually first, then connected to the web services.

1. **Create PostgreSQL Database First**
   - Go to Render Dashboard → "New +" → "PostgreSQL"
   - Name: `crm-database`
   - Plan: Free
   - Click "Create Database"
   - **Save the connection details** (Internal Database URL, Host, Port, Database, User, Password)

2. **Create Redis Instance (Optional)**
   - **Note:** Render.com doesn't offer Redis on the free tier
   - **Option A:** Use a free Redis service like [Upstash](https://upstash.com/) (free tier available)
     - Sign up at https://upstash.com
     - Create a new Redis database
     - Copy the REST URL or Redis URL
   - **Option B:** Skip Redis - the app will work without it, but reminder notifications won't be sent automatically
   - If using Upstash, save the connection URL

3. **Deploy Backend with Blueprint**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the repository: `DevHillary/Interview`
   - Render will automatically detect `render.yaml` and create the backend service
   - Click "Apply"
   
   **Note:** The frontend must be deployed separately as a Static Site (see Step 4)

4. **Configure Backend Environment Variables**
   - Go to the `crm-backend` service → "Environment"
   - Add/Update these variables:
     ```
     DB_NAME=<from-postgres-database-name>
     DB_USER=<from-postgres-user>
     DB_PASSWORD=<from-postgres-password>
     DB_HOST=<from-postgres-host>
     DB_PORT=5432
     # Celery/Redis (Optional - leave empty to disable)
     CELERY_BROKER_URL=<upstash-redis-url-or-leave-empty>
     CELERY_RESULT_BACKEND=<upstash-redis-url-or-leave-empty>
     ALLOWED_HOSTS=crm-backend.onrender.com
     CORS_ALLOWED_ORIGINS=https://crm-frontend.onrender.com
     ```
   - Use the **Internal Database URL** and **Internal Redis URL** (not external URLs)

5. **Configure Frontend Environment Variable**
   - Go to the `crm-frontend` service → "Environment"
   - Set: `VUE_APP_API_URL=https://crm-backend.onrender.com` (use your actual backend URL)

6. **Wait for Deployment**
   - Render will build and deploy all services
   - This may take 5-10 minutes for the first deployment

7. **Initialize Database**
   - Once the backend is deployed, go to backend service → "Shell"
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

#### 2. Set Up Redis (Optional)

**Note:** Render.com doesn't offer Redis on the free tier. You have two options:

**Option A: Use Upstash (Free Redis Service)**
1. Go to https://upstash.com and sign up
2. Create a new Redis database
3. Copy the REST URL or Redis URL
4. Use this URL for `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`

**Option B: Skip Redis**
- Leave `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` empty
- The app will work, but reminder notifications won't be sent automatically

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
   # Celery/Redis (Optional - use Upstash or leave empty)
   CELERY_BROKER_URL=<upstash-redis-url-or-empty>
   CELERY_RESULT_BACKEND=<upstash-redis-url-or-empty>
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

**Note:** Static sites cannot be defined in render.yaml. Deploy manually:

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

### Celery Workers (Optional)

**Note:** Celery is optional. If you don't set up Redis, reminder notifications won't work automatically, but the rest of the app will function normally.

If you want to enable reminder notifications:
1. Set up a free Redis instance on Upstash (https://upstash.com)
2. Add the Redis URL to backend environment variables
3. (Optional) Deploy Celery workers separately:
   - Create a new "Background Worker" service
   - Use the same environment variables as the backend
   - Start command: `cd backend && celery -A config worker --loglevel=info`

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

