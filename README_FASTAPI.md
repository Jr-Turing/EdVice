# FastAPI Migration Guide

This repository currently uses Flask. This guide introduces an incremental path to migrate to FastAPI while keeping the site working.

## What’s included

- `main_fastapi.py`: FastAPI entrypoint that mounts the existing Flask app via WSGIMiddleware.
- `/api/health`: Native FastAPI endpoint to verify server.
- Dependencies added: `fastapi`, `uvicorn`.

## Run the FastAPI gateway (Windows PowerShell)

```pwsh
# From repo root
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"

# Install deps (prefer your venv)
pip install -r requirements.txt

# Run FastAPI (serves native /api routes and mounts Flask at /)
python -m uvicorn main_fastapi:app --reload --host 0.0.0.0 --port 8000
```

Then open:
- Health check: http://localhost:8000/api/health
- Existing site (Flask, mounted): http://localhost:8000/

## Phased migration plan

1) Boot via FastAPI (done)
- Keep the Flask app mounted at `/` so everything continues to work.
- Add new FastAPI-native endpoints under `/api/*` as you go.

2) Database layer
- Today: Models use `Flask-SQLAlchemy (db.Model)`.
- Target: Plain SQLAlchemy with a shared `Base`, `engine`, and `SessionLocal`.
- Steps:
  - Extract a `database.py` with `engine` and `SessionLocal` (using `DATABASE_URL`).
  - Convert models to inherit from a shared `Base` (Declarative Base) instead of `db.Model`.
  - Replace `db.session` calls with session dependencies in FastAPI.

3) Templates + static
- FastAPI supports Jinja2 via `fastapi.templating.Jinja2Templates`.
- Mount static files via `StaticFiles`.
- Port pages gradually: for each Flask route that `render_template`, add a FastAPI route returning `TemplateResponse`.

4) Auth & sessions
- Flask-Login → choose a FastAPI-friendly approach:
  - Cookie sessions with `itsdangerous` and Starlette middleware, or
  - JWT (e.g., `OAuth2PasswordBearer`) and front-end auth, or
  - `fastapi-users` package for batteries-included flows.
- Migrate endpoints that require `@login_required` to FastAPI dependencies.

5) Blueprints → Routers
- Replace Flask blueprints with FastAPI routers (`APIRouter`).
- Keep route paths and handler logic similar to minimize breakage.

6) Decommission Flask
- Once all routes (HTML and API) are in FastAPI and models use plain SQLAlchemy sessions, remove Flask and Flask-SQLAlchemy.

## Notes
- While the Flask app is mounted, any existing functionality remains accessible and stable.
- Add new capabilities in FastAPI first, then migrate existing endpoints.
- If you want me to start converting a specific route (e.g., `/college-finder`) to native FastAPI now, I can scaffold it with templates, pagination, and filters.
