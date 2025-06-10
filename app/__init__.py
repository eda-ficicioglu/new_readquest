# app/__init__.py

from flask import Flask

def create_app():
    # 1. instance_relative_config=True parametresini ekleyin.
    # Bu, Flask'in projenin kök dizinindeki 'instance' klasörünü tanımasını sağlar.
    app = Flask(__name__, instance_relative_config=True)

    # 2. Yapılandırmayı 'instance' klasöründen yükle.
    # Flask, 'config.py' dosyasını otomatik olarak instance klasöründe arayacaktır.
    # Başına yol (path) eklemenize gerek yoktur.
    app.config.from_pyfile('config.py')
    
    # 3. Blueprint'i uygulamaya kaydet (Bu kısım aynı kalır)
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
