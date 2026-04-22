"""
Fake News Detection Flask Web Application
Production-ready deployment with error handling and logging

Author: ML Team
Version: 1.0
"""

import os
import pickle
import logging
from flask import Flask, render_template, request, jsonify

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Configure logging for better debugging and monitoring
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Print to console
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# FLASK APP INITIALIZATION
# ============================================================================

app = Flask(__name__)

# Configure Flask based on environment (development or production)
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    logger.info("Running in PRODUCTION mode")
else:
    app.config['DEBUG'] = True
    logger.info("Running in DEVELOPMENT mode")

# ============================================================================
# MODEL AND VECTORIZER LOADING
# ============================================================================

# Global variables for model and vectorizer
model = None
vectorizer = None


def load_models():
    """
    Load trained ML models from pickle files.
    
    Returns:
        tuple: (model, vectorizer) or (None, None) if loading fails
    """
    global model, vectorizer
    
    # Load LogisticRegression model
    try:
        logger.info("Loading model.pkl...")
        with open('model.pkl', 'rb') as f:
            model = pickle.load(f)
        logger.info("✓ Model loaded successfully")
    except FileNotFoundError:
        logger.error("ERROR: model.pkl not found in current directory")
        logger.error("Please ensure model.pkl exists in the same directory as app.py")
        model = None
    except pickle.UnpicklingError as e:
        logger.error(f"ERROR: Corrupted model file - {str(e)}")
        model = None
    except Exception as e:
        logger.error(f"ERROR loading model: {type(e).__name__}: {str(e)}")
        model = None
    
    # Load TF-IDF Vectorizer
    try:
        logger.info("Loading vectorizer.pkl...")
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        logger.info("✓ Vectorizer loaded successfully")
    except FileNotFoundError:
        logger.error("ERROR: vectorizer.pkl not found in current directory")
        logger.error("Please ensure vectorizer.pkl exists in the same directory as app.py")
        vectorizer = None
    except pickle.UnpicklingError as e:
        logger.error(f"ERROR: Corrupted vectorizer file - {str(e)}")
        vectorizer = None
    except Exception as e:
        logger.error(f"ERROR loading vectorizer: {type(e).__name__}: {str(e)}")
        vectorizer = None
    
    return model, vectorizer


# Load models on application startup
model, vectorizer = load_models()

# ============================================================================
# ROUTE HANDLERS
# ============================================================================


@app.route('/', methods=['GET'])
def index():
    """
    Homepage route - renders the main web interface.
    
    Returns:
        str: Rendered HTML template
        500: If template rendering fails
    """
    try:
        logger.info("Homepage accessed")
        return render_template('index.html')
    except FileNotFoundError:
        logger.error("ERROR: index.html template not found")
        return jsonify({'error': 'Template not found'}), 500
    except Exception as e:
        logger.error(f"ERROR rendering homepage: {type(e).__name__}: {str(e)}")
        return jsonify({'error': 'Failed to load homepage'}), 500


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Prediction route - handles both GET (display form) and POST (process prediction).
    
    Returns:
        - GET: Rendered HTML template with form
        - POST: HTML with prediction result or error message
        - AJAX: JSON response with prediction, confidence, and error (if any)
    
    Form Data:
        news (str): News text to analyze
    
    Response:
        JSON: {
            'result': 'Real News' or 'Fake News',
            'confidence': '98.53%',
            'error': None or error message
        }
    """
    prediction = None
    confidence = None
    error = None
    news_text = ""
    
    if request.method == 'POST':
        try:
            # Extract news text from form
            news_text = request.form.get('news', '').strip()
            logger.info(f"Received prediction request - Text length: {len(news_text)} chars")
            
            # VALIDATION 1: Check if text is empty
            if not news_text:
                error = "Please enter some text to analyze"
                logger.warning("Empty text submitted")
            
            # VALIDATION 2: Check if models are loaded
            elif model is None or vectorizer is None:
                error = "Model or vectorizer not loaded. Please restart the application."
                logger.error("Models not loaded when prediction requested")
            
            # VALIDATION 3: Text length validation
            elif len(news_text) < 10:
                error = "Text is too short. Please enter at least 10 characters."
                logger.warning(f"Text too short: {len(news_text)} chars")
            
            # VALIDATION 4: Text length upper limit (optional)
            elif len(news_text) > 5000:
                error = "Text is too long. Please enter less than 5000 characters."
                logger.warning(f"Text too long: {len(news_text)} chars")
            
            else:
                # Step 1: Transform text using TF-IDF vectorizer
                try:
                    logger.info("Vectorizing text...")
                    text_tfidf = vectorizer.transform([news_text])
                    logger.info(f"✓ Text vectorized - Shape: {text_tfidf.shape}")
                except Exception as e:
                    error = f"Error processing text: {str(e)}"
                    logger.error(f"Vectorization error: {type(e).__name__}: {str(e)}")
                
                # Step 2: Make prediction using trained model
                if error is None:
                    try:
                        logger.info("Making prediction...")
                        # Get prediction (0=Fake, 1=Real)
                        pred = model.predict(text_tfidf)[0]
                        # Get confidence score
                        conf = model.predict_proba(text_tfidf).max()
                        
                        # Convert numeric prediction to human-readable label
                        prediction = "Real News" if pred == 1 else "Fake News"
                        confidence = f"{conf:.2%}"
                        
                        logger.info(f"✓ Prediction: {prediction} (Confidence: {confidence})")
                    except Exception as e:
                        error = f"Error making prediction: {str(e)}"
                        logger.error(f"Prediction error: {type(e).__name__}: {str(e)}")
        
        except Exception as e:
            error = f"Unexpected error: {str(e)}"
            logger.error(f"Unexpected error in prediction: {type(e).__name__}: {str(e)}", exc_info=True)
    
    # Handle both AJAX (JSON) and form submission (HTML) requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX request - return JSON response
        logger.info(f"AJAX response: {prediction}, Error: {error}")
        status_code = 200 if not error else 400
        return jsonify({
            'result': prediction,
            'confidence': confidence,
            'error': error
        }), status_code
    else:
        # Regular form submission - render HTML template with results
        try:
            return render_template(
                'index.html',
                prediction=prediction,
                confidence=confidence,
                error=error,
                news_text=news_text
            )
        except Exception as e:
            logger.error(f"ERROR rendering prediction template: {type(e).__name__}: {str(e)}")
            return f"Error: {str(e)}", 500


@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint - used for monitoring and uptime checks.
    Useful for Render and other cloud platforms to verify app is running.
    
    Returns:
        JSON: {
            'status': 'healthy' or 'degraded',
            'model_loaded': bool,
            'vectorizer_loaded': bool
        }
    """
    try:
        # Determine status based on whether models are loaded
        status = 'healthy' if (model is not None and vectorizer is not None) else 'degraded'
        logger.info(f"Health check - Status: {status}")
        
        return jsonify({
            'status': status,
            'model_loaded': model is not None,
            'vectorizer_loaded': vectorizer is not None
        }), 200
    except Exception as e:
        logger.error(f"ERROR in health check: {type(e).__name__}: {str(e)}")
        return jsonify({'status': 'error', 'error': str(e)}), 500


# ============================================================================
# ERROR HANDLERS - Handle various error scenarios
# ============================================================================


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    logger.warning(f"404 Error: {request.path}")
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors."""
    logger.warning(f"405 Error: {request.method} {request.path}")
    return jsonify({'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    logger.error(f"500 Error: {type(error).__name__}: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Handle all unexpected errors."""
    logger.error(f"Unexpected error: {type(error).__name__}: {str(error)}", exc_info=True)
    return jsonify({'error': 'An unexpected error occurred'}), 500


# ============================================================================
# REQUEST/RESPONSE HOOKS - For monitoring
# ============================================================================


@app.before_request
def log_request_info():
    """Log incoming requests (optional - can be verbose)."""
    if request.method != 'GET':  # Only log POST requests to reduce spam
        logger.debug(f"Request: {request.method} {request.path}")


@app.after_request
def log_response_info(response):
    """Log response status codes."""
    if response.status_code >= 400:  # Log errors
        logger.warning(f"Response: {response.status_code} for {request.method} {request.path}")
    return response


# ============================================================================
# APPLICATION STARTUP
# ============================================================================


if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    env = os.environ.get('FLASK_ENV', 'development')
    debug_mode = env != 'production'
    
    logger.info("=" * 70)
    logger.info("Starting Fake News Detection Flask Application")
    logger.info("=" * 70)
    logger.info(f"Port: {port}")
    logger.info(f"Environment: {env}")
    logger.info(f"Debug mode: {debug_mode}")
    logger.info(f"Model loaded: {model is not None}")
    logger.info(f"Vectorizer loaded: {vectorizer is not None}")
    logger.info("=" * 70)
    
    # Run Flask development server
    # NOTE: For production, use gunicorn: gunicorn app:app
    try:
        app.run(
            debug=debug_mode,
            host='0.0.0.0',
            port=port,
            threaded=True
        )
    except Exception as e:
        logger.error(f"FATAL ERROR: Failed to start application: {str(e)}")
        raise
