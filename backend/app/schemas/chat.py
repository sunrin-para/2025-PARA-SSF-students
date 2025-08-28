import time
from pydantic import BaseModel, Field
from typing import List, Optional

class FunctionsRequest(BaseModel): # 유저의 질문을 바탕으로 어떤 과정을 거칠지 정하는 API의 호출 양식입니다.
    role: str="user" # 역할, 기본값 user
    message: str # 질문, 유저가 한 말
    created_at: int=Field(default_factory=lambda: int(time.time())) # 유저가 전송한 시간. 자동으로 기록함

class FunctionsResponse(BaseModel): # 유저의 질문을 바탕으로 어떤 과정을 거칠지 정하는 API의 반환 방식입니다.
    functions: Optional[List]=None # 처리 과정

class MessageResponse(BaseModel): # 유저가 보낸 메세지에 답장해주는 API의 반환 양식입니다.
    message: dict # 답장
