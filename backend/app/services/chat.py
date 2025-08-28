import os, json, time
from typing import List, Dict, Optional
from openai import OpenAI
from prompts import PromptHandler
from utils import JsonHandler

class Pipeline(): # AI 답변을 생성하는 객체입니다.
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY")) # env 파일에서 openai api key를 가져옵니다.
        self.prompt_handler = PromptHandler() # AI가 제 역할을 수행할 수 있도록 하는 프롬프트 관리자를 선언합니다.

    def build_chat_with_system(self, chat: List[Dict], system_prompt: str): # 프롬프트를 채팅 기록 가장 최근 메세지 바로 직전에 추가하는 함수입니다.
        t = chat.pop() # 임시로 가장 최근 메세지를 떼어냅니다
        chat.append({"role": "system", "content": }) # 프롬프트를 가장 최근에 넣습니다. 빈칸을 채워주세요.
        chat.append(t) # 다시 떼어냈던 가장 최근 메세지에 넣습니다.
        return chat

    def parsed_response(self, response: str): # AI 답변을 객체화 하는 함수입니다.
        try:
            return json.loads(response.strip())
        except:
            start = response.find('[')
            end = response.rfind(']') + 1
            if '[' in response and end > start:
                try:
                    return json.loads(response[start:end])
                except:
                    pass
        return []

    def get_completion(self, chat: List[Dict]) -> str: # AI 답변을 생성하는 함수 입니다.
        response = self.client.chat.completions.create(model=, messages=) # OpenAi API에 모델명과 채팅 기록을 전달하여 답변을 생성합니다. 빈칸을 채워주세요.
        return response.choices[0].message.content # 답변을 반환 합니다.

    def select_functions(self, chat: List[Dict]): # 유저의 질문을 어떻게 처리해야하는지 결정하는 함수입니다.
        chat_with_system = self.build_chat_with_system(chat.copy(), self.prompt_handler.functions_prompt) # 프롬프트를 채팅 기록에 임시로 추가합니다.
        response = self.get_completion(chat_with_system) # AI 답변을 생성합니다.
        return self.parsed_response(response) # 답변을 객체화하여 반환 합니다.

    def generate_message(self, chat: List[Dict]) -> str: # 유저의 질문에 대해 어떻게 답장해야하는지 정하는 함수입니다.
        chat_with_system = self.build_chat_with_system(chat.copy(), self.prompt_handler.chat_prompt) # 프롬프트를 채팅 기록에 임시로 추가합니다.
        return self.get_completion(chat_with_system) # AI 답변을 생성합니다.

class ChatService():
    def __init__(self):
        self.json_handler = JsonHandler("./data/chat.json", []) # 데이터를 관리하는 객체를 가져옵니다.
        self.chat = self.json_handler.read() # 현재 채팅 내역을 불러와서 객체 내 변수로 선언 합니다.
        self.pipeline = Pipeline() # AI 답변을 생성하는 객체를 불러옵니다.

    def save_chat(self): # 대화내역이 업데이트 될떄마다 사용하는 용도의 함수입니다.
        self.json_handler.write(self.chat) # 대화내역을 저장합니다.

    def add_message(self, role: str, content: str, created_at: Optional[int] = None): # 메세지를 대화내역에 추가하는 함수입니다.
        message = {
            "role": role,
            "content": content,
            "created_at": created_at or int(time.time())
        }
        self.chat.append() # 메세지를 대화내역에 추가합니다. 빈칸을 채워주세요.
        return message

    def get_functions(self, role: str, message: str, created_at: Optional[int] = None): # 유저의 질문을 어떻게 처리해야할지 고르고 반환하는 함수입니다.
        try:
            self.add_message(, , ) # 메세지를 대화내역에 추가합니다. 빈칸을 채워주세요.
            functions = self.pipeline.select_functions(self.chat) # AI에게 어떤 과정을 거칠지 판단시킵니다.
            self.save_chat() # 대화내역을 저장합니다.
            return functions
        except Exception as e:
            raise Exception(str(e))

    def generate_message(self): # 유저의 질문에 대한 메세지를 생성하는 함수입니다.
        try:
            content = self.pipeline.generate_message(self.chat) # AI에게 메세지를 생성시킵니다.
            message = self.add_message("assistant", ) # AI의 답변을 대화내역에 추가합니다. 빈칸을 채워주세요.
            self.save_chat() # 대화내역을 저장합니다.
            return message
        except Exception as e:
            raise Exception(str(e))

    def get(self): # 대화내역을 불러오는 함수입니다.
        try:
            return self.chat
        except Exception as e:
            raise Exception(str(e))

    def reset(self): # 대화내역을 초기화 하는 함수입니다.
        try:
            self.chat = []
            self.save_chat()
        except Exception as e:
            raise Exception(str(e))
