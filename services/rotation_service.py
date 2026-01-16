import random
from models.image import Image
from models.text import Text
from models.rotation_state import RotationState
from database import db

def get_next_image():
    images = Image.query.filter_by(active=True).order_by(Image.id).all()
    if not images:
        return None

    state = RotationState.query.first()
    if not state:
        state = RotationState()
        db.session.add(state)
        db.session.commit()

    if state.last_image_id is None:
        next_image = images[0]
    else:
        ids = [img.id for img in images]
        index = ids.index(state.last_image_id)
        next_image = images[(index + 1) % len(images)]

    state.last_image_id = next_image.id
    db.session.commit()

    return next_image

def get_random_text():
    texts = Text.query.filter_by(active=True).all()
    if not texts:
        return None

    state = RotationState.query.first()
    last_text_id = state.last_text_id if state else None

    available = [t for t in texts if t.id != last_text_id]
    if not available:
        available = texts

    text = random.choice(available)

    state.last_text_id = text.id
    db.session.commit()

    return text
