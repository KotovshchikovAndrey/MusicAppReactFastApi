import sys
import os

sys.path.append(os.path.join(sys.path[0], '../../'))

from pytube import YouTube
from backend.db import database
import asyncio
from aiohttp import ClientSession

API_KEY = 'AIzaSyDc_a6zS2ugNOvvJQHnnMVcKPwV7EXmyvM'


class MusicParser:
    _upload_dir: str = os.path.join(os.path.dirname( __file__ ), '..','media')

    def __init__(self, api_key: str, music_titles: list) -> None:
        self.music_titles = music_titles
        self.api_url = 'https://www.googleapis.com/youtube/v3/search'
        self.request_params = {
            'key': api_key,
            'type': 'video'
        }
    
    async def _find_music_by_title(self, music_title: str, session: ClientSession) -> int:
        self.request_params['q'] = music_title
        async with session.get(url=self.api_url, params=self.request_params) as response:
            json_response = await response.json()
        
        return json_response['items'][0]['id']['videoId']
    
    async def _download_music_file(self, music_title: str) -> None:
        async with ClientSession() as session:
            music_id = await self._find_music_by_title(
                music_title=music_title, 
                session=session
            )
            
        youtube = YouTube(f'https://www.youtube.com/watch?v={music_id}')
        audio = youtube.streams.get_audio_only()

        try:
            mp4_file = audio.download(self._upload_dir)
            root, ext = os.path.splitext(mp4_file)
            track = root + '.mp3'
            os.rename(mp4_file, track)
        except FileExistsError:
            os.remove(mp4_file)
        else:
            title = os.path.basename(root)
            file_name = title + '.mp3'
            query = f"INSERT INTO music (title, file_name) VALUES ('{title}', '{file_name}')"
            await database.execute(query=query)
    
    async def parse_music(self):
        await database.connect()

        await asyncio.gather(
            *[self._download_music_file(music_title=title) for title in self.music_titles]
        )


if __name__ == '__main__':
    music_title_list = []
    while True:
        try:
            input_value = input('введите путь до файла с названиями треков... (для выхода введите exit)')
            if input_value == 'exit':
                break

            file = open(input_value, encoding='UTF-8')
            music_title_list = file.readlines()
            file.close()
            break
        except FileNotFoundError:
            print('Не удалось прочитать файл!')

    if music_title_list:
        parser = MusicParser(api_key=API_KEY, music_titles=music_title_list)
        asyncio.run(parser.parse_music())


