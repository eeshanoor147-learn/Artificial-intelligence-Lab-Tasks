import os
import pandas as pd
import numpy as np
import joblib
from flask import Flask, request, render_template, jsonify
from sklearn.ensemble import RandomForestRegressor
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# ---------- Automatically create templates folder and HTML file if missing ----------
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')
INDEX_HTML_PATH = os.path.join(TEMPLATES_DIR, 'index.html')

if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)
    print("Created 'templates' folder.")

if not os.path.exists(INDEX_HTML_PATH):
    with open(INDEX_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartPrice AI - Phone Price Predictor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 30px;
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3rem;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            margin-bottom: 10px;
        }
        .header p {
            color: rgba(255, 255, 255, 0.9);
            font-size: 1.1rem;
        }
        .form-section {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 20px;
            padding: 25px;
            margin-bottom: 25px;
            transition: transform 0.3s ease;
        }
        .form-section:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.2);
        }
        .section-title {
            font-size: 1.5rem;
            color: #fff;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.3);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .section-title i {
            font-size: 1.5rem;
        }
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .form-group label {
            color: #fff;
            font-weight: 500;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .form-group label i {
            font-size: 1rem;
        }
        input, select {
            padding: 12px 15px;
            border: none;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.95);
            font-size: 0.9rem;
            transition: all 0.3s ease;
            font-family: inherit;
        }
        input:focus, select:focus {
            outline: none;
            box-shadow: 0 0 0 3px rgba(118, 75, 162, 0.5);
            transform: scale(1.02);
        }
        .radio-group {
            display: flex;
            gap: 15px;
            background: rgba(255, 255, 255, 0.95);
            padding: 10px 15px;
            border-radius: 12px;
        }
        .radio-option {
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }
        .radio-option input[type="radio"] {
            width: auto;
            margin: 0;
            padding: 0;
        }
        .predict-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            font-size: 1.2rem;
            font-weight: 600;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        .predict-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
        }
        .predict-btn:active {
            transform: translateY(0);
        }
        .result-card {
            background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
            border-radius: 20px;
            padding: 25px;
            margin-top: 30px;
            text-align: center;
            display: none;
            animation: slideUp 0.5s ease;
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .result-card.show {
            display: block;
        }
        .result-title {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 10px;
        }
        .result-price {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin: 10px 0;
        }
        .error-message {
            color: #dc3545;
            background: rgba(220, 53, 69, 0.1);
            padding: 15px;
            border-radius: 12px;
            margin-top: 20px;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 1s ease-in-out infinite;
            vertical-align: middle;
            margin-left: 10px;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        @media (max-width: 768px) {
            .container { padding: 15px; }
            .form-grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 2rem; }
        }
        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }
        .tooltip {
            cursor: help;
            border-bottom: 1px dashed rgba(255, 255, 255, 0.5);
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-mobile-alt"></i> SmartPrice AI</h1>
            <p>Advanced Smartphone Price Prediction Engine | Powered by Random Forest</p>
        </div>
        <form id="predictionForm">
            <!-- Basic Information Section -->
            <div class="form-section">
                <div class="section-title">
                    <i class="fas fa-info-circle"></i>
                    <span>Basic Information</span>
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label><i class="fas fa-tag"></i> Brand</label>
                        <select id="brand" name="brand" required>
                            <option value="">Select Brand</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-calendar"></i> Launch Year</label>
                        <input type="number" id="launch_year" name="launch_year" value="2023" min="2015" max="2025" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-microchip"></i> Chipset</label>
                        <select id="chipset" name="chipset" required>
                            <option value="">Select Chipset</option>
                        </select>
                    </div>
                </div>
            </div>
            <!-- Features & Build Section -->
            <div class="form-section">
                <div class="section-title">
                    <i class="fas fa-cogs"></i>
                    <span>Features & Build</span>
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label><i class="fas fa-database"></i> RAM (GB)</label>
                        <input type="number" id="ram_gb" name="ram_gb" value="8" min="2" max="24" step="1" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-hdd"></i> Storage (GB)</label>
                        <input type="number" id="storage_gb" name="storage_gb" value="128" min="32" max="1024" step="32" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-charging-station"></i> Fast Charging (W)</label>
                        <input type="number" id="fast_charging_w" name="fast_charging_w" value="25" min="0" max="200" step="5" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-weight-hanging"></i> Weight (g)</label>
                        <input type="number" id="weight_g" name="weight_g" value="180" min="100" max="350" step="1" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-charging-station"></i> Wireless Charging</label>
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="wireless_charging" value="yes" checked> Yes</label>
                            <label class="radio-option"><input type="radio" name="wireless_charging" value="no"> No</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-tachometer-alt"></i> Refresh Rate (Hz)</label>
                        <input type="number" id="refresh_rate_hz" name="refresh_rate_hz" value="90" min="60" max="144" step="30" required>
                    </div>
                </div>
            </div>
            <!-- Display & Camera Section -->
            <div class="form-section">
                <div class="section-title">
                    <i class="fas fa-eye"></i>
                    <span>Display & Camera</span>
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label><i class="fas fa-tv"></i> Display Type</label>
                        <select id="display_type" name="display_type" required>
                            <option value="">Select Display Type</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-camera"></i> Rear Camera (MP)</label>
                        <input type="number" id="rear_camera_mp" name="rear_camera_mp" value="50" min="12" max="200" step="2" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-camera-retro"></i> Front Camera (MP)</label>
                        <input type="number" id="front_camera_mp" name="front_camera_mp" value="16" min="8" max="64" step="2" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-battery-full"></i> Battery (mAh)</label>
                        <input type="number" id="battery_mah" name="battery_mah" value="5000" min="2000" max="8000" step="100" required>
                    </div>
                </div>
            </div>
            <!-- Sensors & Others Section -->
            <div class="form-section">
                <div class="section-title">
                    <i class="fas fa-microchip"></i>
                    <span>Sensors & Performance</span>
                </div>
                <div class="form-grid">
                    <div class="form-group">
                        <label><i class="fas fa-thumbtack"></i> Fingerprint Sensor</label>
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="fingerprint_sensor" value="yes" checked> Yes</label>
                            <label class="radio-option"><input type="radio" name="fingerprint_sensor" value="no"> No</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-smile"></i> Face Unlock</label>
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="face_unlock" value="yes" checked> Yes</label>
                            <label class="radio-option"><input type="radio" name="face_unlock" value="no"> No</label>
                        </div>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-wifi"></i> Wi-Fi Version</label>
                        <select id="wifi_version" name="wifi_version" required>
                            <option value="">Select Wi-Fi Version</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-bluetooth"></i> Bluetooth Version</label>
                        <input type="number" id="bluetooth_version" name="bluetooth_version" value="5.2" step="0.1" min="4.0" max="6.0" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-chart-line"></i> GPU Score</label>
                        <input type="number" id="gpu_score" name="gpu_score" value="5000" min="1000" max="15000" step="100" required>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-chart-bar"></i> CPU Score</label>
                        <input type="number" id="cpu_score" name="cpu_score" value="8000" min="2000" max="20000" step="100" required>
                    </div>
                </div>
            </div>
            <button type="submit" class="predict-btn">
                <i class="fas fa-chart-line"></i> Predict Price 
                <span id="loadingIndicator" style="display: none;"><span class="loading"></span></span>
            </button>
        </form>
        <div id="result" class="result-card">
            <div class="result-title"><i class="fas fa-chart-line"></i> Predicted Smartphone Price</div>
            <div class="result-price" id="predictedPrice">₹0.00</div>
            <div id="errorMessage" style="display: none;" class="error-message"></div>
        </div>
    </div>
    <script>
        async function loadFeatureOptions() {
            try {
                const response = await fetch('/api/features');
                const data = await response.json();
                if (data.categorical_options) {
                    for (const [category, options] of Object.entries(data.categorical_options)) {
                        const select = document.getElementById(category);
                        if (select && options) {
                            options.forEach(option => {
                                const opt = document.createElement('option');
                                opt.value = option;
                                opt.textContent = option;
                                select.appendChild(opt);
                            });
                        }
                    }
                }
            } catch (error) {
                console.error('Error loading feature options:', error);
            }
        }
        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const loadingIndicator = document.getElementById('loadingIndicator');
            const predictBtn = document.querySelector('.predict-btn');
            const resultCard = document.getElementById('result');
            const errorMsg = document.getElementById('errorMessage');
            loadingIndicator.style.display = 'inline-block';
            predictBtn.disabled = true;
            resultCard.classList.remove('show');
            errorMsg.style.display = 'none';
            const formData = new FormData(e.target);
            try {
                const response = await fetch('/predict', { method: 'POST', body: formData });
                const data = await response.json();
                if (data.success) {
                    const priceElement = document.getElementById('predictedPrice');
                    priceElement.textContent = data.formatted_price;
                    resultCard.classList.add('show');
                } else {
                    errorMsg.textContent = data.error || 'Prediction failed. Please check your inputs.';
                    errorMsg.style.display = 'block';
                    resultCard.classList.add('show');
                }
            } catch (error) {
                errorMsg.textContent = 'Network error. Please try again.';
                errorMsg.style.display = 'block';
                resultCard.classList.add('show');
            } finally {
                loadingIndicator.style.display = 'none';
                predictBtn.disabled = false;
            }
        });
        loadFeatureOptions();
        document.querySelectorAll('input, select').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
                this.parentElement.style.transition = 'transform 0.3s ease';
            });
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
    </script>
</body>
</html>""")
    print("Created 'index.html' inside templates folder.")
# ---------------------------------------------------------------------

# Global variables to store model, feature names, and encoders
model = None
feature_columns = None
categorical_encoders = {}
categorical_cols = ['brand', 'build_material', 'wifi_version', 'chipset', 'display_type']
numerical_cols = []

def load_model_and_encoders():
    """Load the trained model and create encoders from the original dataset"""
    global model, feature_columns, categorical_encoders, numerical_cols
    
    # Load the trained model
    try:
        model = joblib.load('mobile_price_prediction.pkl')
        print("Model loaded successfully.")
    except FileNotFoundError:
        print("ERROR: 'mobile_price_prediction.pkl' not found. Please ensure the model file exists.")
        raise
    
    # Load the original dataset to create encoders
    try:
        df = pd.read_csv('smartphone_dataset_1lacc.csv')
        print("Dataset loaded successfully.")
    except FileNotFoundError:
        print("ERROR: 'smartphone_dataset_1lacc.csv' not found. Please ensure the dataset file exists.")
        raise
    
    # Drop the same columns as in the notebook
    columns_to_drop = ['model_name', 'camera_setup', 'os']
    df.drop(columns=columns_to_drop, inplace=True)
    
    # Separate features (X) and target (y)
    X = df.drop('price_inr', axis=1)
    
    # Store feature columns in the order they will be used (from the trained model)
    feature_columns = list(model.feature_names_in_)
    
    # Create encoders for each categorical column using factorize
    for col in categorical_cols:
        if col in X.columns:
            codes, uniques = pd.factorize(X[col])
            categorical_encoders[col] = {str(val): idx for idx, val in enumerate(uniques)}
            categorical_encoders[f'{col}_reverse'] = {idx: str(val) for idx, val in enumerate(uniques)}
            print(f"Loaded encoder for {col}: {len(uniques)} unique values")
    
    print(f"Model loaded successfully. Expected features: {len(feature_columns)}")
    print(f"First 5 feature columns: {feature_columns[:5]}...")

def preprocess_input(data_dict):
    """Convert user input to model-ready format"""
    input_dict = {}
    
    # Process categorical features using saved encoders
    for col in categorical_cols:
        if col in data_dict:
            user_value = str(data_dict[col])
            if col in categorical_encoders:
                if user_value in categorical_encoders[col]:
                    input_dict[col] = categorical_encoders[col][user_value]
                else:
                    default_code = list(categorical_encoders[col].values())[0]
                    input_dict[col] = default_code
                    print(f"Warning: '{user_value}' not found for {col}, using default code {default_code}")
            else:
                input_dict[col] = 0
        else:
            input_dict[col] = 0
    
    # Process numerical features
    numerical_features = [
        'launch_year', '5g_support', 'dual_sim', 'expandable_storage', 
        'water_resistance', 'wireless_charging', 'fingerprint_sensor', 
        'face_unlock', 'gpu_score', 'cpu_score', 'screen_to_body_ratio',
        'colors_available', 'warranty_years', 'bluetooth_version', 'ram_gb',
        'storage_gb', 'thickness_mm', 'refresh_rate_hz', 'battery_mah',
        'fast_charging_w', 'rear_camera_mp', 'front_camera_mp', 'weight_g'
    ]
    
    for col in numerical_features:
        try:
            input_dict[col] = float(data_dict.get(col, 0))
        except (ValueError, TypeError):
            input_dict[col] = 0
    
    # Create DataFrame with correct column order
    input_df = pd.DataFrame([input_dict])
    
    # Ensure all required columns are present and in the correct order
    missing_cols = set(feature_columns) - set(input_df.columns)
    for col in missing_cols:
        input_df[col] = 0
    
    input_df = input_df[feature_columns]
    return input_df

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_data = request.form.to_dict()
        
        # Convert boolean-like string values to integers
        bool_fields = ['5g_support', 'dual_sim', 'expandable_storage', 'water_resistance', 
                      'wireless_charging', 'fingerprint_sensor', 'face_unlock']
        
        for field in bool_fields:
            if field in form_data:
                form_data[field] = int(form_data[field] == 'yes')
        
        input_df = preprocess_input(form_data)
        prediction = model.predict(input_df)[0]
        
        result = {
            'success': True,
            'predicted_price': round(float(prediction), 2),
            'formatted_price': f"₹{round(float(prediction), 2):,.2f}"
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/features')
def get_features():
    return jsonify({
        'categorical_features': categorical_cols,
        'categorical_options': {
            col: list(categorical_encoders[col].keys()) for col in categorical_cols if col in categorical_encoders
        },
        'numerical_features': [
            'launch_year', '5g_support', 'dual_sim', 'expandable_storage', 
            'water_resistance', 'wireless_charging', 'fingerprint_sensor', 
            'face_unlock', 'gpu_score', 'cpu_score', 'screen_to_body_ratio',
            'colors_available', 'warranty_years', 'bluetooth_version', 'ram_gb',
            'storage_gb', 'thickness_mm', 'refresh_rate_hz', 'battery_mah',
            'fast_charging_w', 'rear_camera_mp', 'front_camera_mp', 'weight_g'
        ]
    })

if __name__ == '__main__':
    load_model_and_encoders()
    app.run(debug=True, host='0.0.0.0', port=5000)