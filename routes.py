from flask import Blueprint, request, jsonify
from models import Log
from extensions import db
from log_parser import LogParser

api_routes = Blueprint("api", __name__)

@api_routes.route("/logs", methods=["GET"])
def get_logs():
    logs = Log.query.order_by(Log.created_at.desc()).all()
    return jsonify([
        {
            "id": l.id,
            "source_ip": l.source_ip,
            "event_type": l.event_type,
            "severity": l.severity,
            "created_at": l.created_at.isoformat() if l.created_at else None
        } for l in logs
    ])

@api_routes.route("/logs", methods=["POST"])
def add_log():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "Missing message"}), 400

    parsed = LogParser.parse(data["message"])
    new_log = Log(
        source_ip=parsed.get("source_ip"),
        destination_ip=parsed.get("destination_ip"),
        event_type=parsed.get("event_type"),
        severity=parsed.get("severity"),
        raw_message=parsed.get("raw_message"),
        parsed_data=parsed.get("parsed_data", {})
    )
    db.session.add(new_log)
    db.session.commit()
    return jsonify({"message": "log saved"}), 201