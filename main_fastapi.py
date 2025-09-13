from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.wsgi import WSGIMiddleware

# Import the existing Flask app
from app import app as flask_app

app = FastAPI(title="EdVise (FastAPI gateway)")


@app.get("/api/health")
def health():
    return JSONResponse({"status": "ok"})


# Mount the Flask app at root so all existing routes and templates continue working
app.mount("/", WSGIMiddleware(flask_app))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_fastapi:app", host="0.0.0.0", port=8000, reload=True)
