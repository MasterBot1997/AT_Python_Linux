import subprocess

def func(command, text):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout

    if result.returncode == 0:
        if text in out:
            return True
        return False
    return False

if __name__ == '__main__':
    val_1 = 'cat /etc/os-release'
    # val_1 = 'cat /etc' # Проверка на ложь
    val_2 = '22.04'
    print(func(val_1, val_2))