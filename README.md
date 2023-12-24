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
```
-h, --help: 显示帮助信息，列出了所有可用选项和它们的说明。

-u U: 指定用户。你需要提供一个用户名作为参数，例如：-u username。

-ul UL: 指定用户文件。你可以提供一个包含多个用户名的文件作为参数，每行一个用户名，例如：-ul userfile.txt。

-p P: 指定密码。你需要提供密码作为参数，例如：-p password。

-pl PL: 指定密码文件。你可以提供一个包含多个密码的文件作为参数，每行一个密码，例如：-pl passwordfile.txt。

-ip IP: 指定目标IP地址或IP地址范围。你可以提供单个IP地址或CIDR表示的IP地址范围，例如：-ip 192.168.0.1 或 -ip 192.168.0.1/24。

-il IL: 指定IP地址、域名或IP地址与端口的文件。你可以提供一个文件，其中包含多个IP地址、域名或IP地址与端口的组合，例如：-il targets.txt。

-port PORT: 指定端口号。你需要提供一个端口号作为参数，例如：-port 22。

-key KEY: 指定SSH密钥文件路径。如果你选择了SSH连接模式，你需要提供SSH密钥文件的路径，例如：-key /path/to/ssh/key。

-m M: 指定操作模式。你需要选择一种操作模式，可以是"mysql"、"mssql"或"ssh"之一，例如：-m mysql。

-o O: 指定输出文件。你可以提供一个文件路径，用于将输出结果保存到文件中，例如：-o output.txt。

-t T: 指定线程数。你可以设置线程数，以控制并发执行的任务数量，例如：-t 4
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
