from pydantic import BaseModel
from typing import Dict, Any

class PlaylistResponse(BaseModel): # 플레이리스트를 생성하는 API의 반환 양식입니다.
    playlist: Dict[str, Any]
