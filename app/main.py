import os
from fastapi import FastAPI

DATABASE_URL = (
    f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
    f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
)

app = FastAPI(title="SatCom API", version="0.1.0")

@app.get("/")
def root():
    return {"message": "SatCom API is running successfully!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/satellites")
def list_satellites():
    return {"satellites": []}  # потом добавите данные