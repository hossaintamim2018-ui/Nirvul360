"""
nirvul360 Python Backend Runner
Runs FastAPI with Uvicorn on port 8000
"""
import sys
import os
from pathlib import Path
import uvicorn
from dotenv import load_dotenv

backend_dir = Path(__file__).resolve().parent
root_dir = backend_dir.parent

# Load .env from root or backend directory
env_path = root_dir / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    load_dotenv(dotenv_path=backend_dir / ".env", override=True)

# Ensure backend is in pythonpath
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting nirvul360 Python Backend on http://localhost:{port}")
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False, app_dir=str(backend_dir))
