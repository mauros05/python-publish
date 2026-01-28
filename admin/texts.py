from flask import Blueprint, render_template, request, redirect, url_for
from models.text import Text
from database import db


admin_texts = Blueprint("admin_texts", __name__)

@admin_texts.route("/admin/texts")
def index():
    texts = Text.query.all()
    return render_template("/admin/texts.html", texts=texts)


@admin_texts.route("/admin/texts/create", methods=["POST"])
def create():
    content = request.form["content"]

    text = Text(content=content)
    db.session.add(text)
    db.session.commit()

    return redirect(url_for("admin_texts.index"))

@admin_texts.route("/admin/texts/<int:text_id>/toggle")
def toggle(text_id):
    text=Text.query.get_or_404(text_id)
    text.active = not text.active
    db.session.commit()

    return redirect(url_for("admin_texts.index"))
