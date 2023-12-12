import subprocess

def func(command, text):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout

    if result.returncode == 0:
        if text in out:
            return True
        return False
    return False

def func_del_arh(command):
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')


if __name__ == '__main__':
    val_1 = 'cd ~/shared/AT_Python_Linux/HW_2/test_step_zip/fold_1; 7z a ../fold_2/arch_fold_1'
    # val_1 = 'cd ~/shared/AT_Python_Linux/HW_2/test_step_zip/fold_2; 7z h'
    # val_1 = 'cat /etc' # Проверка на ложь
    val_2 = 'Everything is Ok'
    # val_2 = '1 file, 265 bytes (1 KiB)'
    print(func(val_1, val_2))
    # func_del('cd ~/shared/AT_Python_Linux/HW_2/test_step_zip/fold_2; rm ./arch_fold_1.7z')