from fastapi import FastAPI
from app.api.v1.routes import user
from app.api.v1.routes import summary_status
from app.api.v1.routes import filter_main
from app.api.v1.routes import application_row
from app.api.v1.routes import comments

from fastapi.middleware.cors import CORSMiddleware



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
app.include_router(filter_main.router, prefix="/api/v1/filters", tags=["filters"])
app.include_router(application_row.router, prefix="/api/v1/applications", tags=["applications"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])




@app.get("/")
def root():
    return {"message": "PROSPARITY API is running"} 