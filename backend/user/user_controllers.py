from fastapi import APIRouter, Depends, status, Request
from user.user_repositories import UserRepository, TokenRepository
from user.user_schemas import UserCreateSchema, UserAuthSchema
from user.user_services import UserRegistrationService, UserAuthService, TokenService
from error.exception_errors import ApiError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import get_db
from user.user_auth_backend import AuthenticationBackend
from user.user_schemas import User

router = APIRouter(prefix='/user')


@router.get('/', status_code=status.HTTP_200_OK)
async def get_all_users(session: Session = Depends(get_db)):
    user_repository = UserRepository(session=session)
    users = await user_repository.get_all()
    return users


@router.get('/refresh', status_code=status.HTTP_200_OK)
async def refresh(request: Request, session: Session = Depends(get_db)):
    token = request.cookies.get('refresh_token')

    if not token:
        raise ApiError.unauthorized(msg='Токен не найден!')
    
    token_service = TokenService(token_repository=TokenRepository(session=session))
    token_payload = await token_service.check_refresh_token(token=token)

    if token_payload is None:
        raise ApiError.forbidden(msg='Токен невалиден!')
    
    new_access_token = token_service.create_access_token(payload=token_payload)
    responce_data = {
            'msg': 'Токен обновлен!',
            'access_token': new_access_token
        }

    return JSONResponse(content=responce_data)


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def get_user_detail(user_id: int , session: Session = Depends(get_db)):
    user_repository = UserRepository(session=session)
    user = await user_repository.get_by_id(id=user_id)
    return user


@router.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration(
    user: UserCreateSchema,
    session: Session = Depends(get_db)
):
    user_registration_service = UserRegistrationService(
        user_data=user.dict(), 
        user_repository=UserRepository(session=session)
    )

    if not await user_registration_service.registartion_data_is_valid():
        raise ApiError.bad_request(
            msg='Введены невалидные данные!', 
            error_list=user_registration_service.errors
        )

    token_service = TokenService(token_repository=TokenRepository(session=session))
    user_id = await user_registration_service.registration()
    access_token = token_service.create_access_token(payload={'user_id': user_id})
    refresh_token = token_service.create_refresh_token(payload={'user_id': user_id})
    await token_service.set_token_for_user(refresh_token=refresh_token, user_id=user_id)

    responce_data = {
        'msg': 'Вы успешно зарегестрировались!',
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    responce = JSONResponse(content=responce_data, status_code=status.HTTP_201_CREATED)
    responce.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=60*60*24*30)
    return responce


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: UserAuthSchema, session: Session = Depends(get_db)):
    user_auth_service = UserAuthService(user_repository=UserRepository(session=session))

    user = await user_auth_service.authenticate(user_data=user.dict())
    if not user:
        raise ApiError.unauthorized(msg='Неверный Логин или Пароль!')
    
    token_service = TokenService(token_repository=TokenRepository(session=session))
    access_token = token_service.create_access_token(payload={'user_id': user.id})
    refresh_token = token_service.create_refresh_token(payload={'user_id': user.id})
    await token_service.set_token_for_user(refresh_token=refresh_token, user_id=user.id)

    responce_data = {
            'msg': 'Авторизация прошла успешно!',
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    responce = JSONResponse(content=responce_data)
    responce.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=60*60*24*30)
    return responce 


@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(request: Request, session: Session = Depends(get_db)):
    token_service = TokenService(token_repository=TokenRepository(session=session))

    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise ApiError.unauthorized('Токен не найден!')
        
    await token_service.remove_token(token=refresh_token)

    responce = JSONResponse(content='Вы разлогинены!')
    responce.delete_cookie(key='refresh_token')
    return responce


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_db), 
    current_user: User = Depends(AuthenticationBackend(auth_db_type='SQL'))
):
    user_repository = UserRepository(session=session)
    await user_repository.delete(id=user_id)

    return JSONResponse(
        content={'msg': 'Пользователь удален!'}
    )
