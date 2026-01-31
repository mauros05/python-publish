from flask import Blueprint, render_template, request, redirect, url_for
from models.post import Post
from models.image import Image
from models.text import Text
from datetime import datetime
from database import db

admin_posts = Blueprint("admin_posts", __name__, url_prefix="/admin/posts")

@admin_posts.route("/")
def index():
    posts = Post.query.order_by(Post.publish_at.asc()).all()
    images = Image.query.filter_by(status=True).all()
    texts = Text.query.filter_by(active=True).all()

    return render_template("admin/posts.html", posts=posts, texts=texts, images=images)

@admin_posts.route("/create", methods=["POST"])
def create():
    text_id = request.form["text_id"]
    image_id = request.form["image_id"]
    publish_at_str = request.form["publish_at"]
    publish_at = datetime.fromisoformat(publish_at_str)

    post = Post(
        text_id=text_id,
        image_id=image_id,
        publish_at=publish_at,
        status="pending"
    )

    db.session.add(post)
    db.session.commit()

    return redirect(url_for("admin_posts.index"))

@admin_posts.route("/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    texts = Text.query.filter_by(active=True).all()
    images = Image.query.filter_by(status=True).all()

    if request.method == "POST":
        post.text_id = request.form.get("text_id")
        post.image_id = request.form.get("image_id")

        publish_at_str = request.form.get("publish_at")
        if publish_at_str:
            post.publish_at = datetime.fromisoformat(publish_at_str)

        db.session.commit()
        return redirect(url_for("admin_posts.index"))

    return render_template(
        "admin/posts_edit.html",
        post=post,
        texts=texts,
        images=images
    )

@admin_posts.route("/<int:post_id>/delete", methods=["POST"])
def delete(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("admin_posts.index"))
