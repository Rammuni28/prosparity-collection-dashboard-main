from fastapi import FastAPI
from app.api.v1 import user
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import application
from app.api.v1 import collections

app = FastAPI(title="PROSPARITY API")

# CORS for Postman/local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(application.router, prefix="/api/v1/application", tags=["application"])
app.include_router(collections.router, prefix="/api/v1/collections", tags=["collections"])

@app.get("/")
def root():
    return {"message": "PROSPARITY API is running"} 