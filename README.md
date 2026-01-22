# Python Publis 🚀

Sistema de publicación automatica de contenido (imágenes + textos) en redes sociales usando Flask y schedulers.

## 🧠 Características

- CRUD de imágenes y textos
- Rotación automática sin repetición
- Programación semanal de publicaciones
- Scheduler con APScheduler
- Publicación mock (Facebook API simulada)
- Base de datos SQLite
- Seeds iniciales

## ⚙️ Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Ejecutar
python app.py

## Seed de datos
python seed.py
