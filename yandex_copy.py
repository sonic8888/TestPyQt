import os
import shutil
import sqlite3
import glob
import re

path_folder_out = ''
user_dict = os.environ['USERPROFILE']
base_path_yandex_music = {'user': user_dict, 'appdata': r'AppData\Local\Packages',
                          'yandex_music': 'Yandex.Music_', 'local': 'LocalState'}
kind = 5
pattern = r'[\?\\>\*<\/\|":]'
base_path = path_db = ''


def get_base_path():
    path = os.path.join(base_path_yandex_music['user'], base_path_yandex_music['appdata'])
    if not os.path.exists(path):
        print(f'не найдена папка:{path}')
        return -1
    path_yandex = ''
    for d in os.listdir(path):
        if d.find('Yandex.Music_') != -1:
            path_yandex = d
    if not path_yandex:
        print("не найдена папка содержащая 'Yandex.Music_'")
        return -1
    path_part_local = os.path.join(path, path_yandex, base_path_yandex_music['local'])
    return path_part_local


def get_path_db():
    _pattern = base_path + r'\*.SQlite'
    _path_db = glob.glob(_pattern)
    if _path_db:
        return _path_db[0]
    else:
        print(f'не найдена база данных:{base_path}*.SQlite')
        return -1


def get_path_music(db_name):
    base_name = os.path.basename(db_name)
    name = os.path.splitext(base_name)[0]
    name_dir = name.split('_')
    _path_music = os.path.join(base_path, 'Music', name_dir[1])
    return _path_music


def copy_files():
    global base_path, path_db
    base_path = get_base_path()
    # print(base_path)
    if base_path == -1:
        exit()
    path_db = get_path_db()
    if path_db == -1:
        exit()
    # print(path_db)
    path_folder_source = get_path_music(path_db)
    con = sqlite3.connect(path_db)

    cursor = con.cursor()

    t_track_id = tuple(cursor.execute('SELECT TrackId FROM T_PlaylistTrack WHERE Kind = ?', (kind,)))
    for track_id in t_track_id:
        _id = track_id[0]
        cursor.execute('SELECT Title FROM T_Track WHERE Id = ?', (_id,))
        name_single = cursor.fetchone()[0]
        cursor.execute('SELECT ArtistId FROM T_TrackArtist WHERE TrackId = ?', (_id,))
        artist_id = cursor.fetchone()[0]
        cursor.execute('SELECT Name FROM T_Artist WHERE Id = ?', (artist_id,))
        artist_single = cursor.fetchone()[0]
        new_file_name = name_single + ' ' + artist_single
        new_file_name = re.sub(pattern, '_', new_file_name) + '.mp3'
        file_out = os.path.join(path_folder_out, new_file_name)
        file_source = os.path.join(path_folder_source, _id + '.mp3')
        if os.path.exists(file_source):
            try:
                path = shutil.copy2(file_source, file_out)
            except OSError:
                print(file_source, file_out)
        else:
            print(f'файл: {file_source} не найден.')


def main():
    global path_folder_out
    while True:
        path_folder_out = input("Укажите путь к папке для копирования файлов или 'n' для выхода: ")
        if path_folder_out == 'n':
            break
        if os.path.isdir(path_folder_out):
            copy_files()
            print(f'копирование файлов в директорию: {path_folder_out} \n'
                  f'успешно завершено.')
            break
        else:
            print(f'путь:{path_folder_out} не найден.\n'
                  f'укажите существующий путь. ')
            continue


if __name__ == "__main__":
    main()
