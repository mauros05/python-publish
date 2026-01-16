from database import db
from datetime import datetime, date

class RotationState(db.Model):
    __tablename__ = "rotation_state"

    id = db.Column(db.Integer, primary_key=True)

    last_image_index = db.Column(db.Integer, default=0)
    last_text_id = db.Column(db.Integer, nullable=True)

    last_generated_week = db.Column(db.Integer, nullable=True)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<RotationState image={self.last_image_index} "
            f"text={self.last_text_id}>"
            f"week={self.last_generated_week}"
        )
