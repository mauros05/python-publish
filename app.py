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

@app.route("/admin/images")
def admin_images():
    images = Image.query.all()
    return render_template("admin/images.html", images=images)

@app.route("/admin/images/<int:image_id>/toggle")
def toggle_image(image_id):
    image = Image.query.get_or_404(image_id)
    image.status = not image.status
    db.session.commit()
    return redirect(url_for("admin_images"))

@app.route("/admin/texts")
def admin_texts():
    texts = Text.query.all()
    return render_template("/admin/texts.html", texts=texts)

@app.route("/admin/texts/<int:text_id>/toggle")
def toggle_text(text_id):
    text = Text.query.get_or_404(text_id)
    text.active = not text.active
    db.session.commit()
    return redirect(url_for("admin_texts"))

@app.route("/admin/posts")
def admin_posts():
    posts = Post.query.order_by(Post.publish_at.desc()).all()
    return render_template("admin/posts.html", posts=posts)

@app.route("/posts", methods=["GET"])
def list_posts():
    posts = Post.query.all()

    return jsonify([
        {
            "id": p.id,
            "publish_at": p.publish_at.isoformat(),
            "status": p.status,
            "platform": p.platform,
            "image_path": p.image_path if p.image else None,
            "text": p.text if p.text else None
        }
        for p in posts
    ])

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

@app.route("/images", methods=["GET"])
def list_images():
    images = Image.query.filter_by(status=True).all()

    return jsonify([
        {
            "id": img.id,
            "path": img.url
        }
        for img in images
    ])

@app.route("/texts", methods=["POST"])
def create_text():
    data = request.json

    text = Text(
        content=data["content"]
    )

    db.session.add(text)
    db.session.commit()

    return jsonify({
        "message": "Texto creado",
        "id": text.id
    }), 201

@app.route("/texts", methods=["GET"])
def list_texts():
    texts = Text.query.filter_by(active=True).all()

    return jsonify([
        {
            "id": txt.id,
            "content": txt.content
        }
        for txt in texts
    ])

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
