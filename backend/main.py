from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import login, register

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="/api")
app.include_router(register.router, prefix="/api")
