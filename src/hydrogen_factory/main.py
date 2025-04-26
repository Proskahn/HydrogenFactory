from fastapi import FastAPI
from hydrogen_factory.api.router import api_router

app = FastAPI(
    title="HydrogenFactory Control API",
    description="API for controlling a hydrogen production factory",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the HydrogenFactory Control API"}