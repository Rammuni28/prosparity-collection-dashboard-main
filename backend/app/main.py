from fastapi import FastAPI
from app.api.v1.routes import user
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import application
from app.api.v1.routes import summary_status

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
app.include_router(summary_status.router, prefix="/api/v1/summary_status", tags=["summary_status"])

@app.get("/")
def root():
    return {"message": "PROSPARITY API is running"} 