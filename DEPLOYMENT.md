# Project Folder Structure - Flask ML Project

```
fake-news-detection/
│
├── app.py                      # Main Flask application
├── train_model.py              # Model training script
├── test_app.py                 # Application tests
│
├── model.pkl                   # Trained LogisticRegression model (binary file)
├── vectorizer.pkl              # TF-IDF vectorizer (binary file)
│
├── templates/
│   └── index.html              # HTML template for web interface
│
├── static/                     # (Optional) Static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version specification
├── Procfile                    # Heroku/Render process definition
├── render.yaml                 # Render deployment configuration
│
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
│
├── Fake.csv                    # Fake news dataset (training data)
├── True.csv                    # Real news dataset (training data)
│
└── run.bat                     # Windows batch launcher (optional)
```

## File Descriptions

### Core Application Files
- **app.py**: Main Flask application with routes
- **train_model.py**: Script to train the ML model
- **test_app.py**: Unit tests for Flask application

### Model Files
- **model.pkl**: Serialized LogisticRegression model (created after training)
- **vectorizer.pkl**: Serialized TfidfVectorizer (created after training)

### Web Files
- **templates/index.html**: Jinja2 HTML template with form and results

### Configuration Files
- **requirements.txt**: All Python package dependencies with versions
- **runtime.txt**: Specifies Python version (e.g., python-3.11.4)
- **Procfile**: Deployment instruction for Heroku/Render
- **render.yaml**: Render-specific deployment configuration
- **.gitignore**: Files to exclude from Git repository

### Documentation
- **README.md**: Project documentation and setup instructions

### Data Files
- **Fake.csv**: Training data (fake news)
- **True.csv**: Training data (real news)

### Optional Files
- **run.bat**: Windows batch file to easily run the Flask app
- **static/**: Static assets (CSS, JS, images) if needed

---

## Deployment on Render

### Prerequisites
1. Push code to GitHub repository
2. Sign up on [render.com](https://render.com)
3. Have Python 3.11+ and trained models (model.pkl, vectorizer.pkl)

### Steps to Deploy

#### 1. Connect GitHub Repository
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/fake-news-detection.git
git push -u origin main
```

#### 2. Create Render Service
- Go to [dashboard.render.com](https://dashboard.render.com)
- Click "New +" → "Web Service"
- Connect your GitHub repository
- Select the repository
- Name: `fake-news-detection`
- Root Directory: (leave empty)
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Click "Create Web Service"

#### 3. Alternative: Using render.yaml (YAML Deploy)
```bash
git push origin main
```
Render will automatically detect `render.yaml` and deploy accordingly.

### Environment Variables (if needed)
In Render dashboard:
- Set `FLASK_ENV=production` (recommended)
- Set `PORT=5000` (if custom port needed)

---

## Project Structure Best Practices

✅ **Recommended Structure:**
```
project/
├── app.py                      # Main application
├── models/                     # Optional: Separate model files
│   ├── model.pkl
│   └── vectorizer.pkl
├── templates/                  # HTML templates
├── static/                     # CSS, JS, images
├── tests/                      # Unit tests
├── data/                       # Datasets
│   ├── Fake.csv
│   └── True.csv
└── config.py                   # Configuration (optional)
```

## Key Files for Deployment

### requirements.txt
```
Flask==3.0.0
scikit-learn==1.8.0
pandas==3.0.2
gunicorn==22.0.0
numpy==2.4.4
scipy==1.17.1
```

### Procfile
```
web: gunicorn app:app
```

### runtime.txt
```
python-3.11.4
```

### render.yaml
```yaml
services:
  - type: web
    name: fake-news-detection
    runtime: python
    pythonVersion: 3.11
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
```

---

## Important Notes for Deployment

1. **Model Files**: Ensure model.pkl and vectorizer.pkl are committed to Git
2. **Data Files**: Optional - can exclude large CSV files from Git if needed
3. **Port Binding**: Use `$PORT` environment variable (Render sets this)
4. **Python Version**: Specify in runtime.txt (e.g., 3.11.4)
5. **Dependencies**: Keep requirements.txt updated with exact versions
6. **Debug Mode**: Set `debug=False` in production

---

## Local Development

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Run tests
python test_app.py
```

## Production Deployment

```bash
# Using gunicorn (production server)
gunicorn app:app --workers 4 --bind 0.0.0.0:5000

# On Render (automatic via Procfile)
```

---

## Checklist Before Deployment

- ✅ model.pkl exists and works
- ✅ vectorizer.pkl exists and works
- ✅ requirements.txt has all dependencies
- ✅ runtime.txt specifies Python version
- ✅ Procfile configured for production server
- ✅ app.py has debug=False for production
- ✅ README.md with setup instructions
- ✅ .gitignore excludes unnecessary files
- ✅ Code pushed to GitHub
- ✅ Render service created and linked

---

## Troubleshooting Deployment

### Build Fails
- Check Python version matches runtime.txt
- Verify all dependencies in requirements.txt
- Ensure model files are committed to Git

### Runtime Errors
- Check logs in Render dashboard
- Verify model.pkl and vectorizer.pkl paths
- Ensure PORT environment variable is used

### Slow Startup
- Pre-compile Python files
- Use binary format for large models
- Consider model caching strategies

---

For more info: [Render Deployment Guide](https://render.com/docs/deploy-flask)
