from app.database import SessionLocal


def get_db() -> None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
