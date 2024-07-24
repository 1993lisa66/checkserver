import paramiko
import datetime

# 服务器信息
servers = [
    {
        'name': 'Server1',
        'host': 'server1.example.com',
        'username': 'your_username',
        'password': 'your_password',
        'port': 22
    },
    {
        'name': 'Server2',
        'host': 'server2.example.com',
        'username': 'your_username',
        'password': 'your_password',
        'port': 22
    }
]

# 定义要执行的命令和对应的标题
commands = [
    ("find / -type f -size 0 -exec rm {} \;", "Deleting 0-byte files"),
    ("ps aux --sort=-%mem", "Top processes by memory usage"),
    ("mount | column -t", "Mounted filesystems"),
    ("fdisk -l", "Disk partitions"),
    ("swapon -s", "Swap spaces in use"),
    ("hdparm -I /dev/sda", "Disk parameters for /dev/sda"),  # 根据需要调整设备
    ("dmesg | grep -i 'sda\|hda'", "IDE/SATA device detection at boot"),
    ("ip a", "Network interfaces"),
    ("iptables -L", "Firewall settings"),
    ("route -n", "Routing table"),
    ("netstat -lntp", "Listening ports"),
    ("netstat -antp", "Established connections"),
    ("netstat -s", "Network statistics"),
    ("cat /var/log/messages | grep -i 'error\|exception'", "System log errors"),  # 根据实际日志路径调整
    ("systemctl list-units --type=service --state=running", "Running services"),
    ("systemctl list-units --type=service --state=inactive", "Inactive services"),
    ("top -b -n 1 | head -n 20", "Top 20 processes by CPU"),
    ("df -h", "Disk usage"),
    ("du -sh * | sort -rh | head -n 10", "Top 10 directories by size"),
    ("iostat -x 1 2", "Disk I/O load"),
    ("ps aux | wc -l", "Number of processes"),
    ("sar -n DEV", "Network load"),
    ("netstat -i || cat /proc/net/dev", "Network errors"),
    ("who | wc -l || uptime", "Logged in users and system uptime"),
    ("ps -e -o %cpu,%pid,%mem,args | sort -nr", "Processes by CPU usage"),
    ("free -h", "Memory space"),
]

def execute_commands(server):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server['host'], port=server['port'], username=server['username'], password=server['password'])

    # 创建文件名，包含服务器名称和当前日期
    filename = f"{server['name']}_{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"

    with open(filename, "w") as file:
        file.write(f"Server: {server['name']}\n")
        for command, header in commands:
            file.write(f"\n=== {header} ===\n")
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode('utf-8')
            errors = stderr.read().decode('utf-8')
            
            if errors:
                file.write(f"Errors:\n{errors}\n")
            else:
                file.write(f"{output}\n")

    client.close()
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    for server in servers:
        execute_commands(server)
