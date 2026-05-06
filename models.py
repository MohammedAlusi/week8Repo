from extensions import db
from datetime import datetime

class Log(db.Model):
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    source_ip = db.Column(db.String(45), index=True)
    destination_ip = db.Column(db.String(45))
    event_type = db.Column(db.String(50), index=True)
    severity = db.Column(db.String(20), index=True)
    raw_message = db.Column(db.Text)
    parsed_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    alerts = db.relationship("ThreatAlert", backref="log", lazy=True)


class ThreatAlert(db.Model):
    __tablename__ = "threat_alerts"

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("logs.id"))
    threat_type = db.Column(db.String(50))
    threat_score = db.Column(db.Float)
    description = db.Column(db.Text)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)