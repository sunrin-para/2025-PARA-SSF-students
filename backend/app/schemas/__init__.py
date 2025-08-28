from typing import Any, Optional
from pydantic import BaseModel
from .chat import *
from .playlist import *
from .user import *

class GetResponse(BaseModel): # 정보를 불러오는 API의 반환 양식입니다.
    data: Optional[Any]

class ResetResponse(BaseModel): # 정보를 초기화 하는 API의 반환 양식입니다.
    message: str # 성공 여부
