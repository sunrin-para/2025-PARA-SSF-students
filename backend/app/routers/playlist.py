from fastapi import APIRouter, HTTPException, Query
from schemas import GetResponse, PlaylistResponse
from services import PlaylistService

router = APIRouter(
    prefix="/playlist", tags=["playlist"],
    responses={404: {"description": "Not found"}},
)

playlist_service = PlaylistService()

@router.post("/generate", response_model=PlaylistResponse) # 사용자로 부터 수집한 정보를 바탕으로 맞춤형 플레이르스트를 제작하는 API 입니다.
def generate_playlist(track_length: int = Query(default=, description="생성할 트랙 개수", ge=1, le=100)): # 호출할때에는 플레이리스트 트랙 갯수를 받습니다. 만약 받은게 없으면 20개를 기본값으로 합니다. 빈칸을 채워주세요.
    try:
        playlist = playlist_service.generate_playlist() # 플레이리스트를 생성하는 함수를 호출합니다. 빈칸을 채워주세요.
        return PlaylistResponse(playlist=playlist)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get", response_model=GetResponse) # 기존의 생성되었던 플레이리스트를 불러옵니다.
async def get_playlist():
    try:
        data = playlist_service.get()
        return GetResponse(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
