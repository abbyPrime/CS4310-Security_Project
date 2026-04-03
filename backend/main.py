from fastapi import FastAPI
from routers import login, register

app = FastAPI()

app.include_router(login.router, prefix="/api")
app.include_router(register.router, prefix="/api")
