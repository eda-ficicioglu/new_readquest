# app/__init__.py

from flask import Flask
import os


def create_app():
    # Uygulamayı oluştur
    app = Flask(__name__)

    # --- DÜZELTME BURADA ---
    # config.py dosyasının tam yolunu (absolute path) oluşturuyoruz.
    # app.root_path, 'app' klasörünün yolunu verir. '..' ile bir üst dizine çıkarak
    # 'config.py' dosyasını buluruz. Bu, en güvenilir yöntemdir.
    config_path = os.path.join(app.root_path, '..', 'config.py')
    app.config.from_pyfile(config_path)

    # Blueprint'i uygulamaya kaydet
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app