# Python Publis 🚀

Sistema de publicación automatica de contenido (imágenes + textos) en redes sociales usando Flask y schedulers.

## 🧠 Características

- CRUD de imágenes y textos
- Rotación automática sin repetición
- Programación semanal de publicaciones
- Scheduler con APScheduler
- Publicación en Facebook e Instagram (Graph API)
- Base de datos SQLite
- Seeds iniciales

## ⚙️ Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## ▶️ Ejecutar

```bash
python app.py
```

## 🔐 Variables de entorno

```bash
# Facebook
FACEBOOK_PAGE_ID_TEST=<page_id>
FACEBOOK_PAGE_ACCESS_TEST=<page_access_token>

# Instagram (Instagram API with Facebook Login)
INSTAGRAM_ACCESS_TOKEN=<user_or_page_access_token_with_permissions>
INSTAGRAM_API_VERSION=v24.0
```

`INSTAGRAM_IG_USER_ID` es opcional si ya tienes `FACEBOOK_PAGE_ID_TEST`; se resuelve automáticamente desde la página conectada.

Para Instagram, la imagen debe ser una URL pública (por ejemplo, Cloudinary).

## 🧪 Seed de datos

```bash
python seed.py
```
