import os
from app import app
from database import db
from models.image import Image
import cloudinary.uploader
from config.cloudinary import init_cloudinary

IMAGE_FOLDER = "uploads/images"

def upload_images():
    init_cloudinary()

    with app.app_context():
        files = os.listdir(IMAGE_FOLDER)

        if not files:
            print("No hay imagenes en uploads/images")
            return

        for filename in files:
            file_path = os.path.join(IMAGE_FOLDER, filename)

            if not os.path.isfile(file_path):
                continue

            # Evita duplicados
            exists = Image.query.filter_by(public_id=filename).first()
            if exists:
                print(f"Ya existe: {filename}")
                continue


            print(f"Subiendo {filename} a Cloudinay...")

            result = cloudinary.uploader.upload(
                file_path,
                folder="Super Tortas Tampico"
            )

            image = Image(
                public_id=result["public_id"],
                url=result["secure_url"]
            )

            db.session.add(image)
            db.session.commit()

            print(f"Imagen guardada: {result['public_id']}")


if __name__=="__main__":
    upload_images()
