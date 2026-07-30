from fastapi import FastAPI

from app.api.health import router as health_router

app = FastAPI()

app.include_router(health_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Chat with Documents API!"
    }