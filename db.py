from app import app
from extensions import db
from models import Log, ThreatAlert

with app.app_context():
    db.create_all()
    print("Database created successfully")