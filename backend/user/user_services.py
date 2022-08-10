from asyncio import tasks
from user.user_repositories import UserRepository, TokenRepository
from fastapi import Request
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Union
from user.user_schemas import User
from user.user_tasks import clear_expired_token_task


REFRESH_TOKEN_SECRET_KEY = 'zpijfjkfzkfjzkjfiojijklfnhduofhuhzljfj'
ACCESS_TOKEN_SECRET_KEY = 'ouhozhfioidmnvndzinifjnzjkldnfkjlnkjznd'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30
REFRESH_TOKEN_EXPIRE = 30


class TokenService:

    def __init__(self, token_repository: TokenRepository) -> None:
        self._token_repository = token_repository
    
    def create_access_token(self, payload: dict) -> str:
        payload_to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
        payload_to_encode.update({"exp": expire})
        token = jwt.encode(payload_to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

        return token
    
    def create_refresh_token(self, payload: dict) -> str:
        payload_to_encode = payload.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE)
        payload_to_encode.update({"exp": expire})
        token = jwt.encode(payload_to_encode, REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)

        clear_expired_token_task.apply_async((token, ), eta=expire)

        return token
    
    async def check_refresh_token(self, token) -> Union[None, str]:
        token_in_db = await self._token_repository.get_token_by_value(token_value=token)
        if token_in_db is None:
            return None
        
        try:
            payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except Exception:
            await self.remove_token(token=token)
            return None

    async def set_token_for_user(self, user_id: int, refresh_token: str) -> None:
        create_data = {
            'refresh_token': refresh_token,
            'user_id': user_id
        }

        await self._token_repository.create(create_data=create_data)
    
    async def remove_token(self, token) -> None:
         await self._token_repository.delete_token_by_value(token_value=token)


class UserRegistrationService:
    
    def __init__(
        self, 
        user_data: dict, 
        user_repository: UserRepository
    ) -> None:
        self._user_data = user_data
        self._user_repository = user_repository
        self._errors = []
        
    async def _validate_registration_data(self) -> None:
        username = self._user_data.get('username')
        email = self._user_data.get('email')
        password = self._user_data.get('password')
        confirm_password = self._user_data.get('confirm_password')

        if await self._user_repository.username_exists(username=username):
            self._errors.append(f'Пользователь с именем {username} уже существует!')

        if await self._user_repository.email_exists(email=email):
            self._errors.append(f'Пользователь с почтой {email} уже существует!')
        
        if password != confirm_password:
            self._errors.append('Пароли не совпадают!')

    async def registartion_data_is_valid(self) -> bool:
        await self._validate_registration_data()
        if not self._errors:
            return True
        
        return False

    async def registration(self) -> int:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hash_password = pwd_context.hash(self._user_data['password'])

        create_data ={
            'username': self._user_data['username'],
            'email': self._user_data['email'],
            'password': hash_password
        }
        
        user_id = await self._user_repository.create(create_data=create_data)
        return user_id
        
    @property
    def errors(self) -> list:
        return self._errors


class UserAuthService:

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository
    
    def verify_password(self, introduced_password, hashed_password) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(introduced_password, hashed_password)
    
    async def authenticate(self, user_data: dict) -> Union[bool, User]:
        user_data_for_repository = {
            'username': user_data.get('username', ''),
            'email': user_data.get('email', '')
        }

        user = await self._user_repository.get_user(**user_data_for_repository)
        if user is None:
            return False

        if not self.verify_password(
            introduced_password=user_data.get('password', ''), 
            hashed_password=user.password
        ):
            return False
        
        return user
    
    async def get_current_user(self, request: Request) -> Union[None, User]:
        authorization = request.headers.get('authorization')
        if not authorization:
            return None
        
        acess_token = authorization.split()[-1]
        if not acess_token:
            return None
        
        try:
            payload = jwt.decode(acess_token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload['user_id']
        except Exception:
            return None
        
        user = await self._user_repository.get_user(id=user_id)
        if user is None:
            return None
        
        return user
        

            







    

        