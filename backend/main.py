from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login, register, upload, screenplay
from database import engine
from sqlalchemy import text
import os

app = FastAPI(title="CinemaShare API", version="1.0.0")


@app.on_event("startup")
def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS uploaded_files (
                file_id         SERIAL PRIMARY KEY,
                original_filename VARCHAR(255) NOT NULL,
                file_data       BYTEA NOT NULL,
                file_size       INT NOT NULL,
                content_type    VARCHAR(100),
                uploaded_by     INT NOT NULL,
                uploaded_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_revoked      BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS file_lines (
                line_id     SERIAL PRIMARY KEY,
                file_id     INT NOT NULL,
                line_number INT NOT NULL,
                content     TEXT NOT NULL,
                FOREIGN KEY (file_id) REFERENCES uploaded_files(file_id)
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS line_role_permissions (
                line_id     INT NOT NULL,
                role_name   VARCHAR(100) NOT NULL,
                PRIMARY KEY (line_id, role_name),
                FOREIGN KEY (line_id) REFERENCES file_lines(line_id)
            )
        """))
        conn.commit()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "CinemaShare API",
        "version": "1.0.0",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }

app.include_router(login.router, prefix="/api")
app.include_router(register.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(screenplay.router, prefix="/api")
