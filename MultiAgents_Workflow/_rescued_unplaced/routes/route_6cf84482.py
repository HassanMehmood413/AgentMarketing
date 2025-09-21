from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import engine,Base

from .routes.research_adapter import router as research_router
from .routes.writer_adapter import router as writer_router
from .routes.auth import router as auth_router
from .routes.frontend_api import router as frontend_api_router

app = FastAPI(
    title="Multi-Agent Research Platform",
    description="AI-powered research and reporting platform using Coral Protocol",
    version="1.0.0",
    tags=["Agent Backend (LangGraph x Coral)"]
)

# CORS for frontend connections (Next.js, React, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000","http://localhost:8080","*"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    print("TABLE CREATING")
    try:
        Base.metadata.create_all(bind=engine)
        print("TABLES CREATED")
    except Exception as e:
        print(e)
        raise HTTPException(status_code='500',detail="TABLES NOT CREATED")

@app.get("/health")
def health():
    return {"ok": True}

# Mount all API routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(frontend_api_router, prefix="/api/v1", tags=["Frontend API"])
app.include_router(research_router, prefix="/agents/research")
app.include_router(writer_router,   prefix="/agents/writer")