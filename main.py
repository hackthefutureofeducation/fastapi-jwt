from fastapi import FastAPI
from routes import users

app = FastAPI()
app.include_router(users)

@app.get("/")
def rooter():
    return {"message": "FastAPI with multiple route files"}