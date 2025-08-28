from typing import List
from utils import JsonHandler

class UserService():
    def __init__(self):
        self.json_handler = JsonHandler("./data/preferences.json", []) # 데이터를 관리하는 객체를 가져옵니다.
        self.user = self.json_handler.read() # 데이터를 읽어옵니다.

    def update_preferences(self, moods: List[str], genres: List[str], countries: List[str]): # 선호도를 업데이트 하는 함수입니다.
        try:
            self.user = {
                "moods": moods or self.user.get("moods", []),
                "genres": genres or self.user.get("genres", []),
                "countries": countries or self.user.get("countries", [])
            } # 각 항목당 선호도를 업데이트합니다. 만약 None이 들어오면 기존 값으로 설정합니다.
            self.json_handler.write(self.user) # 데이터를 저장합니다.
            return "success"
        except Exception as e:
            raise Exception(str(e))

    def reset(self): # 선호도를 리셋합니다.
        try:
            self.user = {"moods": [], "genres": [], "countries": []}
            self.json_handler.write(self.user)
            return "success"
        except Exception as e:
            raise Exception(str(e))
