# mysql or ssh or mssql boom

### boom.py -h 帮助命令:
```
boom.py -h
usage: boom.py [-h] [-u U] [-ul UL] [-p P] [-pl PL] [-ip IP] [-il IL] [-port PORT] [-key KEY] [-m M] [-o O] [-t T]

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
