from app.main import create_app
from app.core.config import settings

app = create_app()

if __name__ == "__main__":
    # Running with standard Flask development server for now
    # In production/sidecar mode, we might use a production server wrapper
    print(f"Starting Jarvis Backend on port {settings.PORT}...")
    app.run(host=settings.HOST, port=settings.PORT, debug=True)
