from app import app
from database import db
from models.image import Image
from models.text import Text
from models.rotation_state import RotationState

with app.app_context():
    db.session.add_all([
        Image(path="uploads/images/barda_clasica_v1.png"),
        Image(path="uploads/images/barda_especia_v1.png"),
        Image(path="uploads/images/pierna_v1.png"),
        Image(path="uploads/images/ternera_v1.png"),
    ])
    print("Path de imagenes creadas")

    db.session.add_all([
        Text(content="¡Las mejores tortas te esperan hoy!"),
        Text(content="Ven por tu torta favorita 🤤"),
        Text(content="Hoy es buen día para una torta 🌯"),
    ])
    print("Textos creados")

    if not RotationState.query.first():
        db.session.add(
            RotationState(
                last_image_index=None,
                last_text_id=None
            )
        )
        print("RotationState creado")
    else:
        print("RotationState ya existe")


    db.session.commit()

    print("Sesion completado")
