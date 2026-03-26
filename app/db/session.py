from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.config import get_database_url, settings


class Database:
    def __init__(self, url: str | None = None):

        self.url = url or self._build_postgres_url()

        self.engine = create_engine(
            self.url,
            echo=settings.APP_DEBUG,
            future=True,
            pool_pre_ping=True
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True
        )

    def _build_postgres_url(self) -> str:
        return get_database_url()

    def get_session(self) -> Session:
        return self.SessionLocal()

db=Database()
engine = db.engine
SessionLocal = db.SessionLocal


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()