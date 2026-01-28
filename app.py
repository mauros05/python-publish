# ================
# Imports
# ================

# Flask
from flask import Flask, request, jsonify, render_template, redirect, url_for

# Env & Config
from dotenv import load_dotenv
from config.cloudinary import init_cloudinary
import cloudinary.uploader

# DB
from database import db
from flask_migrate import Migrate

# Models
from models.post import Post
from models.image import Image
from models.text import Text

# Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs import publish_pending_posts, generate_week_post

# Routes
from admin.texts import admin_texts
from admin.images import admin_images

# ================
# App config
# ================

# Llama variables de entorno
load_dotenv()

# Inicializa la app
app = Flask(__name__)

# Inicializa Cloudinary
init_cloudinary()
# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Se evitan los warnings

db.init_app(app)
migrate = Migrate(app, db)

# ================
# Routes
# ================

@app.route("/")
def home():
    return "python-publish working"

@app.route("/admin")
def admin_panel():
    return render_template("admin/layout.html")

app.register_blueprint(admin_texts)
app.register_blueprint(admin_images)

@app.route("/admin/posts")
def admin_posts():
    posts = Post.query.order_by(Post.publish_at.desc()).all()
    return render_template("admin/posts.html", posts=posts)

@app.route("/images/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    result = cloudinary.uploader.upload(
        file,
        folder="Super Tortas Tampico",
        resource_type="image"
    )

    image = Image(
        public_id=result["public_id"],
        url=result["secure_url"]
    )

    db.session.add(image)
    db.session.commit()

    return jsonify({
        "message": "Image uploaded",
        "id": image.id,
        "url": image.url
    }), 201


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
    print("Hola la app esta iniciada 👍")
    print("Scheduler started")
    app.run(port=5001)
