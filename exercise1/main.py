from anime import Anime
from anime_repository_file import AnimeRepositoryFile
import time

def split_lines(anime_list_str: list[str], final_splitted_lines: list[list[str]]) -> list[list[str]]:
    
    splitted_line = []
    for line in anime_list_str:
        splitted_line = line.split(': ')
        final_splitted_lines.append(splitted_line)
    return final_splitted_lines

def find_a_word(splitted_lines_list: list, word: str):
    counter = 0
    for line_word in splitted_lines_list:
        if  word in line_word:
            counter = counter + 1
    return counter

def read_all_anime(anime_list_str: list, splitted_lines: list):
    k = 1
    while k <= len(splitted_lines):
        if k % 6 == 1:
            print(f'{splitted_lines[k-1][0]}: {splitted_lines[k-1][1]}')
        elif (k % 6 > 1 and k % 6 < 6):
            print(f'\t{splitted_lines[k-1][0]}: {splitted_lines[k-1][1]}')
        elif k % 6 == 0:
            print(f'{splitted_lines[k-1][0]}')
        k = k + 1
    return

def option_list():
    print('-a to Print all anime from the List')
    print('-r to Search an anime from the List')
    print('-w to Insert a new Anime')
    print('-u to Update an existing Anime')
    print('-d to Delete an anime from the List')
    print('-h to print the Current List')
    print('-q to exit the program')
    return

def search_by_id(anime_id: int, splitted_lines: list[list[str]]) -> list:
    anime_from_list: list = []
    k = 1
    flag = False
    while k <= len(splitted_lines):
        if anime_id == splitted_lines[k-1][0]:
            flag = True
        if flag:
            if k % 6 == 0:
                anime_from_list.append(splitted_lines[k-1][0])
                break
            anime_from_list.append(splitted_lines[k-1][0])
            anime_from_list.append(splitted_lines[k-1][1])
        k = k + 1
    anime_from_list.append('},')
    return anime_from_list

def update_anime_list(splitted_lines: list[list[str]], anime: Anime) -> list[list[str]]:
    
    anime_from_list: list[11]
    final_splitted_lines: list = []
    anime_from_list = search_by_id(anime.anime_id, splitted_lines)
    
    anime_from_list[3] = anime.get_title() + ','
    anime_from_list[5] = anime.get_author() + ','
    anime_from_list[7] = str(anime.get_episodes()) + ','
    anime_from_list[9] = str(anime.get_seasons()) + ','
    
    final_splitted_lines: list = []

    for line in splitted_lines:
        final_splitted_lines.append(line)
    
    k = 0
    j = 0
    flag = False
    while k < len(final_splitted_lines):    
        if j > len(anime_from_list):
            break
        if anime.anime_id == final_splitted_lines[k][0]:
            flag = True
        if flag:
            if j == 10:
                final_splitted_lines[k] = [anime_from_list[j]]
                break
            final_splitted_lines[k] = [anime_from_list[j], anime_from_list[j + 1]]
            j = j + 2
        k = k + 1
    print(final_splitted_lines)
    return final_splitted_lines

def main():
    
    anime_repo = AnimeRepositoryFile()
    anime_list_str: list[str] = anime_repo.retrieve_all_anime()
    splitted_lines: list = []

    splitted_lines = split_lines(anime_list_str, splitted_lines)

    anime = Anime()
    anime_list: list = []
    current_time = time.asctime()
    
    print(f'{current_time}')
    anime.print_date_info()
    
    while(True):
    
        program_option = input('Select an option or type -h to see the list of options:\n')
        
        if program_option == '0' or program_option == '-a':
            read_all_anime(anime_list_str, splitted_lines)
        elif program_option == '1' or program_option == '-r':
            print('Search an anime by title from the anime List')
            title = input('Title: ')
            for anime in anime_list:
                if anime.get_title() == title:
                    print(f'{anime.title}, {anime.author}')
                    return 0
            print(f'Not Found - title: {title}')
        elif program_option == '2' or program_option == '-w':
            print('Insert a new Anime')

            anime_id: int = input('Anime_id: ')
            title: str = input('Title: ')
            author: str = input('Author: ')
            episodes: str = input('Number of Episodes: ')
            seasons: str = input('Number of Seasons: ')

            anime = Anime()
            anime.set_anime_id(anime_id)
            anime.set_title(title)
            anime.set_author(author)
            anime.set_episodes(episodes)
            anime.set_seasons(seasons)
            
           # splitted_lines = split_lines(anime_list_str, splitted_lines)
            splitted_lines.append([f'{anime.get_anime_id()}', '{'])
            splitted_lines.append(['title', f'{anime.get_title()},'])
            splitted_lines.append(['author', f'{anime.get_author()},'])
            splitted_lines.append(['episodes', f'{anime.get_episodes()},'])
            splitted_lines.append(['seasons', f'{anime.get_seasons()},'])
            splitted_lines.append(['},'])
            
            anime_repo.write_line_all_anime(splitted_lines)
            anime_list.append(anime)
        
        elif program_option == '3' or program_option == '-u':
            
            anime = Anime()
            
            anime.set_anime_id(input('Anime Id: '))
            anime.set_title(input('Title: : '))
            anime.set_author(input('Author: '))
            anime.set_episodes(input('Episodes: '))
            anime.set_seasons(input('Seasons: '))
            
            splitted_lines = update_anime_list(splitted_lines, anime)
            anime_repo.write_line_all_anime(splitted_lines)

        elif program_option == '4' or program_option == '-d':
            print('Delete an anime from the List')

            anime = Anime()
            
            anime.set_title('')
            anime.set_author('')
            anime.set_episodes(0)
            anime.set_seasons(0)

            anime_id = input('Insert the anime Id: ')
            if anime_id == '':
                return -1

            anime.set_anime_id(anime_id)
            splitted_lines = update_anime_list(splitted_lines, anime)
            anime_repo.write_line_all_anime(splitted_lines)

        elif program_option == '5' or program_option == '-h':
            option_list()
        elif program_option == '6' or program_option == '-q':
            print('Quitting the Program...')
           # splitted_lines = split_lines(anime_list_str, splitted_lines)
            anime_repo.write_line_all_anime(splitted_lines)
            return 0
        else:
            print('Something went Wrong...')
    
    
    return -1


main()

