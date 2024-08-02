import paramiko
from datetime import date

# 服务器地址和账户名密码列表
servers = [
    {"hostname": "", "username": "", "password": ""},
]

# 定义要执行的多个命令
commands = [
    "uptime",
    "df -h",
    "free -m",
    "netstat -ant",
    "tail -n 20 /var/log/syslog",
    "ps aux --sort=%cpu | head -n 10",
    "mount | column -t | head -n 10",
    "ip addr show",
    "who",
    "date",
    "w"
]


def ssh_command(hostname, username, password, command):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # 连接服务器
        client.connect(hostname=hostname, username=username, password=password)
        # 执行命令
        stdin, stdout, stderr = client.exec_command(command)
        # 读取命令执行结果
        output = stdout.read().decode('utf-8')
        # 关闭连接
        client.close()
        return output
    except Exception as e:
        print(f"Error executing SSH command on {hostname}: {str(e)}")
        return None


def main():
    today = date.today().strftime("%Y-%m-%d")
    for server in servers:
        hostname = server["hostname"]
        username = server["username"]
        password = server["password"]
        output_filename = f"{today}_{hostname}.txt"
        print(f"Checking server {hostname}...")
        for command in commands:
            print(f"Executing command: {command}")
            result = ssh_command(hostname, username, password, command)
            with open(output_filename, 'w') as f:
                f.write(f"===== {hostname} =====\n")
                if result:
                    f.write(f"=== Command: {command} ===\n")
                    f.write(result)
                    f.write("\n\n")
                else:
                    f.write(f"=== Command: {command} failed ===\n")
                    f.write("\n\n")
        print(f"Output saved to {output_filename}")


if __name__ == "__main__":
    main()
