import argparse
import pymysql
import concurrent.futures
import paramiko
import pyodbc
import ipaddress


parser = argparse.ArgumentParser(description='write value')
parser.add_argument('-u', default='root', type=str, help='user')
parser.add_argument('-ul', default='', type=str, help='user file')
parser.add_argument('-p', default='123456', type=str, help='pass')
parser.add_argument('-pl', default='', type=str, help='pass file')
parser.add_argument('-port', default=3306, type=int, help='port')
parser.add_argument('-ipf', default='', type=str, help='ip or domain file')
parser.add_argument('-ipp', default='', type=str, help='ip:port or domain:port file')
parser.add_argument('-ip', default='127.0.0.1', type=str, help='192.168.0.1 or 192.168.0.1/24')
parser.add_argument('-key', default='', type=str, help='ssh key file path')
parser.add_argument('-m', default='mysql', type=str, help='mysql or mssql or ssh')
parser.add_argument('-o', default='ok.txt', type=str, help='out file')
parser.add_argument('-t', default=10, type=int, help='threads')
args = parser.parse_args()
# 初始化参数
mod=args.m
port_mapping = {"mysql": 3306, "ssh": 22, "mssql": 1433}
ip, user, pwd = [], [], []
if '/' in args.ip:
    try:
        ip_network = ipaddress.IPv4Network(args.ip, strict=False)
        ip = [str(ip) for ip in ip_network.hosts()]
    except ipaddress.AddressValueError:
        print(f"Invalid CIDR format for -ip: {args.ip}")
        exit(1)
ip = [args.ip] if args.ipf == '' else open(args.ipf, "r").read().strip().split('\n')
ip = [args.ip] if args.ipp == '' else open(args.ipp, "r").read().strip().split('\n')
user = [args.u] if args.ul == '' else open(args.ul, "r").read().strip().split('\n')
pwd = [args.p] if args.pl == '' else open(args.pl, "r").read().strip().split('\n')
port = port_mapping.get(mod, None)
def write(data):
    with open(args.o,'a+',encoding='utf-8') as f:
        f.writelines(data+'\n')

def mysql_login():
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.t) as executor:
        # 使用嵌套循环生成所有可能的(i, u, p)组合
        for i in ip:
            for u in user:
                for p in pwd:
                    # 提交任务给线程池并异步执行mysql_run
                    executor.submit(mysql_run, i, u, p)

def mysql_run(i,u,p):
    try:
        # 尝试连接到MySQL数据库
        mysql_host=i.split(':')[0] if ':' in i else i
        mysql_port=int(i.split(':')[1]) if ':' in i else port
        connection = pymysql.connect(
            host = mysql_host,
            port=mysql_port,
            user=u,
            password=p,
            connect_timeout=10
        )
        
        # 如果成功连接，打印登录成功消息
        print(f"mod:{mod}, ip:{mysql_host}, port:{str(mysql_port)} --> user:{u}, pwd:{p}")
        write(f"mod:{mod}, ip:{mysql_host}, port:{str(mysql_port)} --> user:{u}, pwd:{p}")

    except pymysql.Error as e:
        # 如果登录失败，打印错误消息
        print(f"mod:{mod}, ip:{mysql_host}, port:{str(mysql_port)} --> user:{u}, pwd:{p}, Login failed: {e}")

    finally:
        # 关闭数据库连接
        if connection:
            connection.close()


def ssh_login():
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.t) as executor:
        # 使用嵌套循环生成所有可能的(i, u, p)组合
        for i in ip:
            for u in user:
                for p in pwd:
                    # 提交任务给线程池并异步执行mysql_run
                    executor.submit(ssh_run, i, u, p)

def ssh_run(i,u,p):
    try:
        # 创建SSH客户端对象
        ssh_client = paramiko.SSHClient()
        ssh_hostname = i.split(':')[0] if ':' in i else i
        ssh_port = int(i.split(':')[1]) if ':' in i else port
        # 自动添加主机密钥（仅用于测试，实际生产环境中应谨慎）
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if args.key !='':
            private_key = paramiko.RSAKey(filename=args.key)
            # 连接到SSH服务器
            ssh_client.connect(
                hostname=ssh_hostname,
                port=ssh_port,
                username=u,
                pkey=private_key,
                banner_timeout=10,  # 设置超时时间
                gss_auth=False,  # 禁用GSS认证
                gss_kex=False,  # 禁用GSS交换
                look_for_keys=False,  # 禁用查找SSH密钥
                allow_agent=False,  # 禁用SSH代理
                ssh_version='2'  # 指定SSH协议版本
            )
        else:
                ssh_client.connect(
                hostname=ssh_hostname,
                port=ssh_port,
                username=u,
                password=p,
                banner_timeout=10,  # 设置超时时间
                gss_auth=False,  # 禁用GSS认证
                gss_kex=False,  # 禁用GSS交换
                look_for_keys=False,  # 禁用查找SSH密钥
                allow_agent=False,  # 禁用SSH代理
                ssh_version='2'  # 指定SSH协议版本
            )

        # 如果成功连接，打印登录成功消息
        print(f"mod:{mod}, ip:{ssh_hostname}, port:{str(ssh_port)} --> user:{u}, pwd:{p if args.key ==''else private_key}")
        write(f"mod:{mod}, ip:{ssh_hostname}, port:{str(ssh_port)} --> user:{u}, pwd:{p if args.key ==''else private_key}")

    except paramiko.AuthenticationException:
        print(f"mod:{mod}, ip:{ssh_hostname}, port:{str(ssh_port)} --> user:{u}, pwd:{p if args.key ==''else private_key}, Authentication failed, please check your credentials.")
    except paramiko.SSHException as e:
        print(f"mod:{mod}, ip:{ssh_hostname}, port:{str(ssh_port)} --> user:{u}, pwd:{p if args.key ==''else private_key}, SSH connection failed: {e}")
    except Exception as e:
        print(f"mod:{mod}, ip:{ssh_hostname}, port:{str(ssh_port)} --> user:{u}, pwd:{p if args.key ==''else private_key}, Error: {e}")
    finally:
        # 关闭SSH连接
        if ssh_client:
            ssh_client.close()

def mssql_login():
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.t) as executor:
        # 使用嵌套循环生成所有可能的(i, u, p)组合
        for i in ip:
            for u in user:
                for p in pwd:
                    # 提交任务给线程池并异步执行mysql_run
                    executor.submit(mssql_run, i, u, p)

def mssql_run(i,u,p):
    # MSSQL连接参数
    server = i.split(':')[0] if ':' in i else i,
    port = int(i.split(':')[1]) if ':' in i else port,
    username = u,
    password = p,

    # 构建连接字符串，包括端口号
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},{str(port)};UID={username};PWD={password}'
    try:
        # 尝试连接到MSSQL数据库
        connection = pyodbc.connect(conn_str)
        
        # 如果成功连接，打印登录成功消息
        print(f"mod:{mod}, ip:{server}, port:{str(port)} --> user:{u}, pwd:{p}, Login successful")

    except pyodbc.Error as e:
        # 如果登录失败，打印错误消息
        print(f"mod:{mod}, ip:{server}, port:{str(port)} --> user:{u}, pwd:{p}, Login failed: {e}")
    finally:
        # 关闭数据库连接
        if connection:
            connection.close()

print(f'try login {mod}:\n\nip={ip}\n\nuser={user}\n\npwd={pwd}\n\n')
if args.m =='mysql':
    mysql_login()
if args.m =='ssh':
    ssh_login()
if args.m =='mssql':
    mssql_login()
