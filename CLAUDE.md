# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚀 Build & Development

### Setup
- **Prerequisites:** Python 3.10+, Node.js, Rust/Cargo
- **Initial Setup (recommended):**
  - From repo root: `./start_dev.sh`
    - Sets up the Python virtualenv
    - Installs backend + frontend dependencies
    - Starts backend and frontend together for local development
- **Environment Layout:**
  - Backend venv: `backend/venv`
  - Frontend dependencies: `frontend/node_modules`
- **Secrets:**
  - Copy `backend/.env.example` to `backend/.env` and fill in your API keys.

### Backend (Python/Flask)
- **Directory:** `backend/`
- **Install Dependencies (manual):**
  - `python -m venv venv`
  - `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
  - `pip install -r requirements.txt`
- **Run Server:**
  - `python run.py`
    - Flask API on `http://127.0.0.1:3721`.
- **Lint:**
  - `ruff check .`
- **Type Check:**
  - `mypy .`
- **Testing:**
  - Run all tests: `pytest`
  - Run single file: `pytest tests/test_api.py`
  - Run single test: `pytest tests/test_api.py::test_health_check`
- **Production Build (backend binary):**
  - From `backend/`: `pyinstaller backend.spec`
    - Output in `dist/backend`.

### Frontend (Tauri/React)
- **Directory:** `frontend/`
- **Install Dependencies:**
  - `npm install`
- **Run Dev:**
  - `npm run tauri dev`
    - Launches Tauri app (React SPA in webview, dev port 1420).
- **Build:**
  - Web assets: `npm run build`
  - Desktop app: `npm run tauri build`

### Production Build (Combined)
- **Backend Binary:**
  - Ensure `pyinstaller backend.spec` has been run and the binary is available.
- **Frontend/App:**
  - Place the backend binary under `frontend/src-tauri/binaries/` with the correct platform-specific suffix.
  - From `frontend/`: `npm run tauri build`.

---

## 🏗 Architecture

### High-Level Overview
Jarvis v5.6-proxy is a **desktop AI assistant** using a sidecar architecture:
- **Frontend:** React SPA (Vite + TypeScript + Mantine UI) hosted in a Tauri (Rust) webview.
- **Backend:** Python Flask REST API running on `127.0.0.1:3721`.
- **Communication:** HTTP/REST over localhost plus SSE for streaming chat responses.
- **Lifecycle:** The Tauri shell manages the backend process as a sidecar.

### Backend Structure
_Main package: `backend/app/`_

- **Core / Brain Pipeline** (`backend/app/core/brain/`):
  - `orchestrator.py`: Central coordinator. Handles intent classification (regex), prompt assembly, model selection, and streaming response generation.
  - `context.py`: Builds conversation context (history + short-term memory) for LLM calls.
- **LLM Integration** (`backend/app/core/llm_providers.py`):
  - Unified provider layer supporting `generate_stream` (SSE) and multimodal input.
  - Supports Gemini (internal), GPT-5 (internal), and Qwen (public).
- **Services Layer** (`backend/app/core/services/`):
  - Encapsulates domain logic for Memory, Reminder, Calendar, Reflection, etc.
  - API routes call into these services; they interact with DB and external systems.
- **Configuration** (`backend/app/core/config.py`):
  - Pydantic v2 settings. **Secrets must be loaded from environment variables (.env).**
- **Database** (`backend/app/core/database.py` + `backend/app/models/sql.py`):
  - SQLAlchemy setup targeting SQLite at `backend/storage/jarvis.db`.
  - Uses `get_db_session()` context manager for safe transaction handling.
- **Scheduler** (`backend/app/core/scheduler.py`):
  - APScheduler for background tasks (reminders, daily reflections).
- **API Layer** (`backend/app/api/v1/`):
  - `router.py`: Main chat endpoints (streaming).
  - `reminders.py`, `memories.py`, `sessions.py`, `prompts.py`: Feature-specific REST endpoints.
  - All endpoints return standardized `{success, data, error}` envelope (except chat stream).

### Frontend Structure
_Main package: `frontend/src/`_

- **Application Shell**:
  - `App.tsx`: Main application component (navigation, layout wiring).
  - `main.tsx`: React entry point.
- **API Layer**:
  - `api/client.ts`: Centralized API client with type-safe methods (`apiGet`, `apiPost`, etc.).
- **Pages & Features**:
  - `components/chat/…`: Chat UI and streaming display.
  - `components/reminders/…`: Reminder dashboard (decomposed into sub-components).
  - `components/memories/…`: Memory browsing and search.
  - `components/prompts/…`: Prompt templates management.
  - `components/settings/…`: Settings & configuration UI.
- **State / Context**:
  - `context/ChatContext.tsx`: Chat/session state.
  - `context/SettingsContext.tsx`: User settings and preferences.

---

## 📝 Coding Guidelines & Conventions

- **Path Handling:**
  - Use `pathlib.Path` for all filesystem paths and operations in Python.

- **Type Safety:**
  - Python: Add full type hints; keep `mypy` passing.
  - TypeScript: Use strict types and explicit interfaces for API responses.

- **Security:**
  - **NEVER hardcode secrets.** Use `backend/app/core/config.py` which loads from `.env`.
  - Use `get_db_session()` context manager for all DB operations to ensure rollback/cleanup.

- **Logging:**
  - Use `import logging` and `logger.info/error`. **Do NOT use `print()`.**

- **API Standards:**
  - Return `api_success(data)` or `api_error(message)` from `app.api.response`.
  - Frontend should use `api/client.ts` methods.

These guidelines are intended to help future Claude Code sessions quickly become productive while respecting the existing architecture and conventions of Jarvis v5.6-proxy.
