import os
from flask import Blueprint, jsonify, render_template, request
from app.inference import predict_emotion
from app.models import DetectionHistory
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/history')
def history():
    records = DetectionHistory.query.order_by(DetectionHistory.timestamp.desc()).all()
    return render_template('history.html', records=records)

@main_bp.route('/about')
def about():
    return render_template('about.html')

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
        return jsonify({"error": str(e)}), 500

@main_bp.route('/api/save', methods=['POST'])
def api_save():
    """Stores a finalized emotion session and image snapshot into SQLite."""
    data = request.get_json()
    if not data or 'emotion' not in data or 'confidence' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    try:
        new_record = DetectionHistory(
            emotion=data['emotion'],
            confidence=float(data['confidence']),
            image_data=data.get('image', '') # Catches the picture sent from JS
        )
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"status": "success", "message": "Record saved successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to save record"}), 500