"""
Custom wrapper for Elysia API - Separates backend from frontend serving
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import the original Elysia app
from elysia.api.app import app as elysia_app

# Import the lifespan and other necessary items
from elysia.api.app import lifespan

# Create our custom FastAPI app with the same lifespan
custom_app = FastAPI(
    title="Construction Co-Pilot API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware (same as original but ensuring all origins for development)
custom_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Copy all routes from the original app EXCEPT static file serving
for route in elysia_app.routes:
    # Skip static file routes and the root HTML route
    if (not route.path.startswith("/_next") and 
        not route.path.startswith("/static") and 
        route.path != "/" and
        route.path != "/{path:path}"):  # Skip catch-all routes
        custom_app.routes.append(route)

# Add our custom root endpoint for API info
@custom_app.get("/")
async def root():
    """Root endpoint - returns API information."""
    return {
        "name": "Construction Co-Pilot API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/health"
    }

# Future: Add custom SharePoint endpoints here
# @custom_app.post("/sharepoint/sync")
# async def sync_sharepoint(site_name: str):
#     """Sync SharePoint to Weaviate"""
#     from custom.sharepoint_tools import sync_sharepoint_to_weaviate
#     return await sync_sharepoint_to_weaviate(site_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("custom_app:custom_app", host="0.0.0.0", port=8000, reload=True)