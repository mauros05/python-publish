from database import db

class RotationState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_image_id = db.Column(db.Integer, nullable=True)
    last_text_id = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return (
            f"<RotationState image={self.last_image_id} "
            f"text={self.last_text_id}>"
        )
