from datetime import datetime
from database import db
from models.post import Post
from utils.schedule import generate_schedule
from services.rotation_service import get_next_image, get_random_text

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
        print("Generando publicaciones de la semana...")

        dates = generate_schedule(
            days=[0, 2, 4],
            hour=10,
            total_posts=3
        )

        for date in dates:
            image = get_next_image()
            text = get_random_text()

            if not image or not text:
                print("No hay imágenes o textos suficientes")
                return

            post = Post(
                text=text.content,
                image_path=image.path,
                publish_at=date,
                platform="facebook"
            )

            db.session.add(post)

        db.session.commit()
        print("Publicaciones de la semana creada")
