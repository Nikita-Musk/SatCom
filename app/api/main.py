from fastapi import FastAPI

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