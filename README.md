# mysql or ssh boom

### boom.py -h 帮助命令:
```
python3 boom.py -h
usage: boom.py [-h] [-u U] [-ul UL] [-p P] [-pl PL] [-port PORT] [-ipf IPF] [-ipp IPP] [-ip IP] [-key KEY] [-m M] [-o O] [-t T]

write value

optional arguments:
  -h, --help  show this help message and exit
  -u U        user
  -ul UL      user file
  -p P        pass
  -pl PL      pass file
  -port PORT  port
  -ipf IPF    ip or domain file
  -ipp IPP    ip:port or domain:port file
  -ip IP      ip address
  -key KEY    ip address
  -m M        mysql or ssh
  -o O        out file
  -t T        threads
```
#
### 爆破指定ip ssh协议：
```
python3 boom.py -ip 127.0.0.1 -m ssh -pl pwd.txt

```
#
### 爆破指定ip mysql协议：
```
python3 boom.py -ip 127.0.0.1 -m mysql -pl pwd.txt

```
### 批量爆破ssh（格式  ip:port or domain:port file）：
```
python3 boom.py -ipp ip.txt -m ssh -ul user.txt -pl pwd.txt -t 50

```
