from app import app
from database import db
from models.image import Image
from models.text import Text
from models.rotation_state import RotationState

"""
Seed de desarrollo:
- Crea textos base
- Inicializa RotationState
- NO crea imágenes
- NO crea posts
"""

with app.app_context():
    db.session.add_all([
        Text(content="¡Las mejores tortas te esperan hoy!"),
        Text(content="Ven por tu torta favorita 🤤"),
        Text(content="Hoy es buen día para una torta 🌯"),
    ])
    print("Textos creados")

    if not RotationState.query.first():
        db.session.add(
            RotationState(
                last_image_index=0,
                last_text_id=None
            )
        )
        print("RotationState creado")
    else:
        print("RotationState ya existe")


    db.session.commit()

    print("Sesion completado")
