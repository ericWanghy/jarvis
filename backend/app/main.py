import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s"
)

from flask import Flask
from flask_cors import CORS
from app.core.config import settings
from app.core.database import init_db
from app.core.scheduler import init_scheduler
from app.api.v1.router import api_blueprint
from app.api.v1.prompts import prompts_bp
from app.api.v1.memories import memories_bp
from app.api.v1.sessions import sessions_bp
from app.api.v1.reminders import reminders_bp
import app.models.sql  # Import models to register them with Base

def create_app() -> Flask:
    app = Flask(__name__)

    # Enable CORS for frontend communication
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Database
    init_db()

    # Initialize Background Scheduler
    # Only init scheduler if not in debug reloader (to avoid double scheduler)
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or settings.ENV == "production":
         init_scheduler()

    # Register Blueprints
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")
    app.register_blueprint(prompts_bp, url_prefix="/api/v1/prompts")
    app.register_blueprint(memories_bp, url_prefix="/api/v1/memories")
    app.register_blueprint(sessions_bp, url_prefix="/api/v1/sessions")
    app.register_blueprint(reminders_bp, url_prefix="/api/v1/reminders")

    @app.route("/health")
    def health_check():
        return {"status": "ok", "version": "5.6.0", "app": settings.APP_NAME}

    return app
