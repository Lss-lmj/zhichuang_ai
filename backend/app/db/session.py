from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

def _project_root() -> Path:
    backend_root = Path(__file__).resolve().parents[2]
    repo_root = backend_root.parent
    return repo_root if (repo_root / "Makefile").exists() else backend_root


def _database_url() -> str:
    if not settings.database_url.startswith("sqlite:///"):
        return settings.database_url
    sqlite_path = settings.database_url.removeprefix("sqlite:///")
    if sqlite_path == ":memory:":
        return settings.database_url
    path = Path(sqlite_path)
    if not path.is_absolute():
        path = _project_root() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{path}"

database_url = _database_url()
connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
