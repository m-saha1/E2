from fastapi import FastAPI
from app.crud import router as crud_router
from app.analytics import router as analytics_router

app = FastAPI(title="Housing API")

app.include_router(crud_router, prefix="/data")
app.include_router(analytics_router, prefix="/analytics")

