from typing import Union
from fastapi import APIRouter, Depends , status, Response, UploadFile, Body, File, Request
from requests import Session
from .music_repositories import MusicRepository
from .music_services import MusicStreamingService
from error.exception_errors import ApiError
from fastapi.responses import StreamingResponse, JSONResponse
from db import get_db


router = APIRouter(prefix='/music')

@router.get('/', status_code=status.HTTP_200_OK)
async def get_music_list(session: Session = Depends(get_db)):
    music_repository = MusicRepository(session=session)
    all_music = await music_repository.get_all()
    return all_music

@router.get('/{music_id}',status_code=status.HTTP_200_OK)
async def get_music_detail(music_id: int, session: Session = Depends(get_db)):
    music_repository = MusicRepository(session=session)
    music = await music_repository.get_by_id(id=music_id)
    return music

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_music(
    title: str = Body(),
    description: str = Body(),
    music_file: UploadFile = File(...),
    session: Session = Depends(get_db)
):
    if not music_file.filename:
        raise ApiError.bad_request(msg='Загрузите музыкальный файл!')

    music_repository = MusicRepository(session=session)
    await music_repository.create(
        title=title,
        description=description,
        music_file=music_file
    )

    return {
        'msg': 'Трек успешно создан!'
    }

@router.put('/{music_id}', status_code=status.HTTP_200_OK)
async def update_music(
    music_id: int,
    title: Union[str, None] = Body(),
    description: Union[str, None] = Body(),
    music_file: Union[UploadFile, None] = File(...),
    session: Session = Depends(get_db)
):
    music_repository = MusicRepository(session=session)

    music = await music_repository.get_by_id(id=music_id)
    if music is None:
        raise ApiError.bad_request(msg='Трек с таким id не найден!')

    await music_repository.update(
        id=music_id,
        title=title,
        description=description,
        music_file=music_file
    )

    return {
        'msg': 'Трек успешно обновлен!'
    }

@router.delete('/{music_id}', status_code=status.HTTP_204_NO_CONTENT)   
async def delete_music(music_id: int, session: Session = Depends(get_db)):
    music_repository = MusicRepository(session=session)
    await music_repository.delete(id=music_id)

    return JSONResponse(
        content={'msg': 'Трек удален!'}
    )

@router.get('/stream/{music_id}', status_code=status.HTTP_206_PARTIAL_CONTENT)
async def get_streaming_music(
    music_id: int,
    request: Request,
    session: Session = Depends(get_db)
):
    music_repository = MusicRepository(session=session)
    music = await music_repository.get_by_id(id=music_id)
    
    if music is None:
        return Response(content='Не удалось найти файл!',status_code=status.HTTP_404_NOT_FOUND)
    
    streaming_service = MusicStreamingService()
    music_file_name = music.get('file_name')
    file, status_code, content_length, content_range = streaming_service.get_streaming_data(
        file_name=music_file_name,
        request=request
    )

    response_headers = {
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
        'Cache-Control': 'no-cache',
        'Content-Range': content_range
    }

    return StreamingResponse(file, status_code=status_code,headers=response_headers)






