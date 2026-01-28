from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from models.image import Image
from database import db

# Env & Config
from dotenv import load_dotenv
from config.cloudinary import init_cloudinary
import cloudinary.uploader

# Llama variables de entorno
load_dotenv()

# Inicializa Cloudinary
init_cloudinary()

admin_images = Blueprint("admin_images", __name__, url_prefix="/admin/images")

@admin_images.route("/")
def index():
    images = Image.query.all()
    return render_template("admin/images.html", images=images)

@admin_images.route("/<int:image_id>/toggle")
def toggle_image(image_id):
    image = Image.query.get_or_404(image_id)
    image.status = not image.status
    db.session.commit()

    return redirect(url_for("admin_images.index"))

@admin_images.route("/upload", methods=["POST"])
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
