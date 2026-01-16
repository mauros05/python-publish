import random
from models.image import Image
from models.text import Text
from models.rotation_state import RotationState
from database import db

def get_rotation_state():
    state = RotationState.query.first()
    if not state:
        state = RotationState()
        db.session.add(state)
        db.session.commit()
    return state

def get_next_image():
    images = Image.query.filter_by(active=True).order_by(Image.id).all()
    if not images:
        return None

    state = get_rotation_state()

    image = images[state.last_image_index % len(images)]
    state.last_image_index += 1

    db.session.commit()
    return image

def get_next_text():
    texts = Text.query.filter_by(active=True).all()
    if not texts:
        return None

    state = get_rotation_state()

    available = [t for t in texts if t.id != state.last_text_id]
    text = random.choice(available or texts)

    state.last_text_id = text.id
    db.session.commit()

    return text
