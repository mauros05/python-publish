# ================
# Imports
# ================

from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
from scheduler.jobs import publish_pending_posts, generate_week_post
from utils.schedule import generate_schedule

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

@app.route("/posts/schedule", methods=["POST"])
def create_scheduled_post():
    data = request.json

    dates = generate_schedule(
        days=data["days"],
        hour=data["hour"],
        total_posts=data.get("total_posts", 10)
    )

    created_post = []

    for date in dates:
        post = Post(
            text=data["text"],
            image_path=data["image_path"],
            publish_at=date,
            platform=data.get("platform", "facebook")
        )
        db.session.add(post)
        created_post.append(post)

    db.session.commit()

    return jsonify({
        "message": f"{len(created_post)} publicaciones creadas",
        "posts": [p.publish_at.isoformat() for p in created_post]
    })


# ================
# Scheculer
# ================

scheduler = BackgroundScheduler()

# Job 1: Publicar posts pendientes
scheduler.add_job(
    func=publish_pending_posts,
    trigger="interval",
    seconds=30,
    args=[app]
)


# Job 2: Generar posts de la semana (DOMINGO)
scheduler.add_job(
    func=generate_week_post,
    trigger="cron",
    day_of_week="sun",
    hour=9,
    args=[app]
)


# ================
# Run
# ================

if __name__== "__main__":
    scheduler.start()
    print("Scheduler started")
    app.run(debug=True, use_reloader=False)
