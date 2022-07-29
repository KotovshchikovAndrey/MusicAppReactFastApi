from typing import Union
from sqlalchemy.orm import Session
from base.base_repository import BaseRepository
from user.user_schemas import User, Token
from abc import ABC, abstractmethod
from user.user_models import (
    User as user_model, 
    JwtToken as token_model
)


class AuthRepository(ABC):

    @abstractmethod
    def get_user(self, **user_data: dict) -> Union[None, User]:
        raise Exception('Абстрактный метод get_user должен быть переопределен!')


class UserRepository(BaseRepository, AuthRepository):
    _user_model: user_model = user_model

    def __init__(self, session: Session) -> None:
        super().__init__(model=self._user_model)
        self._session_db = session
    
    async def get_user(self, **user_data: dict) -> Union[None, User]:
        filter_query_params = " AND ".join("{}='{}'".format(key, val) for key, val in user_data.items()).strip()
        query = f"SELECT * FROM {self.table} WHERE {filter_query_params};"
        user = await self.database.fetch_one(query)
        if user is not None:
            return User.from_orm(user)

    async def username_exists(self, username) -> bool:
        query = f"SELECT EXISTS (SELECT true FROM {self.table} WHERE username='{username}')"
        return await self.database.fetch_val(query)

    async def email_exists(self, email) -> bool:
        query = f"SELECT EXISTS (SELECT true FROM {self.table} WHERE email='{email}')"
        return await self.database.fetch_val(query)


class TokenRepository(BaseRepository):
    _token_model: token_model = token_model

    def __init__(self, session: Session) -> None:
        super().__init__(model=self._token_model)
        self._session_db = session
    
    async def get_token_by_value(self, token_value) -> Union[None, Token]:
        query = self.table.select().where(self.table.c.refresh_token == token_value)
        token = await self.database.fetch_one(query=query)
        if token is not None:
            return Token.from_orm(token)
    
    async def delete_token_by_value(self, token_value) -> None:
        query = self.table.delete().where(self.table.c.refresh_token == token_value)
        await self.database.execute(query)
        
        