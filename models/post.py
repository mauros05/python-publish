from database import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    publish_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")
    platform = db.Column(db.String(20), default="facebook")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def __repr__(self):
    return f"<Post {self.id} - {self.status}>"
