from fastapi import Request
from typing import IO, Generator
from base.base_utils import FileManager


class MusicStreamingService:
    
    def _ranged(
        self, 
        file: IO[bytes],
        start: int = 0,
        end: int = None,
        block_size: int = 8192
    ) -> Generator:
        consumed = 0

        file.seek(start)
        while True:
            data_length = min(block_size, end - start - consumed) if end else block_size
            if data_length <= 0:
                break
            data = file.read(data_length)
            if not data:
                break
            consumed += data_length
            yield data

        if hasattr(file, 'close'):
            file.close()
    
    def get_streaming_data(self, file_name: str, request: Request) -> tuple:
        file_service = FileManager(file_name=file_name)
        file = file_service.open_file(mode='rb')
        file_size = file_service.get_file_size
        content_length = file_size
        status_code = 200
        
        content_range = request.headers.get('range')
        if content_range is not None:
            content_ranges = content_range.strip().lower().split('=')[-1]
            range_start, range_end, *_ = map(str.strip, (content_ranges + '-').split('-'))
            range_start = max(0, int(range_start)) if range_start else 0
            range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
            content_length = (range_end - range_start) + 1
            file = self._ranged(file=file, start=range_start, end=range_end + 1)
            status_code = 206
            content_range = f'bytes {range_start}-{range_end}/{file_size}'

        return file, status_code, content_length, content_range      

        

