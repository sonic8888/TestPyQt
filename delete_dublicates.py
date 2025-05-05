import os, re
import pprint
from re import Pattern
from rapidfuzz import fuzz
from colorama import Fore

path_directory = ""
pattern_digital = r"^[0-9\.\-\s)]{1,}"
equals_value = 95.0


def create_clean_name_list(directory: str) -> []:
    _list_files = os.listdir(directory)
    p = re.compile(pattern_digital, re.I)
    list_files = []
    for file in _list_files:
        _clean_name = get_clean_name(file, p)
        list_files.append((file, _clean_name))
    return list_files


def get_clean_name(file_name: str, regular_object: Pattern) -> str:
    _res = regular_object.match(file_name)
    if _res:
        return file_name[_res.end():]
    else:
        return file_name


def search_duplicates(sequence: {}) -> {}:
    _set_num = set()
    _dict_duplicates = {}
    for n in range(0, len(sequence) - 2):
        if n is _set_num:
            continue
        _list_names = []
        for m in range(n + 1, len(sequence) - 1):
            _value = fuzz.QRatio(sequence[n][1], sequence[m][1])
            if _value > equals_value:
                _set_num.add(m)
                _list_names.append(sequence[m][0])
        if _list_names:
            _dict_duplicates[sequence[n][0]] = _list_names
    return _dict_duplicates


def dictionary_to_list(dictionary: {}) -> []:
    _list = []
    for item in dictionary.values():
        for n in item:
            _list.append(n)
    return _list


def show_sequence(sequence: []):
    pprint.pprint(sequence)
    print('')


def editing_list_duplicates(duplicates: [], files: []) -> []:
    duplicates = duplicates.copy()
    for f in files:
        for dup in duplicates:
            if dup.startswith(f):
                duplicates.remove(dup)
    return duplicates


def remove_duplicates(duplicates: []):
    for file in duplicates:
        _file_path = os.path.join(path_directory, file)
        try:
            os.remove(_file_path)
        except FileNotFoundError:
            print(Fore.RED + f"файл:{_file_path} не найден")
        except OSError:
            print(Fore.RED + f"не удалось удалить файл:{_file_path}")


def main():
    global  path_directory
    while True:
        path_directory = input("Укажите путь к папке или 'n' для выхода: ")
        if path_directory == 'n':
            break
        if not os.path.isdir(path_directory):
            print(Fore.RED + 'Путь к папке или диску указан неверно')
            continue
        _val = input(f"значение соответствия по умолчанию равно: {equals_value}, \n"
                     f"если нужно изменить нажмите 'v', если нет любую другую клавишу: ")
        if _val == 'v':
            while True:
                try:
                    _val_equals = float(input('введите значение от 50.0 до 100.0: '))
                    if _val_equals < 50.0 or _val_equals > 100.0:
                        print("значение должно быть в диапазоне от 50.0 до 100.0")
                        continue
                    input(f"значение соответствия равно: {_val_equals} ")
                    break
                except ValueError:
                    print(Fore.RED + "значение должно быть десятичным числом")
                    continue
        _files = create_clean_name_list(path_directory)
        _duplicates = search_duplicates(_files)
        _list_duplicates = dictionary_to_list(_duplicates)
        show_sequence(_duplicates)
        if not _list_duplicates:
            print("дубликаты не найдены.")
            break
        _val = input("если нужно отредактировать удаляемые файлы введите:'r'\n"
                     "если нет любую другую клавишу: ")
        if _val == 'r':
            _list_not_delete = []
            while True:
                _file_start_name = input("введите имя файла который не нужно удалять,\n"
                                         " или 'break' для выхода: ")
                if _file_start_name == 'break':
                    break
                _list_not_delete.append(_file_start_name)
            _list_duplicates = editing_list_duplicates(_list_duplicates, _list_not_delete)
            remove_duplicates(_list_duplicates)
            print("были удалены файлы:")
            show_sequence(_list_duplicates)
            break
        remove_duplicates(_list_duplicates)
        print("были удалены файлы:")
        show_sequence(_list_duplicates)
        break


if __name__ == '__main__':
    main()
