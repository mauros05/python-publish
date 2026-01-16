from app import app
from database import db
from models.image import Image
from models.text import Text

with app.app_context():
    db.session.add_all([
        Image(path="uploads/images/barda_clasica_v1.png"),
        Image(path="uploads/images/barda_especia_v1.png"),
        Image(path="uploads/images/pierna_v1.png"),
        Image(path="uploads/images/ternera_v1.png"),
    ])

    db.session.add_all([
        Text(content="¡Las mejores tortas te esperan hoy!"),
        Text(content="Ven por tu torta favorita 🤤"),
        Text(content="Hoy es buen día para una torta 🌯"),
    ])

    db.session.commit()

    print("Sesion completado")
