from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    DemoAccountsResponse,
    DemoSessionRequest,
    DemoSessionResponse,
    LocalAccountsResponse,
    LocalSessionRequest,
    SchoolIdentitySessionRequest,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.get("/demo-accounts", response_model=DemoAccountsResponse)
def list_demo_accounts() -> DemoAccountsResponse:
    return AuthService().list_demo_accounts()


@router.get("/local-accounts", response_model=LocalAccountsResponse)
def list_local_accounts(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> LocalAccountsResponse:
    _ensure_admin(authorization, db)
    return AuthService(db).list_local_accounts()


@router.post("/demo-session", response_model=DemoSessionResponse)
def create_demo_session(payload: DemoSessionRequest) -> DemoSessionResponse:
    return AuthService().create_demo_session(payload.user_id)


@router.post("/local-session", response_model=DemoSessionResponse)
def create_local_session(
    payload: LocalSessionRequest,
    db: Session = Depends(get_db),
) -> DemoSessionResponse:
    return AuthService(db).create_local_session(payload.user_id)


@router.post("/school-session", response_model=DemoSessionResponse)
def create_school_identity_session(
    payload: SchoolIdentitySessionRequest,
    x_school_identity_secret: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> DemoSessionResponse:
    return AuthService(db).create_school_identity_session(
        payload,
        shared_secret=x_school_identity_secret,
    )


def _ensure_admin(authorization: str | None, db: Session) -> None:
    account = AuthService(db).current_account(authorization)
    if account.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can list local accounts",
        )
