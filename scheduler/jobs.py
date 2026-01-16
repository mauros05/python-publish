from services.rotation_service import get_next_image, get_next_text
from utils.schedule import generate_schedule
from datetime import datetime, date, timedelta
from models.post import Post
from models.rotation_state import RotationState
from database import db

def publish_pending_posts(app):
    # Permite acceder a la DB fuera de un request
    with app.app_context():
        now = datetime.utcnow()

        posts = Post.query.filter(
            Post.status == "pending",
            Post.publish_at <= now # Solo posts que ya deberian de publicarse
        ).all()

        for post in posts:
            print(f"Publicando post {post.id}...")
            post.status = "published" # Evita que se vuelva a ejecutar
            db.session.commit()

def generate_week_post(app):
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

        for publis_at in dates:
            image = get_next_image()
            text = get_next_text()

            if not image or not text:
                print("No hay imágenes o textos suficientes")
                return

            post = Post(
                image_id=image.id,
                text_id=text.id,
                publish_at=publis_at,
                platform="facebook"
            )

            db.session.add(post)

        state.last_generated_week = current_week
        db.session.commit()
        print("Publicaciones de la semana creada")
