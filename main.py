from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import models
from database import engine
from routes import marketplace_routes

# Auto-create tables on startup if they do not exist.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WorkLocal Marketplace")
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.include_router(marketplace_routes.router, prefix="/api", tags=["marketplace"])


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/static/index.html")
