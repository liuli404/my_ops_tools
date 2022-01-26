import paramiko


def exec_ssh_command(ssh_command):
    # 实例化SSHClient
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    # 连接服务器
    ssh.connect(
        hostname='192.168.1.11',
        port=22,
        username='root',
        password='baikang@123',
        timeout=5
    )
    # 执行命令
    stdin, stdout, stderr = ssh.exec_command(ssh_command)
    result = stdout.read().decode('utf-8')
    ssh.close()
    return result


if __name__ == '__main__':
    print(exec_ssh_command('ls /root'))
