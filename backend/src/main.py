from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.movies_routes import router as movies_router
from routes.reviews_routes import router as reviews_router
from routes.auth_routes import router as auth_router
from routes.users_routes import router as users_router
from routes.actors_routes import router as actors_router

app = FastAPI(title="MovieMesh API", docs_url="/api/docs", openapi_url="/api/openapi.json")

# Include routers
app.include_router(movies_router, prefix="/api/movies", tags=["movies"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["reviews"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(actors_router, prefix="/api/actors", tags=["actors"])

# Allow front-end JS served by same host
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# ───────────────────────── STATIC FRONTEND ─────────────────────
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
