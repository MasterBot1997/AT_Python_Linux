import yaml

from conftest import *
from checker import checkout

with open('config.yaml', 'r') as f:
    data = yaml.safe_load(f)


#Тест выполненый на семинаре
def test_step_zip(make_name_arh, clear_folders, make_file):
    res1 = checkout(f'cd {data["pwd_fold_1"]}; 7z a {data["pwd_fold_2"]}/{make_name_arh}', 'Everything is Ok')
    res2 = checkout(f'ls {data["pwd_fold_2"]}', make_name_arh)
    assert res1, 'Error zip'
    assert res2, 'Error name zip'

def test_step_unzip(make_folders, make_name_arh, clear_folders, make_file):
    res = []
    res.append(checkout(f'cd {data["pwd_fold_1"]}; 7z a {data["pwd_fold_2"]}/{make_name_arh}', 'Everything is Ok'))
    res.append(checkout(f'cd {data["pwd_fold_2"]}; 7z e {make_name_arh}.7z -o{data["pwd_fold_3"]}', 'Everything is Ok'))
    for item in make_file:
        res.append(checkout(f'ls {data["pwd_fold_3"]}', item))
    
    assert all(res), 'Error unzip file'

def test_zip_key_l(clear_folders, make_file, make_name_arh):
    res = []
    res.append(checkout(f'cd {data["pwd_fold_1"]}; 7z a {data["pwd_fold_2"]}/{make_name_arh}', 'Everything is Ok'))
    for item in make_file:
        res.append(checkout(f'cd {data["pwd_fold_2"]}; 7z l {make_name_arh}.7z', item))
    
    assert all(res), 'Error key -l'

def test_zip_key_u(make_name_arh):
    assert checkout(f'cd {data["pwd_fold_1"]}; 7z u {make_name_arh}', 'Everything is Ok'), 'Error key -u'


def test_zip_key_x(clear_folders, make_file, make_name_arh, make_subfolder):
    res = []
    res.append(checkout(f'cd {data["pwd_fold_1"]}; 7z a {data["pwd_fold_2"]}/{make_name_arh}', 'Everything is Ok'))
    res.append(checkout(f'cd {data["pwd_fold_2"]}; 7z x {make_name_arh}.7z -o{data["pwd_fold_3"]}', 'Everything is Ok'))
    for item in make_file:
        res.append(checkout(f'ls {data["pwd_fold_3"]}', item))
    
    res.append(checkout(f'ls {data["pwd_fold_3"]}', make_subfolder[0]))
    res.append(checkout(f'ls {data["pwd_fold_3"]}/{make_subfolder[0]}', make_subfolder[1]))

    assert all(res), 'Error key -x'




