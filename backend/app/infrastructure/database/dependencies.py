from collections.abc import Generator

from sqlalchemy.orm import Session

from app.infrastructure.database.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
