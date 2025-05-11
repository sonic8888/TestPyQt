import nt
import os
import random
import re
import shutil
import tempfile
from pathlib import Path
from PyQt6 import QtCore
from supportive import progress_value

# path_to_dir: str = ''
# path_from_dir: str = ''
regex_pattern: str = r'^\d*\W*'
extensions = ('.mp3', '.wav', '.aif', '.mid', '.flac')
rp = re.compile(regex_pattern, re.I)
messages = {1: "укажите путь к папке с аудиофайлами или введите 'e' для завершения работы:",
            2: 'укажите путь к месту куда нужно скопировать  аудиофайлы:',
            3: "выберите действие или введите 'e' для завершения работы:",
            4: 'c - копировать с перемешиванием',
            5: 'm - переместить с перемешиванием',
            6: 'r - переименовать',
            7: 'укажите путь к месту куда нужно переместить  аудиофайлы:',
            8: 'ch - перемешать файлы в исходной папке',
            9: 'указанного пути не существует.'}


def is_math_type(entry):
    return isinstance(entry, nt.DirEntry)


def get_random_index(files: list):
    count_items = len(files)
    indexes = list(range(1, count_items + 1))
    random.shuffle(indexes)
    return indexes


def is_audio_files(entry: nt.DirEntry):
    is_audio = False
    if is_math_type(entry):
        if entry.is_file:
            extension = Path(entry.name).suffix
            if extension in extensions:
                is_audio = True
    return is_audio


def clear_name_file(entry: nt.DirEntry):
    clear_name = ''
    if is_math_type(entry):
        clear_name = re.split(rp, entry.name, maxsplit=1)
        clear_name = clear_name[-1]
    return clear_name


def get_audiofile_from_dir(path_dir: str):
    files = []
    with os.scandir(path_dir) as it:
        for item in it:
            if is_audio_files(item):
                files.append(item)
    return files


def rename(path_from):
    files = get_audiofile_from_dir(path_from)
    indexes = get_random_index(files)
    rename_audio_files(files, indexes, path_from)


def rename_audio_files(files: list, indexes: list, from_dir: str):
    if files and indexes and len(files) == len(indexes):
        for i in range(len(files)):
            old_name_files = files[i]
            if is_math_type(old_name_files):
                new_name = str(indexes[i]) + '. ' + clear_name_file(old_name_files)
                os.rename(old_name_files.path, os.path.join(from_dir, new_name))


def move_files(files: list, dst: str, signal_pb_set_value: QtCore.pyqtSignal, is_delete_parent_dir=False,
               parent_dir=''):
    count = len(files)
    fun_pb = progress_value(count)
    for index, file in enumerate(files):
        shutil.move(file.path, dst)
        is_v, val = fun_pb()
        if is_v:
            signal_pb_set_value.emit(val)
    if is_delete_parent_dir and parent_dir:
        shutil.rmtree(parent_dir, ignore_errors=True)


def move_files_to(files: list, dst: str, is_delete_parent_dir=False,
                  parent_dir=''):
    for file in files:
        shutil.move(file.path, dst)
    if is_delete_parent_dir and parent_dir:
        shutil.rmtree(parent_dir, ignore_errors=True)


def get_parent_dir(file: nt.DirEntry):
    if is_math_type(file):
        return os.path.dirname(file.path)
    else:
        return ''


def copy_files(files: list, dst: str, signal_pb_set_value: QtCore.pyqtSignal):
    count = len(files)
    fun_pb = progress_value(count)
    for index, file in enumerate(files):
        shutil.copy2(file.path, dst)
        is_v, val = fun_pb()
        if is_v:
            signal_pb_set_value.emit(val)


def move(path_from, path_to, signal_pb_set_value: QtCore.pyqtSignal):
    files = get_audiofile_from_dir(path_from)
    indexes = get_random_index(files)
    rename_audio_files(files, indexes, path_from)
    files = get_audiofile_from_dir(path_from)
    files = sorted(files, key=sort_key)
    move_files(files, path_to, signal_pb_set_value)


def sort_key(file: nt.DirEntry):
    name = file.name
    tp = name.partition('.')
    return int(tp[0])


def copy_mixed(path_from, path_to, signal_pb_set_value: QtCore.pyqtSignal):
    files = get_audiofile_from_dir(path_from)
    indexes = get_random_index(files)
    rename_audio_files(files, indexes, path_from)
    files = get_audiofile_from_dir(path_from)
    files = sorted(files, key=sort_key)
    copy_files(files, path_to, signal_pb_set_value)


def change(path_from, temp_path_to):
    files = get_audiofile_from_dir(path_from)
    indexes = get_random_index(files)
    rename_audio_files(files, indexes, path_from)
    files = get_audiofile_from_dir(path_from)
    move_files_to(files, temp_path_to)
    files = get_audiofile_from_dir(temp_path_to)
    files = sorted(files, key=sort_key)
    move_files_to(files, path_from)


# def display_progressbar(count: int, length: int):
#     a = 1
#     val = length / 100
#     if count > val * a:
#         a += 1
#         m.progress_value += 1


# def main():
#     global path_from_dir, path_to_dir
#     path_from_dir = input(messages[1])
#     if path_from_dir == 'e':
#         return
#     if os.path.exists(path_from_dir):
#         path_from_dir = os.path.abspath(path_from_dir)
#     else:
#         print(messages[9])
#         return
#     while True:
#
#         s = (messages[3], messages[4], messages[5], messages[6], messages[8])
#         message = "\n".join(s)
#         act = input(message + '\n:')
#         match act:
#             case 'c':
#                 try:
#                     path_to_dir = input(messages[7])
#                     if os.path.exists(path_to_dir):
#                         path_to_dir = os.path.abspath(path_to_dir)
#                     else:
#                         print(messages[9])
#                         continue
#                     files = get_audiofile_from_dir(path_from_dir)
#                     indexes = get_random_index(files)
#                     rename_audio_files(files, indexes)
#                     files = get_audiofile_from_dir(path_from_dir)
#                     files = sorted(files, key=sort_key)
#                     copy_files(files, path_to_dir)
#                 except Exception as e:
#                     print(e)
#                     break
#             case 'm':
#                 try:
#                     path_to_dir = input(messages[7])
#                     if os.path.exists(path_to_dir):
#                         path_to_dir = os.path.abspath(path_to_dir)
#                     else:
#                         print(messages[9])
#                         continue
#                     files = get_audiofile_from_dir(path_from_dir)
#                     indexes = get_random_index(files)
#                     rename_audio_files(files, indexes)
#                     files = get_audiofile_from_dir(path_from_dir)
#                     files = sorted(files, key=sort_key)
#                     move_files(files, path_to_dir)
#                 except Exception as e:
#                     print(e)
#                     break
#                 print(f" аудиофайлы находящиеся в {path_from_dir} перемещены в {path_to_dir} c перемешиванием.\n")
#
#             case 'r':
#                 try:
#                     files = get_audiofile_from_dir(path_from_dir)
#                     indexes = get_random_index(files)
#                     rename_audio_files(files, indexes)
#                 except Exception as e:
#                     print(e)
#                     break
#                 print(f'аудиофайлы находящиеся в: {path_from_dir} переименованы.\n')
#             case 'ch':
#                 try:
#                     files = get_audiofile_from_dir(path_from_dir)
#                     indexes = get_random_index(files)
#                     rename_audio_files(files, indexes)
#                     files = get_audiofile_from_dir(path_from_dir)
#                     print("ждите...")
#                     path_to_dir = tempfile.mkdtemp()
#                     move_files(files, path_to_dir)
#                     files = get_audiofile_from_dir(path_to_dir)
#                     files = sorted(files, key=sort_key)
#                     move_files(files, path_from_dir)
#                     print(f"аудиофайлы находящиеся в '{path_from_dir}' перемешаны.\n")
#                 except Exception as e:
#                     print(e)
#                 finally:
#                     shutil.rmtree(path_to_dir)
#             case 'e':
#                 break
#             case _:
#                 continue


if __name__ == "__main__":
    # main()
    pass
