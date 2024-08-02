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



def ssh_command(hostname, username, password):
    # 创建SSH客户端
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password)
        results = {}
        for command in commands:
            print(f"Executing command: {command}")
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')
            results[command] = output
        # 关闭连接
        client.close()
        return results
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
        result = ssh_command(hostname, username, password)
        if result:
            with open(output_filename, 'w') as f:
                for command, output in result.items():
                    f.write(f"=== Command: {command} ===\n")
                    f.write(output)
                    f.write("\n\n")
            print(f"Output saved to {output_filename}")
        else:
            f.write(f"Failed to execute commands on {hostname}\n\n")

if __name__ == "__main__":
    main()
