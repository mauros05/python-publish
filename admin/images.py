from flask import Blueprint, render_template, request, redirect, url_for
from models.image import Image
from database import db

admin_images = Blueprint("admin_images", __name__)

@admin_images.route("/admin/images")
def index():
    images = Image.query.all()
    return render_template("admin/images.html", images=images)

@admin_images.route("/admin/images/<int:image_id>/toggle")
def toggle_image(image_id):
    image = Image.query.get_or_404(image_id)
    image.status = not image.status
    db.session.commit()

    return redirect(url_for("admin_images.index"))
