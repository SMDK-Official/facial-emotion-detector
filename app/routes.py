from flask import Blueprint, jsonify, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/api/health')
def health_check():
    """Simple diagnostic endpoint to verify backend status."""
    return jsonify({
        "status": "healthy",
        "service": "Facial Emotion Detection API",
        "version": "1.0.0"
    })