import random
from models.image import Image
from models.text import Text
from models.rotation_state import RotationState
from database import db

def get_rotation_state():
    """
    Obtiene el estado de rotación de contenidos.

    Busca el primer registro de `RotationState` en la base de datos.
    Si no existe, crea uno nuevo, lo guarda y lo retorna.

    Esta función garantiza que siempre exista un estado de rotación
    disponible para controlar la generación de publicaciones
    (por ejemplo, la última semana generada).
    """
    state = RotationState.query.first()
    if not state:
        state = RotationState()
        db.session.add(state)
        db.session.commit()
    return state

def get_next_image():
    """
    Devuelve la siguiente imagen activa usando rotación circular.
    Actualiza el índice en RotationState.
    """
    images = Image.query.filter_by(status=True).order_by(Image.id).all()
    if not images:
        return None

    state = get_rotation_state()

    image = images[state.last_image_index % len(images)]
    state.last_image_index += 1

    db.session.commit()
    return image

def get_next_text():
    """
    Devuelve el siguiente texto activo usando un metodo al azar.
    Actualiza el índice en RotationState.
    """
    texts = Text.query.filter_by(active=True).all()
    if not texts:
        return None

    state = get_rotation_state()

    available = [t for t in texts if t.id != state.last_text_id]
    text = random.choice(available or texts)

    state.last_text_id = text.id
    db.session.commit()

    return text
