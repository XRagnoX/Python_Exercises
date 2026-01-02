import time

class Anime:

    anime_id: int
    title: str = ''
    author: str = ''
    publication_date: str = ''
    seasons: int
    number_of_episodes: int

    metadata: dict = {}
    magic: int = 0

    _creation_date: float
    _last_update_date: float
    _last_access_date: float
    
    def __init__(self,):
        self.creation_date = time.time()
        self.last_update_date = time.time()
        self.last_access_date = time.time()
        return

    def get_anime_id(self,):
        self.last_access_date = time.time()
        return self.anime_id

    def set_anime_id(self, anime_id: int):
        self.last_access_date = time.time()
        self.last_update_date = time.time()
        self.anime_id = anime_id
        return

    def get_title(self,):
        self.last_access_date = time.time()
        return self.title

    def set_title(self, title: str):
        self.last_access_date = time.time()
        self.last_update_date = time.time()
        self.title = title
        return

    def get_author(self,):
        self.last_access_date = time.time()
        return self.author

    def set_author(self, author: str):
        self.last_access_date = time.time()
        self.last_update_date = time.time()
        self.author = author
        return

    def get_episodes(self,):
        self.last_access_date = time.time()
        return self.number_of_episodes

    def set_episodes(self, number_of_episodes: int):
        self.last_access_date = time.time()
        self.last_update_date = time.time()
        self.number_of_episodes = number_of_episodes
        return

    def get_seasons(self,):
        self.last_access_date = time.time()
        return self.seasons

    def set_seasons(self, seasons: int):
        self.last_access_date = time.time()
        self.last_update_date = time.time()
        self.seasons = seasons
        return

    def print_date_info(self,):
        print(time.strftime("Creation Date: %a %d %b %Y %H:%M:%S +0000" ,time.gmtime(self.creation_date)))
        print(time.strftime("Last Access: %a %d %b %Y %H:%M:%S +0000" ,time.gmtime(self.last_access_date)))
        print(time.strftime("Last Update: %a %d %b %Y %H:%M:%S +0000" ,time.gmtime(self.last_update_date)))


