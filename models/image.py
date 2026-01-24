from database import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = "images"

    id         = db.Column(db.Integer, primary_key=True)

    public_id  = db.Column(db.String(255), nullable=False)
    url        = db.Column(db.Text, nullable=False)
    status     = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Image {self.id} - {self.path}>"
