from fastapi import FastAPI

from app.routers.tasks import router
from app.services.middleware import RequestContextMiddleware


app = FastAPI()

app.add_middleware(RequestContextMiddleware)
app.include_router(router)

@app.get("/")
def root():
    return "OK"