from fastapi import FastAPI
from app.api.routes.recommend import router

app = FastAPI(title="E-Commerce MAS API")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "API Running"}