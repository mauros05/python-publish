from app import app
from models.post import Post
from database import db
from datetime import datetime, timedelta

def prepare_post():
    with app.app_context():
        post = (
            Post.query
            .filter_by(status="pending")
            .order_by(Post.publish_at)
            .first()
        )

        if not post:
            print("No hay post pendientes")
            return

        post.publish_at = datetime.now() - timedelta(minutes=1)
        db.session.commit()

        print(f"Post {post.id} listo para publicación")

if __name__=="__main__":
    prepare_post()
