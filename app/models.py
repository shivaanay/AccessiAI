from datetime import datetime, timezone
from app import db

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_url = db.Column(db.String(2048), nullable=False)
    score = db.Column(db.Integer, nullable=False, default=0)
    violation_count = db.Column(db.Integer, nullable=False, default=0)
    summary_json = db.Column(db.Text, nullable=False, default='[]')
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
