import pytest
import random
import string
import os

from datetime import datetime
from test_task import data
from checker import get_out, upload_files, ssh_checkout


# Предварительное создание директорий для тестирования
# @pytest.fixture()
# def make_folders():
#     return checkout(f'mkdir {data["pwd_fold_1"]} {data["pwd_fold_2"]} {data["pwd_fold_3"]}', '')


@pytest.fixture()
def make_folders():
    if not ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f'ls /home/{data.get("user_name")}',
        "Test",
    ):
        return ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f'mkdir /home/{data.get("user_name")}/Test; cd /home/{data.get("user_name")}/Test; mkdir dir_file dir_zip dir_unzip',
            "",
        )
    return ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f'cd /home/{data.get("user_name")}/Test; mkdir dir_file dir_zip dir_unzip',
        "",
    )


@pytest.fixture()
def clear_folders():
    return ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f'rm -rf /home/{data.get("user_name")}/Test',
        "",
    )


@pytest.fixture()
def make_file():
    list_of_files = []
    for i in range(data["count"]):
        file_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f'cd /home/{data.get("user_name")}/Test/dir_file; dd if=/dev/urandom of={file_name} bs=1M count=1 iflag=fullblock',
            "",
        ):
            list_of_files.append(file_name)
    return list_of_files


@pytest.fixture()
def make_name_arh():
    name_arh = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return name_arh


@pytest.fixture()
def make_subfolder():
    test_file_name = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )
    sub_folder_name = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=5)
    )
    if not ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f'cd /home/{data.get("user_name")}/Test/dir_file; mkdir {sub_folder_name}',
        "",
    ):
        return None, None
    if not ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f'cd /home/{data.get("user_name")}/Test/dir_file/{sub_folder_name}; dd if=/dev/urandom of={test_file_name} bs=1M count=1 iflag=fullblock',
        "",
    ):
        return sub_folder_name, None
    return sub_folder_name, test_file_name


@pytest.fixture(autouse=True)
def time():
    with open("stat.txt", "a", encoding="utf-8") as f:
        res = get_out(f'cat {data["pwd_4"]}').replace("\n", "")
        yield f.writelines(
            f'Время: {datetime.now().strftime("%d-%m-%y %H:%M:%S:%f")} - Статистика загрузки процессора: {res} \n'
        )


if __name__ == "__main__":
    make_folders()
