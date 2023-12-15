import pytest
import random
import string
import os

from datetime import datetime
from test_task import data
from checker import checkout, get_out


# Предварительное создание директорий для тестирования
@pytest.fixture()
def make_folders():
    return checkout(f'mkdir {data["pwd_fold_1"]} {data["pwd_fold_2"]} {data["pwd_fold_3"]}', '')


@pytest.fixture()
def clear_folders():
    return checkout(f'rm -rf {data["pwd_fold_1"]}/* {data["pwd_fold_2"]}/* {data["pwd_fold_3"]}/*', '')

@pytest.fixture()
def make_file():
    list_of_files = []
    for i in range(data['count']):
        file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f'cd {data["pwd_fold_1"]}; dd if=/dev/urandom of={file_name} bs=1M count=1 iflag=fullblock', ''):
            list_of_files.append(file_name)
    return list_of_files



@pytest.fixture()
def make_name_arh():
    name_arh = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return name_arh

@pytest.fixture()
def make_subfolder():
    test_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    sub_folder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f'cd {data["pwd_fold_1"]}; mkdir {sub_folder_name}', ''):
        return None, None
    if not checkout(f'cd {data["pwd_fold_1"]}/{sub_folder_name}; dd if=/dev/urandom of={test_file_name} bs=1M count=1 iflag=fullblock', ''):
        return sub_folder_name, None
    return sub_folder_name, test_file_name

@pytest.fixture(autouse=True)
def time():
    # print(f'Start: {datetime.now().strftime("%H:%M:%S:%f")}')
    # yield print(f'Stop: {datetime.now().strftime("%H:%M:%S:%f")}'
    with open('stat.txt', 'a', encoding='utf-8') as f:
        res = get_out(f'cat {data["pwd_4"]}').replace('\n', '')
        yield f.writelines(f'Время: {datetime.now().strftime("%d-%m-%y %H:%M:%S:%f")} - Статистика загрузки процессора: {res} \n')