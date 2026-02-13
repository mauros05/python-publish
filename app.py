# ================
# Imports
# ================

# Flask
from flask import Flask, render_template

# DB
from database import db
from flask_migrate import Migrate

# Scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.jobs import publish_pending_posts, generate_week_post

# Routes
from admin.texts import admin_texts
from admin.images import admin_images
from admin.posts import admin_posts

# Env & Config
from dotenv import load_dotenv
from config.cloudinary import init_cloudinary

# Test
from services.facebook_service import publish_to_facebook

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

@app.route("/test/facebook-post")
def publish_facebook_post():
    result = publish_to_facebook(
        "Post de prueba con token largo e imagen y prueba 2",
        "https://res.cloudinary.com/ddyzsltco/image/upload/v1769553836/Super%20Tortas%20Tampico/do1rpvok0mqif3htg4vp.png"
        )

    return result

app.register_blueprint(admin_texts)
app.register_blueprint(admin_images)
app.register_blueprint(admin_posts)

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
    print("Hola, la app esta iniciada 👍")
    print("Scheduler started")
    app.run(port=5001)
