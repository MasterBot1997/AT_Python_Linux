import subprocess
import paramiko

def ssh_checkout(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stin, stout, sterr = client.exec_command(cmd)
    exiit_code = stout.channel.recv_exit_status()
    out = (stout.read() + sterr.read()).decode('utf-8')
    client.close()
    if text in out and exiit_code == 0:
        return True
    else:
        return False
    

def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f'Загружаем файл {local_path} в каталог {remote_path}')
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close
    if transport:
        transport.close()

def get_out(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    return result



if __name__ == '__main__':
    print(get_out(f'ls -l'))