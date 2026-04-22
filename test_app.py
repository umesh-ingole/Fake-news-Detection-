"""
Quick test script to verify Flask app functionality
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, model, vectorizer

def test_app():
    """Test Flask app routes and predictions"""
    
    print("=" * 60)
    print("Testing Fake News Detection Flask App")
    print("=" * 60)
    
    # Test 1: Check model and vectorizer loaded
    print("\n[Test 1] Model and Vectorizer Loading")
    if model is not None and vectorizer is not None:
        print("✓ Model loaded successfully")
        print("✓ Vectorizer loaded successfully")
    else:
        print("✗ Failed to load model or vectorizer")
        return False
    
    # Test 2: Test prediction functionality
    print("\n[Test 2] Prediction Functionality")
    test_texts = [
        "The president announced a new policy today.",
        "SHOCKING: Scientists discover aliens",
        "The government reported economic growth this quarter."
    ]
    
    for text in test_texts:
        try:
            tfidf = vectorizer.transform([text])
            prediction = model.predict(tfidf)[0]
            confidence = model.predict_proba(tfidf).max()
            result = "Real News" if prediction == 1 else "Fake News"
            print(f"✓ '{text[:40]}...' → {result} ({confidence:.2%})")
        except Exception as e:
            print(f"✗ Prediction failed: {e}")
            return False
    
    # Test 3: Test Flask routes
    print("\n[Test 3] Flask Routes")
    client = app.test_client()
    
    # Test homepage
    response = client.get('/')
    if response.status_code == 200:
        print(f"✓ GET / → {response.status_code} (Homepage)")
    else:
        print(f"✗ GET / → {response.status_code}")
        return False
    
    # Test health check
    response = client.get('/health')
    if response.status_code == 200 and 'status' in response.json:
        print(f"✓ GET /health → {response.status_code} (Health Check)")
    else:
        print(f"✗ GET /health → {response.status_code}")
        return False
    
    # Test prediction POST (regular form submission - returns HTML)
    response = client.post('/predict', data={'news': 'Test news text for detection'})
    if response.status_code == 200 and 'Fake' in response.data.decode() or 'Real' in response.data.decode():
        print(f"✓ POST /predict → {response.status_code} (HTML template rendered)")
    else:
        print(f"✗ POST /predict → {response.status_code}")
        return False
    
    # Test empty prediction (regular form submission - returns HTML with error)
    response = client.post('/predict', data={'news': ''})
    if response.status_code == 200 and 'Error' in response.data.decode():
        print(f"✓ POST /predict (empty) → {response.status_code} (Error handling works)")
    else:
        print(f"✗ POST /predict (empty) → {response.status_code}")
        return False
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)
    print("\nTo start the app, run: python app.py")
    print("Then open: http://127.0.0.1:5000")
    return True

if __name__ == '__main__':
    try:
        success = test_app()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
