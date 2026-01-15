from datetime import datetime
from models.post import Post
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
        print("Generando publicaciones de la semana...")

        post = Post(
            text="Post de prueba",
            image_path="image1.jpg",
            publish_at=datetime.utcnow(),
            platform="facebook"
        )

        db.session.add(post)
        db.session.commit()
