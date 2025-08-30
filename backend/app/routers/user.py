from fastapi import APIRouter, HTTPException
from schemas import ResetResponse, PreferencesUpdateRequest, UpdateResponse
from services import UserService
from .chat import chat_service

router = APIRouter(
    prefix="/user", tags=["user"],
    responses={404: {"description": "Not found"}},
)

user_service = UserService()

@router.post("/preferences", response_model=UpdateResponse) # 유저와 대화를 통해 수집한 유저의 감정, 좋아하는 장르, 좋아하는 국가들을 수집하여 선호도에 저장합니다.
def update_preferences(request: PreferencesUpdateRequest): # 분위기, 장르, 국가를 양식으로 받습니다.
    try:
        moods, genres, countries = request, request, request # 각각 변수 선언 해줍니다. 빈칸을 채워주세요.
        message = user_service.update_preferences() # 선호도를 업데이트하는 함수를 호출합니다. 빈칸을 채워주세요.
        chat_service.update_preferences() # 해당 API가 호출된걸 기록합니다.
        return UpdateResponse(message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset", response_model=ResetResponse) # 유저의 선호도를 초기화 합니다.
def reset():
    try:
        message = user_service.reset()
        return ResetResponse(message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
