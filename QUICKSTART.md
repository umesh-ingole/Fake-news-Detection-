# Quick Start Guide

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/fake-news-detection.git
cd fake-news-detection
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Flask App
```bash
python app.py
```
Visit: http://127.0.0.1:5000

### 5. Run Tests
```bash
python test_app.py
```

---

## Deployment on Render

### Option 1: Web Dashboard
1. Sign up at [render.com](https://render.com)
2. Connect GitHub repository
3. Create new "Web Service"
4. Select repository and branch
5. Configure:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. Click Deploy

### Option 2: Using render.yaml (YAML Deploy)
1. Ensure `render.yaml` is in repository
2. Push to GitHub
3. Render automatically detects and deploys

---

## Project Structure
```
fake-news-detection/
├── app.py                    # Flask application
├── config.py                 # Configuration
├── train_model.py            # Model training
├── model.pkl                 # Trained model
├── vectorizer.pkl            # TF-IDF vectorizer
├── templates/
│   └── index.html            # Web interface
├── requirements.txt          # Dependencies
├── runtime.txt               # Python version
├── Procfile                  # Process definition
├── render.yaml               # Render config
├── .gitignore               # Git ignore
└── README.md                # Documentation
```

---

## Environment Variables

### Development (.env)
```
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000
```

### Production (Render Dashboard)
```
FLASK_ENV=production
FLASK_DEBUG=0
PORT=5000
```

---

## Features

✅ 98.53% accuracy on test data
✅ Real-time fake news detection
✅ Beautiful responsive UI
✅ Production-ready Flask app
✅ Easy Render deployment
✅ Full test suite
✅ Comprehensive documentation

---

## File Descriptions

| File | Purpose |
|------|---------|
| app.py | Main Flask application |
| config.py | Configuration management |
| train_model.py | ML model training script |
| model.pkl | Trained LogisticRegression model |
| vectorizer.pkl | TF-IDF vectorizer |
| templates/index.html | Web interface template |
| requirements.txt | Python dependencies |
| Procfile | Heroku/Render process definition |
| render.yaml | Render deployment config |
| .gitignore | Git exclude patterns |
| DEPLOYMENT.md | Detailed deployment guide |

---

## Troubleshooting

### Port Already in Use
```bash
# Change port
python app.py --port 8000
```

### Model Not Found
```bash
# Ensure model.pkl and vectorizer.pkl exist in root directory
ls -la *.pkl
```

### Dependencies Not Installing
```bash
# Clear pip cache
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## Next Steps

1. ✅ Train model locally (`python train_model.py`)
2. ✅ Test Flask app (`python test_app.py`)
3. ✅ Push to GitHub
4. ✅ Deploy on Render
5. ✅ Access live app on Render URL

---

## Support

For issues or questions:
- Check [README.md](README.md)
- See [DEPLOYMENT.md](DEPLOYMENT.md)
- Review [Render Documentation](https://render.com/docs)
