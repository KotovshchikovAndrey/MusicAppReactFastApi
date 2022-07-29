from fastapi import UploadFile
from sqlalchemy.orm import Session
from music.music_models import Music as music_model
from base.base_utils import FileManager
from typing import Optional
from base.base_repository import BaseRepository


class MusicRepository(BaseRepository):
    _music_model: music_model = music_model

    def __init__(self, session: Session) -> None:
        super().__init__(model=self._music_model)
        self._session_db = session

    async def create(self,title: str, description: str, music_file: UploadFile) -> None:
        file_servise = FileManager(file_name=music_file.filename)
        upload_file_name = await file_servise.upload_file(file=music_file)
        
        create_data = {
            'title': title,
            'description': description,
            'file_name': upload_file_name
        }
        
        await super().create(create_data=create_data)
        return 
    
    async def update(
        self,
        id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        music_file: Optional[UploadFile] = None
    ) -> None:
        update_data = {}

        if title:
            update_data['title'] = title

        if description:
            update_data['description'] = description
        
        if music_file.filename:
            file_servise = FileManager(file_name=music_file.filename)
            upload_file_name = await file_servise.upload_file(file=music_file)
            update_data['file_name'] = upload_file_name
            
        await super().update(id=id, update_data=update_data)
        return 