# 🚀 Quick Deployment Guide to Render.com

Follow these simple steps to deploy your CRM system to Render.com (takes about 10 minutes).

## Step 1: Sign Up for Render.com

1. Go to [https://render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up with your **GitHub account** (recommended - makes connecting easier)
4. Verify your email if prompted

## Step 2: Create a New Blueprint

1. Once logged in, click the **"New +"** button in the top right
2. Select **"Blueprint"** from the dropdown menu
3. You'll see a page asking to connect a repository

## Step 3: Connect Your GitHub Repository

1. Click **"Connect account"** or **"Configure account"** if you haven't connected GitHub yet
2. Authorize Render to access your GitHub repositories
3. Search for and select: **`DevHillary/Interview`**
4. Click **"Connect"**

## Step 4: Let Render Auto-Configure

1. Render will automatically detect the `render.yaml` file in your repository
2. You'll see a preview of all services that will be created:
   - ✅ PostgreSQL Database (crm-database)
   - ✅ Redis (crm-redis)
   - ✅ Backend Web Service (crm-backend)
   - ✅ Celery Worker (crm-celery-worker)
   - ✅ Celery Beat (crm-celery-beat)
   - ✅ Frontend Web Service (crm-frontend)
3. Click **"Apply"** to start the deployment

## Step 5: Wait for Initial Deployment

1. Render will start building all services (this takes 5-10 minutes)
2. You can watch the build logs by clicking on each service
3. The database and Redis will be ready first
4. Then the backend will build and deploy
5. Finally, the frontend will build and deploy

## Step 6: Configure Environment Variables

After all services are deployed (green status), you need to set a few environment variables:

### For the Frontend Service (crm-frontend):

1. Click on the **"crm-frontend"** service in your Render dashboard
2. Go to the **"Environment"** tab
3. Find the **"VUE_APP_API_URL"** variable
4. Click **"Add Value"** or edit it
5. Set the value to your backend URL (you'll find it on the crm-backend service page)
   - Example: `https://crm-backend.onrender.com`
6. Click **"Save Changes"**
7. The service will automatically rebuild with the new value

### For the Backend Service (crm-backend):

1. Click on the **"crm-backend"** service
2. Go to the **"Environment"** tab
3. Find **"ALLOWED_HOSTS"** and set it to your backend URL (without https://)
   - Example: `crm-backend.onrender.com`
4. Find **"CORS_ALLOWED_ORIGINS"** and set it to your frontend URL
   - Example: `https://crm-frontend.onrender.com`
5. Click **"Save Changes"**
6. The service will automatically redeploy

## Step 7: Access Your Application

Once all services show a green status:

- **Frontend**: `https://crm-frontend.onrender.com`
- **Backend API**: `https://crm-backend.onrender.com`
- **API Documentation**: `https://crm-backend.onrender.com/swagger/`

## Step 8: Test Your Deployment

1. Visit your frontend URL
2. Try logging in with the demo accounts:
   - **Manager**: `manager` / `password123`
   - **Agent**: `agent` / `password123`

## 🎉 You're Done!

Your CRM system is now live on the internet!

## 📝 Important Notes

- **Free Tier**: Render's free tier services spin down after 15 minutes of inactivity. The first request after spin-down may take 30-60 seconds.
- **Database**: Your PostgreSQL database is automatically configured and persistent.
- **HTTPS**: All services automatically get HTTPS certificates.
- **Updates**: Any push to your GitHub repository will automatically trigger a new deployment.

## 🆘 Troubleshooting

### Services won't start?
- Check the build logs for errors
- Make sure all environment variables are set correctly

### Frontend can't connect to backend?
- Verify `VUE_APP_API_URL` is set correctly in the frontend service
- Check that `CORS_ALLOWED_ORIGINS` includes your frontend URL in the backend service

### Database connection errors?
- Wait a few minutes for the database to fully initialize
- Check that database environment variables are correctly linked (they should be automatic)

### Need help?
- Check Render's documentation: https://render.com/docs
- Check the build logs in the Render dashboard for specific error messages

