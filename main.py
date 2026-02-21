from fastapi import FastAPI
from routes import posts, users

app = FastAPI()
app.include_router(users)
app.include_router(posts)

@app.get("/")
def rooter():
    return {"message": "FastAPI with multiple route files"}