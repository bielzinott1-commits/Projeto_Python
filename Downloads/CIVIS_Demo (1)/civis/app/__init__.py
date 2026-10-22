import os
from pathlib import Path
from flask import Flask, render_template
from .config import Config
from .extensions import db, login_manager, csrf

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .auth import bp as auth_bp
    from .main import bp as main_bp
    from .occurrences import bp as occurrences_bp
    from .apprehensions import bp as apprehensions_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(occurrences_bp, url_prefix="/ocorrencias")
    app.register_blueprint(apprehensions_bp, url_prefix="/apreensoes")

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    return app
