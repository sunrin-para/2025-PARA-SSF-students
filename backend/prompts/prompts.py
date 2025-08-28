class PromptHandler:
    def __init__(self): # 각 프롬프트를 읽어옵니다
        self.functions_prompt = self.read_file('./prompts/function.md')
        self.chat_prompt = self.read_file('./prompts/talk.md')
        self.keyword_prompt = self.read_file('./prompts/keyword.md')

    def read_file(self, file_path): # 파일을 읽어오는 함수입니다.
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
