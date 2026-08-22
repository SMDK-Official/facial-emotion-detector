from datetime import datetime
from app import db

class DetectionHistory(db.Model):
    """Database table to store emotion detection sessions."""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    emotion = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Detection {self.emotion} - {self.confidence}%>"