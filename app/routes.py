from flask import Blueprint, jsonify, render_template, request
from app.inference import predict_emotion
from app.models import DetectionHistory
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/detector')
def detector():
    return render_template('detector.html')

@main_bp.route('/history')
def history():
    """Fetches all past detections and renders the history page."""
    # Read all records from the database, sorted by newest first
    records = DetectionHistory.query.order_by(DetectionHistory.timestamp.desc()).all()
    return render_template('history.html', records=records)

@main_bp.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400
    try:
        base64_string = data['image']
        result = predict_emotion(base64_string)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Internal server processing error"}), 500

@main_bp.route('/api/save', methods=['POST'])
def api_save():
    """Saves a finalized emotion result to the SQLite database."""
    data = request.get_json()
    if not data or 'emotion' not in data or 'confidence' not in data:
        return jsonify({"error": "Missing data"}), 400
        
    try:
        new_record = DetectionHistory(
            emotion=data['emotion'],
            confidence=float(data['confidence'])
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"status": "success", "message": "Saved to database"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error"}), 500