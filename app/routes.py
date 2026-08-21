from flask import Blueprint, jsonify, render_template, request
from app.inference import predict_emotion

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Renders the main application homepage."""
    return render_template('index.html')

@main_bp.route('/detector')
def detector():
    """Renders the live webcam detection page."""
    return render_template('detector.html')

@main_bp.route('/api/predict', methods=['POST'])
def api_predict():
    """
    Receives a base64 image frame from the browser,
    runs the inference engine, and returns the emotion JSON.
    """
    data = request.get_json()
    
    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400
        
    try:
        base64_string = data['image']
        # Pass the image to our Inference Engine
        result = predict_emotion(base64_string)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return jsonify({"error": "Internal server processing error"}), 500

@main_bp.route('/api/health')
def health_check():
    """Simple diagnostic endpoint."""
    return jsonify({"status": "healthy"})