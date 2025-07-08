from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.movies_routes import router as movies_router
from routes.reviews_routes import router as reviews_router
from routes.auth_routes import router as auth_router


app = FastAPI(title="MovieMesh API", docs_url="/api/docs", openapi_url="/api/openapi.json")

# Include routers
app.include_router(movies_router, prefix="/api/movies", tags=["movies"])
app.include_router(reviews_router, prefix="/api/movies", tags=["reviews"])
app.include_router(auth_router, prefix="/api", tags=["auth"])

# Allow front-end JS served by same host
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ───────────────────────── STATIC FRONTEND ─────────────────────
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
