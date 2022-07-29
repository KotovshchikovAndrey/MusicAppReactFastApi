from user.user_services import UserAuthService
from user.user_repositories import UserRepository
from fastapi import Depends, Request
from user.user_schemas import User
from error.exception_errors import ApiError
from sqlalchemy.orm import Session
from db import get_db


class AuthRepositoryFactory:

    def create_auth_repositoty(self, db_type: str, session: Session):
        if db_type == 'SQL':
            return UserRepository(session=session)
        
        return UserRepository(session=session)


class AuthenticationBackend:

    def __init__(self, auth_db_type: str) -> None:
        self._auth_db_type = auth_db_type
        self._auth_repository_factory = AuthRepositoryFactory()
    
    async def __call__(self, request: Request, session: Session = Depends(get_db)) -> User:
        self._auth_service = UserAuthService(
            user_repository=self._auth_repository_factory.create_auth_repositoty(
                db_type=self._auth_db_type, 
                session=session
            )
        )

        auth_user = await self._auth_service.get_current_user(request=request)
        if auth_user is None:
            raise ApiError.unauthorized(msg='Токен невалиден!')

        return auth_user