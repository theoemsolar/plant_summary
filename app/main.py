from fastapi import FastAPI
from app.routers.alarms import router as alarms_router
from app.routers.tracker import router as tracker_router
from app.routers.ufv_fps_inv_generic import router as ufv_fps_inv_generic_router


app = FastAPI()

app.include_router(alarms_router)
app.include_router(tracker_router)
app.include_router(ufv_fps_inv_generic_router)


@app.get("/")
async def root():
    return {"message": "Hello from O&M Solar"}
