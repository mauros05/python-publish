# ================
# Imports
# ================

from flask import Flask, request, jsonify
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs import publish_pending_posts

from database import db
from models.post import Post

# ================
# App config
# ================

app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Se evitan los warnings

db.init_app(app)

with app.app_context(): # Necesario para operaciones de DB
    db.create_all()     # Crea la base de datos y tablas


# ================
# Routes
# ================

@app.route("/")
def home():
    return "python-publish working"


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.json # Lee el JSON que mandas desde el cliente

    post = Post(
            text=data["text"],
            image_path=data["image_path"],
            publish_at=datetime.fromisoformat(data["publish_at"]),
            platform=data.get("platform", "facebook")
        ) # Creamos el objeto con la info basica.

    # Guarda en SQLite
    db.session.add(post)
    db.session.commit()

    return jsonify({
        "message": "Publicacion creada",
        "post_id": post.id
    }), 201

@app.route("/posts", methods=["GET"])
def list_posts():
    posts = Post.query.all()

    return jsonify([
        {
            "id": p.id,
            "text": p.text,
            "image_path": p.image_path,
            "publish_at": p.publish_at.isoformat(),
            "status": p.status,
            "platform": p.platform
        }
        for p in posts
    ])




# ================
# Scheculer
# ================

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=publish_pending_posts,
    trigger="interval",
    seconds=30,
    args=[app]
)

scheduler.start()

# ================
# Run
# ================

if __name__== "__main__":
    app.run(debug=True)
