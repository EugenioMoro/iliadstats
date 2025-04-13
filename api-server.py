from fastapi import FastAPI
from routers import stats

app = FastAPI()
# Include the stats router
app.include_router(stats.router, prefix="/api/v1", tags=["IliadStats"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the IliadStats API"}