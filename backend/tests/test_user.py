import random
from urllib import response
import pytest
from httpx import AsyncClient
import jwt
import json
import time
from backend.user.user_services import ACCESS_TOKEN_SECRET_KEY, ALGORITHM


class TestUser:

    @pytest.mark.asyncio
    async def test_read_user_list(self, client: AsyncClient):
        response = await client.get('/user/')
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_read_user_detail(self, client: AsyncClient):
        response = await client.get(f'/user/{random.randint(1,100)}')
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_user_registration(self, client: AsyncClient):
        user_create_data = {
            'username': 'TestUser',
            'email': 'testemail@mail.ru',
            'password': '12345',
            'confirm_password': '12345'
        }

        response = await client.post(
            url='/user/registration',
            data=json.dumps(user_create_data),
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 201

        response_data = response.json()
        user_id = jwt.decode(
            response_data['access_token'], 
            ACCESS_TOKEN_SECRET_KEY, 
            ALGORITHM
        )['user_id']

        response = await client.get(f'/user/{int(user_id)}')
        assert response.json()['username'] == user_create_data['username']
        assert response.json()['email'] == user_create_data['email']
    
    @pytest.mark.asyncio
    async def test_uncorrect_registration(self, client: AsyncClient):
        uncorrect_create_data = {
            'username': 'TestUser',
            'email': 'testemailmail.ru',
            'password': '12345',
            'confirm_password': '1234'
        }

        response = await client.post(
            url='/user/registration',
            data=uncorrect_create_data
        )

        assert response.status_code in (422, 400)

    @pytest.mark.asyncio
    async def test_user_login(self, client: AsyncClient):
        """
            time.sleep помогает избежать одинаковой метки времени
            при создании refresh_token, если не добавить, то возникнет ошибка
            из за идентичной метки времени у зарегестрированного токена и токена,
            созданного при авторизации. В реальных условиях такая сетуация практически
            исключена, поэтому time.sleep нужен только при тестировании.
        """

        user_create_data = {
            'username': 'TestLoginUser',
            'email': 'testloginemail@mail.ru',
            'password': '12345',
            'confirm_password': '12345'
        }

        await client.post(
            url='/user/registration',
            data=json.dumps(user_create_data),
            headers={"Content-Type": "application/json"}
        )

        time.sleep(1)
        response = await client.post(
            url='/user/login',
            data=json.dumps(user_create_data),
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code == 200

        response_data = response.json()
        user_id = jwt.decode(
            response_data['access_token'], 
            ACCESS_TOKEN_SECRET_KEY, 
            ALGORITHM
        )['user_id']

        response = await client.get(f'/user/{int(user_id)}')
        assert response.json()['username'] == user_create_data['username']
        assert response.json()['email'] == user_create_data['email']
    
    @pytest.mark.asyncio
    async def test_uncorrect_login(self, client: AsyncClient):
        user_create_data = {
            'username': 'TestLoginUser',
            'email': 'testloginemail@mail.ru',
            'password': '12345',
            'confirm_password': '12345'
        }

        await client.post(
            url='/user/registration', 
            data=user_create_data
        )

        time.sleep(1)
        uncorrect_login_data = {
            'username': 'TestLoginUser',
            'email': 'testloginemail@mail.ru',
            'password': '1234*'
        }

        response = await client.post(
            url='/user/login',
            data=json.dumps(uncorrect_login_data),
            headers={"Content-Type": "application/json"}
        )

        assert response.status_code in (422, 401)








