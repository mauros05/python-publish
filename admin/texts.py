from flask import Blueprint, render_template, request, redirect, url_for
from models.text import Text
from database import db


admin_texts = Blueprint("admin_texts", __name__, url_prefix="/admin/texts")

@admin_texts.route("/")
def index():
    texts = Text.query.order_by(Text.created_at.desc()).all()
    return render_template("/admin/texts.html", texts=texts)

@admin_texts.route("/create", methods=["POST"])
def create():
    content = request.form.get("content")

    if not content or content.strip() == "":
        return redirect(url_for("admin_texts.index"))

    text = Text(content=content)
    db.session.add(text)
    db.session.commit()

    return redirect(url_for("admin_texts.index"))

@admin_texts.route("/<int:text_id>/toggle")
def toggle(text_id):
    text=Text.query.get_or_404(text_id)
    text.active = not text.active
    db.session.commit()

    return redirect(url_for("admin_texts.index"))
