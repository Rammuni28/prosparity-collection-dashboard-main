from fastapi import FastAPI
from app.api.v1.routes import user
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import summary_status
from app.api.v1.routes import dealers
from app.api.v1.routes import ownership_types
from app.api.v1.routes import repayment_statuses
from app.api.v1.routes import vehicle_statuses
from app.api.v1.routes import calling_statuses
from app.api.v1.routes import lenders

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
app.include_router(dealers.router, prefix="/api/v1/dealers", tags=["dealers"])
app.include_router(ownership_types.router, prefix="/api/v1/ownership-types", tags=["ownership-types"])
app.include_router(repayment_statuses.router, prefix="/api/v1/repayment-statuses", tags=["repayment-statuses"])
app.include_router(vehicle_statuses.router, prefix="/api/v1/vehicle-statuses", tags=["vehicle-statuses"])
app.include_router(calling_statuses.router, prefix="/api/v1/calling-statuses", tags=["calling-statuses"])
app.include_router(lenders.router, prefix="/api/v1/lenders", tags=["lenders"])

@app.get("/")
def root():
    return {"message": "PROSPARITY API is running"} 