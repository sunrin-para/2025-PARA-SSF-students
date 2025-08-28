import os, json, time, random, spotipy
from typing import List, Dict
from spotipy.oauth2 import SpotifyClientCredentials
from openai import OpenAI
from prompts import PromptHandler
from utils import JsonHandler

class Pipeline(): # AI 답변을 생성하는 객체이다.
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_KEY")) # env 파일에서 openai api key를 가져옵니다.
        self.prompt_handler = PromptHandler() # AI가 제 역할을 수행할 수 있도록 하는 프롬프트 관리자를 선언합니다.

    def parsed_chat(self, preferences: Dict[str, List], prompt: str): # AI가 제 역할을 수행할 수 있도록 하는 프롬프트를 추가하는 함수입니다.
        return [
            {"role": "system", "content": }, # 프롬프트를 추가합니다. 빈 칸을 채워주세요.
            {"role": "user", "content": str(preferences)}
        ]

    def parsed_response(self, response: str): # AI 답변을 객체화 하는 함수입니다.
        try:
            return json.loads(response.strip())
        except:
            start = response.find("[")
            end = response.rfind("]") + 1
            if '[' in response and end > start:
                try:
                    return json.loads(response[start:end])
                except:
                    pass
        return []

    def generate_keywords(self, preferences: Dict[str, List]): # 유저의 선호도를 바탕으로 키워드를 생성하는 함수입니다.
        chat = self.parsed_chat(preferences, self.prompt_handler.keyword_prompt) # 키워드 생성 역할을 부여하는 프롬프트를 추가합니다.
        response = self.client.chat.completions.create(model=, messages=) # OpenAI API를 호출하여서 키워드를 생성합니다. 빈칸을 채워주세요.
        return self.parsed_response(response.choices[0].message.content) # 객체화된 결과를 반환합니다.

class SpotifyHandler: # Spotify API를 사용하는 객체이다.
    def __init__(self):
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv("SPOTIFY_ID"),
            client_secret=os.getenv("SPOTIFY_SECRET")
        ) # env 파일에서 SPOTIFY API 정보를 읽어옵니다.
        self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager) # Spotify API를 불러옵니다.

    def search_playlists(self, query: str, limit: int = 10): # Spotify API를 사용하여 내 선호도와 비슷한 플레이르스트를 검색하여 필요한 정보만 빼내는 함수입니다.
        response = self.spotify.search(q=query, type="playlist", limit=limit) # Spotify API를 호출하여 플레이리스트를 검색합니다.
        playlists = [] # 검색결과 저장
        for playlist in response["playlists"]["items"]: # 검색결과 내 플레이리스트들을 각각 꺼냅니다.
            if playlist: # 만약 플레이리스트가 존재한다면
                playlists.append({
                    "id": playlist["id"],
                    "name": playlist["name"],
                    "url": playlist["href"]
                }) # 플레이리스트 정보에서 id, name, url 만 빼내어서 저장합니다.
        return random.sample(playlists, min(3, len(playlists))) # 검색한 플레이르스트중 3개만 추출합니다.

    def get_tracks(self, playlist_id: str): # 플레이리스트에서 곡만 추출하여서 필요한 정보를 빼내는 함수입니다.
        response = self.spotify.playlist_tracks(playlist_id) # 플레이리스트에서 곡만 추출합니다.
        tracks = [] # 곡 정보 저장
        for item in response["items"]: # 플레이리스트에서 곡 리스트를 추출합니다.
            if item["track"]: # 플레이리스트에서 곡이 존재하는 경우
                track = item["track"] # 곡 변수 선언
                artists = [] # 곡 아티스트 저장
                for artist in track['artists']: # 아티스트가 여러명인 경우 하나씩 정보 추출합니다.
                    artists.append({
                        'id': artist['id'],
                        'name': artist['name'],
                        'url': artist['external_urls']['spotify']
                    }) # API에서 필요한 정보만 추출합니다.
                thumbnail = None # 썸네일 기본값 None으로 선언합니다.
                if track["album"]["images"]: # 썸네일이 존재 하는 경우
                    thumbnail = track["album"]["images"][0]["url"] # 썸네일 이미지 URL을 저장합니다.
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    "url": track["external_urls"]["spotify"],
                    'duration': track['duration_ms'],
                    'artists': artists,
                    "thumbnail": thumbnail
                }) # 곡 정보를 tracks 리스트에 추가합니다.
        return tracks # tracks 리스트를 반환합니다.

class PlaylistService():
    def __init__(self):
        self.json_handler = JsonHandler("./data/playlist.json") # 데이터를 관리하는 객체를 가져옵니다.
        self.pipeline = Pipeline() # AI 답변을 생성하는 객체를 불러옵니다.

    def collect_tracks_from_playlist(self, playlist, total_tracks, track_length): # 플레이리스트에서 곡을 수집하는 함수입니다.
        if len(total_tracks) >= track_length: # 수집한 곡 수가 목표 곡 수보다 많거나 같으면 False를 반환합니다.
            return False # False를 반환합니다.

        spotify_handler = SpotifyHandler() # SpotifyHandler 객체를 불러옵니다.
        tracks = spotify_handler.get_tracks(playlist["id"]) # SpotifyHandler 객체를 사용하여 플레이리스트에서 곡을 가져옵니다.

        for track in tracks: # 가져온 곡을 반복합니다.
            if len(total_tracks) >= track_length: # 수집한 곡 수가 목표 곡 수보다 많거나 같으면 반복을 종료합니다.
                break # 반복을 멉춥니다.
            total_tracks[track["id"]] = track #곡 정보를 total_tracks 딕셔너리에 추가합니다.

        return True # True를 반환합니다.

    def generate_playlist(self, track_length: int):
        try:
            chat_handler = JsonHandler("./data/chat.json") # 채팅내역 파일을 불러옵니다.
            chat = chat_handler.read() # 파일을 읽습니다.
            chat.append({
                "role": "system",
                "content": "generate_playlist",
                "created_at": int(time.time())
            }) # 파일에 플레이리스트가 생성된 시점을 기록합니다.
            chat_handler.write(chat) # 파일을 저장합니다.

            sources = [] # 참고한 플레이리스트를 저장합니다.
            total_tracks = {} # 생성된 플레이리스트의 곡들을 저장합니다.
            spotify_handler = SpotifyHandler() # SpotifyHandler 객체를 불러옵니다.

            preferences = JsonHandler("./data/preferences.json").read() # 유저 선호도 파일을 읽습니다.
            keywords = self.pipeline.generate_keywords() # 선호도를 바탕으로 키워드를 생성합니다. 빈칸을 채워주세요.

            for keyword in keywords: # 생성된 키워드들을 반복합니다.
                if len(total_tracks) >= track_length: # 생성된 플레이리스트의 곡 수가 목표 길이보다 크거나 같으면 반복문을 종료합니다.
                    break # 반복문 종료

                playlists = spotify_handler.search_playlists(keyword) # 키워드로 검색
                sources.extend(playlists) # 참고한 플레이리스트들을 저장합니다.

                for playlist in playlists:
                    should_continue = self.collect_tracks_from_playlist(, ,) # 플레이리스트에서 곡을 수집합니다. 빈칸을 채워주세요.
                    if not should_continue: # 플레이리스트에서 곡을 수집하지 못했을 경우 반복문을 종료합니다.
                        break # 반복문 종료

            available_tracks = list(total_tracks.values()) # 곡 목록을 추출합니다.
            selected_tracks = random.sample(available_tracks, min(track_length, len(available_tracks))) # 곡 목록에서 랜덤으로 목표 곡수 만큼 곡을 선택합니다.

            playlist = {"tracks": selected_tracks, "sources": sources} # 플레이리스트 데이터를 변수 선언 합니다.
            self.json_handler.write(playlist) # 데이터를 저장합니다

            return playlist # 데이터를 반환합니다.
        except Exception as e:
            raise Exception(str(e))

    def get(self): # 플레이리스트를 가져오는 함수입니다.
        try:
            return self.json_handler.read()
        except Exception as e:
            raise Exception(str(e))

    def reset(self): # 초기화 하는 함수입니다.
        try:
            self.json_handler.write({"tracks": [], "sources": []})
            return "success"
        except Exception as e:
            raise Exception(str(e))
