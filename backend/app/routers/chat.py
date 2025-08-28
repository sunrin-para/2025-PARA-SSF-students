from fastapi import APIRouter, HTTPException
from schemas import GetResponse, FunctionsRequest, FunctionsResponse, MessageResponse
from services import ChatService

router = APIRouter(
    prefix="/chat", tags=["chat"],
    responses={404: {"description": "Not found"}},
)

chat_service = ChatService()

@router.post("/functions", response_model=FunctionsResponse) # 사용자가 보낸 메세지를 받아서 어떤 과정을 거칠지 정하는 API 입니다.
async def get_functions(request: FunctionsRequest): # API를 호출 할때에는 FunctionsRequest 양식에 맞춰야합니다.
    try:
        role, message, created_at = request., request., request. # 양식의 값들을 다 각각 변수 선언 합니다. 빈칸을 채워주세요.
        functions = chat_service.get_functions() # 결과를 도출하는 함수를 추출합니다. 빈칸을 채워주세요.
        return FunctionsResponse(functions=functions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message", response_model=MessageResponse) # 사용자가 보낸 메세지에 답장을 해주는 API 입니다.
async def generate_message():
    try:
        message = chat_service.generate_message()
        return MessageResponse(message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get", response_model=GetResponse) # 사용자와의 메세지 기록을 불러오는 API 입니다.
async def get_chat():
    try:
        chat = chat_service.get()
        return GetResponse(data=chat)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
