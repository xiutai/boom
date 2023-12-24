# mysql or ssh or mssql boom

### boom.py -h 帮助命令:
```
boom.py -h
usage: boom.py [-h] [-u U] [-ul UL] [-p P] [-pl PL] [-ip IP] [-il IL] [-port PORT] [-key KEY] [-m M] [-o O] [-t T] [-log LOG]

write value

options:
  -h, --help  show this help message and exit
  -u U        user
  -ul UL      user file
  -p P        pass
  -pl PL      pass file
  -ip IP      192.168.0.1 or 192.168.0.1/24
  -il IL      ip or domain or ip:port file
  -port PORT  port
  -key KEY    ssh key file path
  -m M        mysql or mssql or ssh
  -o O        out file
  -t T        threads
  -log LOG    0:none, 1:memory, 2,file
```
### boom.py -h 帮助命令（中文）:
```
usage: boom.py [-h] [-u U] [-ul UL] [-p P] [-pl PL] [-ip IP] [-il IL] [-port PORT] [-key KEY] [-m M] [-o O] [-t T] [-log LOG]

write value

options:
  -h, --help  显示帮助信息并退出
  -u U        指定用户
  -ul UL      指定用户文件
  -p P        指定密码
  -pl PL      指定密码文件
  -ip IP      指定目标IP地址或IP地址范围 (例如：192.168.0.1 或 192.168.0.1/24)
  -il IL      指定IP地址、域名或IP地址与端口的文件
  -port PORT  指定端口号
  -key KEY    指定SSH密钥文件路径
  -m M        指定操作模式 (可以是 "mysql"、"mssql" 或 "ssh")
  -o O        指定输出爆破成功的记录到文件
  -t T        指定线程数
  -log LOG    指定日志记录方式 (0:不记录日志, 1:写入内存, 2:写入文件)
```
#
### 爆破指定ip地址的c段ssh协议：
```
boom.py -ip 127.0.0.1/24 -m ssh -pl pwd.txt

```
#
### 爆破指定ip mysql协议：
```
boom.py -ip 127.0.0.1 -m mysql -pl pwd.txt

```
#
### 爆破指定ip mssql协议：
```
boom.py -ip 127.0.0.1 -m mssql -pl pwd.txt

```
#
### 批量爆破ssh（格式  ip:port or domain:port file）：
```
boom.py -il ip.txt -m ssh -ul user.txt -pl pwd.txt -t 50

```
#
### 批量爆破某个协议的时候，ip列表文件格式可以混合这样写入：
如果ip列表中没有指定端口，就会根据-port 参数的端口号，如果没有指定-port参数就会根据协议默认端口爆破
```
192.168.0.1
192.168.0.1:22
google.com
google.com:22
```
