from services.rotation_service import get_next_image, get_next_text
from services.facebook_service import publish_to_facebook, FacebookPublishError
from utils.schedule import generate_schedule
from utils.time import now_utc_from_local
from datetime import datetime, date, timedelta
from models.post import Post
from models.rotation_state import RotationState
from database import db

def publish_pending_posts(app):
    """
    Publica automáticamente los posts pendientes cuya fecha de publicación
    ya ha sido alcanzada o superada.

    Esta función:
    - Se ejecuta fuera del contexto de una petición HTTP (scheduler).
    - Obtiene todos los posts con estado 'pending'.
    - Verifica si su fecha `publish_at` es menor o igual a la fecha actual.
    - Simula la publicación en Facebook mediante un mock.
    - Marca el post como 'published' para evitar que se publique nuevamente.
    - Guarda el ID devuelto por la plataforma simulada.
    """
    # Permite acceder a la DB fuera de un request
    with app.app_context():
        now = now_utc_from_local()

        posts = Post.query.filter(
            Post.status == "pending",
            Post.publish_at <= now # Solo posts que ya deberian de publicarse
        ).all()

        for post in posts:
            print(f"Publicando post {post.id}...")

            try:
                facebook_id = publish_to_facebook(
                    message=post.text.content,
                    image_url=post.image.url if post.image else None
                )

                post.status = "published" # Evita que se vuelva a ejecutar
                post.facebook_post_id = facebook_id
                db.session.commit()

                print(f"Post {post.id} publicado correctamente")
            except FacebookPublishError as e:
                print(f"Error Facebook en post {post.id}: {e}")

                post.status = "failed"
                post.error_message = str(e)
                db.session.commit
            except Exception as e:
                print(f"Error inesperado en post {post.id}: {e}")

                post.status = "failed"
                post.error_message = "Unexpected error"
                db.session.commit

def generate_week_post(app):
    """
    Genera automáticamente las publicaciones de la semana actual
    (lunes, miércoles y viernes a las 10:00 AM).

    Esta función:
    - Se ejecuta una vez por semana (domingo).
    - Verifica si ya se generaron publicaciones para la semana actual.
    - Obtiene la siguiente imagen y texto según la rotación definida.
    - Crea los posts con estado 'pending'.
    - Guarda la semana generada para evitar duplicados.
    """

    with app.app_context():
        state = RotationState.query.first()

        today = date.today()
        current_week = today - timedelta(days=today.weekday())

        if state and state.last_generated_week == current_week:
            print("Semana ya generada")
            return

        dates = generate_schedule(
            days=[0, 2, 4],
            hour=10,
            total_posts=3
        )

        for publish_at in dates:
            image = get_next_image()
            text = get_next_text()

            if not image or not text:
                print("No hay imágenes o textos suficientes")
                return

            post = Post(
                image_id=image.id,
                text_id=text.id,
                publish_at=publish_at,
                platform="facebook"
            )

            db.session.add(post)

        state.last_generated_week = current_week
        db.session.commit()
        print("Publicaciones de la semana creada")

def generate_week_post_test(app):
    """
    Genera publicaciones de prueba para validar la rotación de imágenes,
    textos y fechas sin depender del control semanal.

    Esta función:
    - No valida si la semana ya fue generada.
    - Siempre crea publicaciones nuevas.
    - Imprime información detallada en consola.
    - Se usa únicamente para desarrollo y testing.
    """
    with app.app_context():
        state = RotationState.query.first()
        if not state:
            state = RotationState()
            db.session.add(state)
            db.session.commit()

        print("⚙️ Generando posts de prueba...")

        dates = generate_schedule(
            days=[0, 2, 4],
            hour=10,
            total_posts=3
        )

        for publish_at in dates:
            image = get_next_image()
            text = get_next_text()

            post = Post(
                image_id = image.id,
                text_id = text.id,
                publish_at=publish_at,
                platform="facebook"
            )

            db.session.add(post)
            print(
                f"📌 Post -> image:{image.id} text:{text.id} "
                f"publish_at: {publish_at}"
            )

        db.session.commit()
        print("Post de prueba creados")
