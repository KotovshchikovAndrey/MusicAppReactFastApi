import pytest
from httpx import AsyncClient
import random
from backend.base.base_utils import FileManager


class TestMusic:

        @pytest.mark.asyncio
        async def test_read_music_list(self, client: AsyncClient) -> None:
                response = await client.get('/music/')
                assert response.status_code == 200
        
        @pytest.mark.asyncio
        async def test_read_music_detail(self, client: AsyncClient) -> None:
                response = await client.get(f'/music/{random.randint(1,100)}')
                assert response.status_code == 200
        
        @pytest.mark.asyncio
        async def test_create_music(self, client: AsyncClient):
                music_title = 'Макс Корж – Мотылёк (Владик Sky Remix).mp3'
                binary_music_file = FileManager(file_name=music_title).open_file(mode='rb')

                data = {
                        'title': 'test_music',
                        'description': 'test_desc'
                }

                create_response = await client.post(
                        url='/music/', 
                        data=data, 
                        files={ 'music_file': ( music_title, binary_music_file )}
                )

                assert create_response.status_code == 201

                music_id = create_response.json()['music_id']
                response = await client.get(f'/music/{music_id}')

                response_data = response.json()
                assert response_data['title'] == data['title']
                assert response_data['description'] == data['description']
                assert response_data['file_name'] == music_title
        
        @pytest.mark.asyncio
        async def test_update_music(self, client: AsyncClient):
                music_title = 'Linkin Park - In The End (Mellen Gi & Tommee Profitt Remix).mp3'
                binary_music_file = FileManager(file_name=music_title).open_file(mode='rb')

                update_data = {
                        'title': 'test_music_update',
                        'description': 'test_desc_update'
                }
                
                update_response = await client.put(
                        url=f'/music/1', 
                        data=update_data, 
                        files={ 'music_file': ( music_title, binary_music_file )}
                )

                assert update_response.status_code == 200

                music_id = update_response.json()['music_id']
                response = await client.get(f'/music/{music_id}')

                response_data = response.json()
                assert response_data['title'] == update_data['title']
                assert response_data['description'] == update_data['description']
                assert response_data['file_name'] == music_title

                


                

        


        

