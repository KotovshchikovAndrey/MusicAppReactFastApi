from fastapi import UploadFile
import os
from pathlib import Path
        
        
class FileManager:
    _upload_dir: str = os.path.join(os.path.dirname( __file__ ), '..','media')

    def __init__(self, file_name: str) -> None:
        self._file_name = file_name
        self._file_path = os.path.join(self._upload_dir, self._file_name)

    async def upload_file(self, file: UploadFile):
        with open(self._file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
            f.close()

        return self._file_name
    
    def open_file(self, mode: str = 'r'):
        file = open(self._file_path, mode)
        return file

    @property
    def get_file_size(self):
        path = Path(self._file_path)
        file_size = path.stat().st_size

        return file_size 