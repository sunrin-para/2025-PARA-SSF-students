import os, json
from typing import Union, List, Dict

class JsonHandler(): # 데이터를 관리하는 객체입니다.
    def __init__(self, path: str, exist_data: Union[List, Dict]={}):
        self.path = path
        if not os.path.isfile(path):
            with open(self.path, "w", encoding="UTF-8") as f:
                json.dump(exist_data, f, ensure_ascii=False, indent="\t")

    def read(self): # 데이터를 읽어옵니다.
        with open(self.path, "r", encoding="UTF-8") as f:
            return json.load(f)

    def write(self, data: Union[List, Dict]): # 데이터를 저장합니다.
        with open(self.path, "w", encoding="UTF-8") as f:
            json.dump(data, f, ensure_ascii=False, indent="\t")
