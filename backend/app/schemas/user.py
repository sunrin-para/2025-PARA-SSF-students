from pydantic import BaseModel
from typing import List, Optional

class PreferencesUpdateRequest(BaseModel): # 유저 선호도를 업데이트 하는 API의 호출 양식입니다.
    genres: Optional[List]=None # 좋아하는 장르
    moods: Optional[List]=None # 좋아하는 분위기
    countries: Optional[List]=None # 좋아하는 노래의 국가

class UpdateResponse(BaseModel): # 유저 선호도를 업데이트 하는 API의 반환 양식입니다.
    message: str # 성공 여부
