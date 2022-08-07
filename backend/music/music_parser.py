import requests
from pytube import YouTube
import json
import os


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
    
    def _find_music_by_title(self, music_title: str) -> int:
        self.request_params['q'] = music_title
        responce = requests.get(self.api_url, params=self.request_params).text
        return json.loads(responce)['items'][0]['id']['videoId']
    
    def download_music_files(self) -> None:
        for title in self.music_titles:
            music_id = self._find_music_by_title(music_title=title)
            youtube = YouTube(f'https://www.youtube.com/watch?v={music_id}')
            audio = youtube.streams.get_audio_only()
            
            try:
                mp4_file = audio.download(self._upload_dir)
                root, ext = os.path.splitext(mp4_file)
                track = root + '.mp3'
                os.rename(mp4_file, track)
            except FileExistsError:
                os.remove(mp4_file)
                continue


music_title_list = []
while True:
    try:
        input_value = input('введите путь до файла с названиями треков... (для выхода введите exit)')
        if input_value == 'exit':
            break

        file = open(input_value)
        music_title_list = file.readlines()
        file.close()
        break
    except FileNotFoundError:
        print('Не удалось прочитать файл!')

if music_title_list:
    parser = MusicParser(api_key=API_KEY, music_titles=music_title_list)
    parser.download_music_files()


