import yaml

from conftest import *
from checker import upload_files, ssh_checkout

with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

path_test_folder = f'/home/{data.get("user_name")}/{data.get("test_folder_name")}/'


# тест установки пакета
def test_deploy():
    res = []
    upload_files(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        data.get("path_file"),
        data.get("path_user2"),
    )
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"echo {data.get('password')} | sudo -S dpkg -i {data.get('path_user2')}",
            "Настраивается пакет",
        )
    )
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"echo {data.get('password')} | sudo -S dpkg -s {data.get('program')}",
            "Status: install ok installed",
        )
    )
    assert all(res), "Деплой не успешен"


# тест архивации файлов
def test_step_zip(clear_folders, make_folders, make_name_arh, make_file):
    res1 = ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f"cd {path_test_folder}dir_file; 7z a {path_test_folder}dir_zip/{make_name_arh}",
        "Everything is Ok",
    )
    res2 = ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f"ls {path_test_folder}dir_zip",
        make_name_arh,
    )
    assert res1, "Error zip"
    assert res2, "Error name zip"


# тест разархивирования файлов
def test_step_unzip(clear_folders, make_folders, make_name_arh, make_file):
    res = []
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"cd {path_test_folder}dir_file; 7z a {path_test_folder}dir_zip/{make_name_arh}",
            "Everything is Ok",
        )
    )
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"cd {path_test_folder}dir_zip; 7z e {make_name_arh}.7z -o{path_test_folder}dir_unzip",
            "Everything is Ok",
        )
    )
    for item in make_file:
        res.append(
            ssh_checkout(
                data.get("ip"),
                data.get("user_name"),
                data.get("password"),
                f"ls {path_test_folder}dir_unzip",
                item,
            )
        )

    assert all(res), "Error unzip file"


# тест ключа l
def test_zip_key_l(clear_folders, make_folders, make_file, make_name_arh):
    res = []
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"cd {path_test_folder}dir_file; 7z a {path_test_folder}dir_zip/{make_name_arh}",
            "Everything is Ok",
        )
    )
    for item in make_file:
        res.append(
            ssh_checkout(
                data.get("ip"),
                data.get("user_name"),
                data.get("password"),
                f"cd {path_test_folder}dir_zip; 7z l {make_name_arh}.7z",
                item,
            )
        )

    assert all(res), "Error key -l"


# тест ключа u
def test_zip_key_u(make_name_arh):
    assert ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f"cd {path_test_folder}dir_file; 7z u {make_name_arh}",
        "Everything is Ok",
    ), "Error key -u"


# тест ключа x
def test_zip_key_x(
    clear_folders, make_folders, make_file, make_name_arh, make_subfolder
):
    res = []
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"cd {path_test_folder}dir_file; 7z a {path_test_folder}dir_zip/{make_name_arh}",
            "Everything is Ok",
        )
    )
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"cd {path_test_folder}dir_zip; 7z x {make_name_arh}.7z -o{path_test_folder}dir_unzip",
            "Everything is Ok",
        )
    )
    for item in make_file:
        res.append(
            ssh_checkout(
                data.get("ip"),
                data.get("user_name"),
                data.get("password"),
                f"ls {path_test_folder}dir_unzip",
                item,
            )
        )

    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"ls {path_test_folder}dir_unzip",
            make_subfolder[0],
        )
    )
    res.append(
        ssh_checkout(
            data.get("ip"),
            data.get("user_name"),
            data.get("password"),
            f"ls {path_test_folder}dir_unzip/{make_subfolder[0]}",
            make_subfolder[1],
        )
    )

    assert all(res), "Error key -x"


# тест удаления пакета
def test_del_7z(clear_folders):
    assert ssh_checkout(
        data.get("ip"),
        data.get("user_name"),
        data.get("password"),
        f"echo {data.get('password')} | sudo -S dpkg -r {data.get('program')}",
        "Удаляется",
    ), "Пакет не удален"
