import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import traceback
import os
import json

# ============================================================================
# CONFIGURATION
# ============================================================================
app = Flask(__name__, template_folder='templates')

# Add CORS headers manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Global variables for model and encoders
model = None
encoders = None
feature_columns = None

# ============================================================================
# LOAD MODEL AND ENCODERS
# ============================================================================
def load_model_and_encoders():
    """Load the trained Random Forest model and LabelEncoders from disk."""
    global model, encoders, feature_columns
    
    # Try different possible model paths
    model_paths = ["mobile_price_model.pkl", "models/mobile_price_model.pkl", "../mobile_price_model.pkl"]
    model_loaded = False
    
    for model_path in model_paths:
        if os.path.exists(model_path):
            try:
                model = joblib.load(model_path)
                print(f"✅ Model loaded successfully from: {model_path}")
                model_loaded = True
                break
            except Exception as e:
                print(f"❌ Failed to load model from {model_path}: {str(e)}")
    
    if not model_loaded:
        print("❌ Model file not found in any location")
        return False
    
    # Load encoders if available
    encoders_paths = ["encoders.pkl", "models/encoders.pkl", "../encoders.pkl"]
    for enc_path in encoders_paths:
        if os.path.exists(enc_path):
            try:
                encoders = joblib.load(enc_path)
                print(f"✅ Encoders loaded successfully from: {enc_path}")
                break
            except Exception as e:
                print(f"⚠️ Could not load encoders from {enc_path}: {str(e)}")
    
    # Define feature columns in the exact order used during training
    feature_columns = [
        'brand', 'model_name', 'os', 'launch_year', '5g_support',
        'dual_sim', 'expandable_storage', 'water_resistance',
        'wireless_charging', 'fingerprint_sensor', 'face_unlock',
        'build_material', 'warranty_years', 'ram_gb', 'storage_gb',
        'display_type', 'fast_charging_w', 'rear_camera_mp', 'front_camera_mp'
    ]
    print("✅ Using feature columns order")
    
    return True

# ============================================================================
# HELPER FUNCTIONS FOR ENCODING
# ============================================================================
def encode_categorical_value(value, encoder, fallback=0):
    """Safely encode a categorical value using a fitted LabelEncoder."""
    try:
        if encoder is None:
            return fallback
        if hasattr(encoder, 'classes_') and value in encoder.classes_:
            return int(encoder.transform([value])[0])
        else:
            print(f"⚠️ Unknown category '{value}', using fallback {fallback}")
            return fallback
    except Exception as e:
        print(f"⚠️ Encoding error for '{value}': {str(e)}")
        return fallback

def encode_features(features_dict):
    """Convert incoming feature dictionary to encoded numerical array."""
    global encoders
    
    # Fallback mappings (if encoders not available)
    brand_fallback = {'Google': 0, 'Samsung': 1, 'Realme': 2, 'OnePlus': 3, 
                      'Nothing': 4, 'Oppo': 5, 'Xiaomi': 6, 'Apple': 7, 'Vivo': 8}
    os_fallback = {'Android': 0, 'iOS': 1}
    build_fallback = {'Metal': 0, 'Glass': 1, 'Plastic': 2, 'Ceramic': 3}
    display_fallback = {'AMOLED': 0, 'LCD': 1, 'OLED': 2, 'Super AMOLED': 3}
    
    # Initialize encoded features dictionary
    encoded = {}
    
    # Brand encoding
    brand_raw = features_dict.get('brand', 'Google')
    if encoders and 'brand' in encoders:
        encoded['brand'] = encode_categorical_value(brand_raw, encoders['brand'], 0)
    else:
        encoded['brand'] = brand_fallback.get(brand_raw, 0)
    
    # Model name encoding
    model_raw = features_dict.get('model_name', 'custom')
    if encoders and 'model_name' in encoders:
        encoded['model_name'] = encode_categorical_value(model_raw, encoders['model_name'], 0)
    else:
        encoded['model_name'] = 0
    
    # OS encoding
    os_raw = features_dict.get('os', 'Android')
    if encoders and 'os' in encoders:
        encoded['os'] = encode_categorical_value(os_raw, encoders['os'], 0)
    else:
        encoded['os'] = os_fallback.get(os_raw, 0)
    
    # Build material encoding
    build_raw = features_dict.get('build_material', 'Glass')
    if encoders and 'build_material' in encoders:
        encoded['build_material'] = encode_categorical_value(build_raw, encoders['build_material'], 1)
    else:
        encoded['build_material'] = build_fallback.get(build_raw, 1)
    
    # Display type encoding
    display_raw = features_dict.get('display_type', 'AMOLED')
    if encoders and 'display_type' in encoders:
        encoded['display_type'] = encode_categorical_value(display_raw, encoders['display_type'], 0)
    else:
        encoded['display_type'] = display_fallback.get(display_raw, 0)
    
    # Numerical features
    encoded['launch_year'] = int(features_dict.get('launch_year', 2022))
    encoded['5g_support'] = int(features_dict.get('5g_support', 1))
    encoded['dual_sim'] = int(features_dict.get('dual_sim', 1))
    encoded['expandable_storage'] = int(features_dict.get('expandable_storage', 0))
    encoded['water_resistance'] = int(features_dict.get('water_resistance', 0))
    encoded['wireless_charging'] = int(features_dict.get('wireless_charging', 0))
    encoded['fingerprint_sensor'] = int(features_dict.get('fingerprint_sensor', 1))
    encoded['face_unlock'] = int(features_dict.get('face_unlock', 1))
    encoded['warranty_years'] = float(features_dict.get('warranty_years', 1))
    encoded['ram_gb'] = int(features_dict.get('ram_gb', 8))
    encoded['storage_gb'] = int(features_dict.get('storage_gb', 128))
    encoded['fast_charging_w'] = int(features_dict.get('fast_charging_w', 25))
    encoded['rear_camera_mp'] = int(features_dict.get('rear_camera_mp', 50))
    encoded['front_camera_mp'] = int(features_dict.get('front_camera_mp', 16))
    
    # Create feature vector in correct column order
    feature_vector = [encoded[col] for col in feature_columns]
    
    return np.array(feature_vector).reshape(1, -1)

# ============================================================================
# API ROUTES
# ============================================================================
@app.route('/')
def index():
    """Serve the main HTML page."""
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>SmartPrice AI - Mobile Price Predictor</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>📱 SmartPrice AI</h1>
            <p>Error loading template: {str(e)}</p>
            <p>Please ensure 'index.html' is in the 'templates' folder.</p>
            <hr>
            <h3>API Endpoints:</h3>
            <ul style="text-align: left; display: inline-block;">
                <li>POST /predict - Make predictions</li>
                <li>GET /health - Check server health</li>
            </ul>
        </body>
        </html>
        """, 500

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """Predict mobile phone price based on provided features."""
    global model
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return '', 200
    
    # Check if model is loaded
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please check server logs.',
            'status': 'error'
        }), 503
    
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Handle two possible input formats
        if 'features' in data and isinstance(data['features'], list):
            features = np.array(data['features']).reshape(1, -1)
            
            if features.shape[1] != len(feature_columns):
                return jsonify({
                    'error': f'Expected {len(feature_columns)} features, got {features.shape[1]}',
                    'expected_features': feature_columns
                }), 400
        else:
            features = encode_features(data)
        
        # Make prediction
        prediction = model.predict(features)
        predicted_price = float(prediction[0])
        predicted_price = round(predicted_price, 2)
        
        return jsonify({
            'predicted_price': predicted_price,
            'currency': 'INR',
            'status': 'success',
            'model_used': 'RandomForestRegressor'
        })
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'encoders_loaded': encoders is not None
    })

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("📱 SmartPrice AI - Mobile Price Prediction API")
    print("=" * 60)
    
    # Check if templates folder exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("📁 Created 'templates' folder. Please place index.html inside it.")
    
    # Load model and encoders
    success = load_model_and_encoders()
    
    if success:
        print("\n🚀 Starting Flask server...")
        print("📍 Open in browser: http://localhost:5000")
        print("📍 API endpoint: POST http://localhost:5000/predict")
        print("📍 Health check: GET http://localhost:5000/health")
        print("\n✨ Server is ready! Press Ctrl+C to stop.")
        print("=" * 60)
        
        # Run the Flask app
        app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
    else:
        print("\n❌ Failed to load required model files.")
        print("   Please ensure the following files exist:")
        print("   - mobile_price_model.pkl")
        print("   - encoders.pkl (optional)")
        print("\n   You can train the model using the provided notebook.")