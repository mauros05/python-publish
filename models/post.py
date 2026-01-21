from database import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = "posts"

    id               = db.Column(db.Integer, primary_key=True)

    image_id         = db.Column(db.Integer, db.ForeignKey("images.id"))
    text_id          = db.Column(db.Integer, db.ForeignKey("texts.id"))

    publish_at       = db.Column(db.DateTime, nullable=False)
    status           = db.Column(db.String(20), default="pending")
    platform         = db.Column(db.String(20), default="facebook")
    facebook_post_id = db.Column(db.String(100), nullable=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    image            = db.relationship("Image")
    text             = db.relationship("Text")

    def __repr__(self):
        return f"<Post {self.id} - {self.status}>"
