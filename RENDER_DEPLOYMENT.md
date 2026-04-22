# Render Deployment Guide for Flask Applications

## Overview

Render is a cloud platform for deploying web applications. This guide covers deploying a Flask ML project with trained models.

---

## Prerequisites

✅ GitHub account with repository
✅ Render account ([render.com](https://render.com))
✅ Flask app with trained models (model.pkl, vectorizer.pkl)
✅ requirements.txt with all dependencies
✅ Procfile for process management

---

## Step 1: Prepare Your Application

### 1.1 Create Procfile
```bash
# In project root directory
echo "web: gunicorn app:app" > Procfile
```

**Content:**
```
web: gunicorn app:app
```

### 1.2 Create runtime.txt
```bash
echo "python-3.11.4" > runtime.txt
```

**Supported Python versions:**
- python-3.11.4
- python-3.10.13
- python-3.9.18
- etc.

### 1.3 Update requirements.txt
```
Flask==3.0.0
gunicorn==22.0.0
scikit-learn==1.8.0
pandas==3.0.2
numpy==2.4.4
scipy==1.17.1
```

### 1.4 Modify app.py for Production
```python
import os
from flask import Flask

app = Flask(__name__)

# Use PORT environment variable (set by Render)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(
        debug=False,           # Disable debug in production
        host='0.0.0.0',       # Listen on all interfaces
        port=port             # Use Render's PORT
    )
```

### 1.5 Create .gitignore
```
.venv/
venv/
__pycache__/
*.pyc
*.pkl
.env
.env.local
.DS_Store
```

---

## Step 2: Push to GitHub

```bash
# Initialize Git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Deploy to Render"

# Add remote (replace with your repo)
git remote add origin https://github.com/yourusername/fake-news-detection.git

# Push to GitHub
git push -u origin main
```

**Verify on GitHub:**
- Procfile exists
- runtime.txt exists
- requirements.txt exists
- All source files committed
- Model files (*.pkl) committed

---

## Step 3: Connect to Render

### 3.1 Sign in to Render
1. Go to [render.com](https://render.com)
2. Click "Sign up" or "Sign in"
3. Choose GitHub authentication
4. Authorize Render to access your GitHub account

### 3.2 Create New Web Service
1. Click **"New +"** button
2. Select **"Web Service"**
3. Choose **"Connect a repository"**

### 3.3 Select Repository
1. Search for your repository
2. Click **"Connect"**
3. Choose branch: **main** (or your default branch)

### 3.4 Configure Service

| Setting | Value |
|---------|-------|
| **Name** | fake-news-detection |
| **Runtime** | Python 3 |
| **Root Directory** | (leave blank) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |

### 3.5 Environment Variables (Optional)
Click **"Advanced"** → **"Add Environment Variable"**

```
FLASK_ENV=production
FLASK_DEBUG=0
```

### 3.6 Deploy
1. Click **"Create Web Service"**
2. Wait for build to complete
3. Get your Render URL (e.g., https://fake-news-detection.onrender.com)

---

## Build & Start Commands Explained

### Build Command
```bash
pip install -r requirements.txt
```

**What it does:**
1. Installs all Python packages
2. Runs in build phase
3. Creates dependency cache

**Why needed:**
- Ensures all packages available at runtime
- Must match your local environment

### Start Command
```bash
gunicorn app:app
```

**What it does:**
1. Starts Gunicorn WSGI server
2. Loads Flask app from app.py
3. Serves on PORT environment variable

**Common variants:**
```bash
# With workers (for production)
gunicorn app:app --workers 4

# Custom bind
gunicorn app:app --bind 0.0.0.0:5000

# With timeout
gunicorn app:app --timeout 120

# Full production setup
gunicorn app:app --workers 4 --worker-class sync --timeout 60
```

---

## Render Dashboard Navigation

### View Logs
1. Go to your service
2. Click **"Logs"** tab
3. See real-time output

### View Metrics
1. Click **"Metrics"** tab
2. See CPU, memory, requests

### Restart Service
1. Click **"Manual Deploy"** dropdown
2. Select **"Clear build cache & deploy"**

### Update Environment Variables
1. Click **"Environment"** tab
2. Edit variables
3. Click **"Save"**
4. Service auto-restarts

---

## Common Errors & Fixes

### ❌ Error 1: "Build failed: command not found: gunicorn"

**Cause:** gunicorn not in requirements.txt

**Fix:**
```bash
# Add to requirements.txt
echo "gunicorn==22.0.0" >> requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Add gunicorn"
git push origin main

# Redeploy on Render
Click "Manual Deploy" > "Clear build cache & deploy"
```

---

### ❌ Error 2: "ModuleNotFoundError: No module named 'sklearn'"

**Cause:** scikit-learn not installed

**Fix:**
```bash
# Add to requirements.txt
echo "scikit-learn==1.8.0" >> requirements.txt
git add requirements.txt
git commit -m "Add scikit-learn"
git push origin main
```

---

### ❌ Error 3: "FileNotFoundError: model.pkl not found"

**Cause:** Model files not committed to Git

**Fix:**
```bash
# Check Git status
git status

# Add model files
git add *.pkl
git commit -m "Add trained models"
git push origin main

# Redeploy
```

**Note:** Use .gitignore carefully - don't exclude .pkl files!

---

### ❌ Error 4: "Port already in use" or "Address already in use"

**Cause:** Port binding conflict

**Fix:** Render automatically assigns PORT via environment variable

**In app.py:**
```python
import os
port = int(os.environ.get('PORT', 5000))
app.run(port=port)
```

---

### ❌ Error 5: "Application failed to start - No module named 'app'"

**Cause:** app.py not in root directory or wrong start command

**Fix:**
1. Verify app.py in repository root
2. Check Start Command: `gunicorn app:app`
3. Check file is committed: `git ls-files | grep app.py`

---

### ❌ Error 6: "Build timed out"

**Cause:** Large dependencies or slow network

**Fix:**
```bash
# Clear build cache and redeploy
# On Render Dashboard: Manual Deploy > Clear build cache & deploy

# Or optimize requirements.txt - remove unnecessary packages
```

---

### ❌ Error 7: "503 Service Unavailable"

**Cause:** 
- App crashed
- Insufficient resources
- Memory limit exceeded

**Fix:**
```bash
# Check logs for errors
# On Render: Logs tab

# Common causes:
# 1. Model file too large
# 2. Insufficient memory
# 3. Python version mismatch

# Solution:
1. Check logs
2. Fix code/requirements
3. Push to GitHub
4. Render auto-redeploys
```

---

### ❌ Error 8: "Deployment rejected: branch is not allowed to deploy"

**Cause:** Branch protection rules or wrong branch selected

**Fix:**
1. On Render service settings
2. Change branch to main (or your default)
3. Save
4. Manually deploy

---

### ❌ Error 9: "Python version 3.11.4 not available"

**Cause:** Outdated runtime.txt or typo

**Fix:**
```bash
# Check available versions and update
echo "python-3.12.0" > runtime.txt

# Or use:
echo "python-3.11.4" > runtime.txt

git add runtime.txt
git commit -m "Update Python version"
git push origin main
```

---

### ❌ Error 10: "App keeps crashing/restarting"

**Cause:** Infinite loop, memory leak, or exceptions

**Fix:**
```python
# Add error handling in app.py
@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

# Add logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

---

## Successful Deployment Checklist

| Task | Status |
|------|--------|
| Procfile created | ✅ |
| runtime.txt created | ✅ |
| requirements.txt complete | ✅ |
| app.py uses PORT env var | ✅ |
| .gitignore configured | ✅ |
| model.pkl committed | ✅ |
| vectorizer.pkl committed | ✅ |
| Pushed to GitHub | ✅ |
| Render service connected | ✅ |
| Build succeeded | ✅ |
| App running | ✅ |
| Can access URL | ✅ |

---

## Deployment Workflow

```
1. Local Development
   └─ python app.py (test locally)

2. Prepare for Deployment
   ├─ Create Procfile
   ├─ Create runtime.txt
   └─ Update requirements.txt

3. Commit to GitHub
   ├─ git add .
   ├─ git commit -m "Deploy"
   └─ git push origin main

4. Configure Render
   ├─ Connect GitHub
   ├─ Set build command
   ├─ Set start command
   └─ Add environment variables

5. Deploy
   ├─ Click "Create Web Service"
   ├─ Wait for build
   ├─ Check logs
   └─ Access URL

6. Monitor
   ├─ Check logs regularly
   ├─ Monitor metrics
   └─ Handle errors
```

---

## Performance Tips

### 1. Gunicorn Workers
```bash
# More workers = better concurrency (default: 1)
gunicorn app:app --workers 4
```

**Formula:** `workers = (2 × CPU cores) + 1`

### 2. Worker Class
```bash
# For I/O-bound (default: sync)
gunicorn app:app --workers 4 --worker-class sync

# For async
gunicorn app:app --workers 4 --worker-class asyncio
```

### 3. Timeout
```bash
# Increase for long-running predictions
gunicorn app:app --timeout 120
```

### 4. Keep-Alive
```bash
# Connection pooling
gunicorn app:app --keepalive 5
```

---

## Cost Optimization

| Feature | Free | Paid |
|---------|------|------|
| Deployment | ✅ | ✅ |
| Custom domain | ❌ | ✅ |
| Auto-sleep | ✅ | ❌ |
| SSL/TLS | ✅ | ✅ |
| Support | Community | Priority |

**Free tier limits:**
- Auto-sleep after 15 min inactivity
- Limited deployment hours
- Shared resources

---

## Production Best Practices

### 1. Environment Variables
```bash
# Never hardcode secrets
os.environ.get('SECRET_KEY')
os.environ.get('DATABASE_URL')
```

### 2. Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.info("User prediction request")
logger.error("Model loading failed")
```

### 3. Error Handling
```python
@app.errorhandler(Exception)
def handle_error(e):
    return {'error': str(e)}, 500
```

### 4. Health Checks
```python
@app.route('/health', methods=['GET'])
def health():
    return {'status': 'healthy'}, 200
```

---

## Resources

- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **Gunicorn Docs**: https://gunicorn.org
- **Python Buildpacks**: https://render.com/docs/deploy-python

---

## Quick Reference

```bash
# Build Command
pip install -r requirements.txt

# Start Command
gunicorn app:app

# Python Version
python-3.11.4

# Typical requirements.txt
Flask==3.0.0
gunicorn==22.0.0
scikit-learn==1.8.0
pandas==3.0.2

# Procfile
web: gunicorn app:app

# Check deployment
curl https://your-app-name.onrender.com/health
```

---

## Support & Troubleshooting

**Check Render Logs:**
```
Dashboard → Service → Logs
```

**Common Log Messages:**
```
✓ Build succeeded
✓ Deploying...
✓ Service is live at https://...
✓ App is running
```

**For errors:**
1. Read error message carefully
2. Check Procfile, runtime.txt, requirements.txt
3. Verify models are committed
4. Check environment variables
5. Clear cache & redeploy

---

**Your Flask app is now production-ready on Render! 🚀**
