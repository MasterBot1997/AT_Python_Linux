import subprocess

def checkout(command, text):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout

    if result.returncode == 0:
        if text in out:
            return True
        return False
    return False

def get_out(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    return result



if __name__ == '__main__':
    print(get_out(f'ls -l'))