from anime import Anime

class AnimeRepositoryFile:

    file_relative_path: str = "./anime_list.txt"
    _file_string_buffer: str = ""
    

    def __init__(self,):
        return
    
    def lines_splitter(self, lines: list) -> list:
        
        splitted_lines: list = []
        new_splitted_lines: list = []
        
        for line in lines:
            splitted_lines.append(line.split('\t'))
        for line in splitted_lines:
            for word in line:
                if word != '\t':
                    if word != '':
                        new_splitted_lines.append(word)
        return new_splitted_lines

    def retrieve_all_anime(self,) -> list:
        with open(self.file_relative_path, 'r') as fd:
            self._file_string_buffer = fd.read(4096)
            lines = self._file_string_buffer.split('\n')
        return self.lines_splitter(lines)

    def retrieve_anime_by_id(self, anime_id: int) -> Anime:
        return Anime()
    
    def retrieve_anime_by_title(self, title: str) -> Anime:
        return Anime()

    def retrieve_animes_by_author(self, author: str) -> list[Anime]:
        return [Anime()]
    
    def write_line_all_anime(self, lines: list):
        with open(self.file_relative_path, 'w') as fd:
            k = 1
            while(k <= len(lines)):
                if (k % 6 == 1):
                  fd.write(f'{lines[k-1][0]}: {lines[k-1][1]}\n')
                elif (k % 6 > 1 and k % 6 < 6):
                    fd.write(f'\t{lines[k-1][0]}: {lines[k-1][1]}\n')
                elif k % 6 == 0:
                    fd.write(f'{lines[k-1][0]}\n')
                k = k + 1
        return

    def append_new_anime(self, anime: Anime) -> Anime:
        with open(self._file_realtive_path, 'a') as fd:
            fd.write(b'{anime.anime_id}: {\n')
            fd.write(b'\ttitle: {anime.title},\n')
            fd.write(b'\tauthor: {anime.author},\n')
            fd.write(b'\tepisodes: {anime.episodes},\n')
            fd.write(b'\tseasons: {anime.seasons},\n')
            fd.write(b'},\n')
        return anime

    def update_existing_anime(self, anime: Anime) -> Anime:
        return Anime()

    def delete_existing_anime_by_id(self, anime_id: int) -> Anime:
        return Anime()

