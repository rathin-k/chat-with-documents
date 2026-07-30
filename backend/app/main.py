from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Chat with Documents API!"}

@app.get("/health")
def health():
    return {"status": "running"}

@app.get("/about")
def about():
    return {
        "project": "Chat with Documents",
        "version": "1.0.0"
    }