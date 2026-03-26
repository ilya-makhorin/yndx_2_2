from fastapi import FastAPI

from app.db.session import SessionLocal
from app.routers.auth import router as auth_router
from app.routers.tasks import router
from app.services.auth import seed_default_users
from app.services.middleware import RequestContextMiddleware


app = FastAPI()

app.add_middleware(RequestContextMiddleware)
app.include_router(router)
app.include_router(auth_router)

@app.on_event("startup")
def startup_seed_users() -> None:
    session = SessionLocal()
    try:
        seed_default_users(session)
    finally:
        session.close()


@app.get("/")
def root():
    return "OK"