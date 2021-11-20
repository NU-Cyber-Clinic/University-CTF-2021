# User
Nmap reveals port 80, hitting that gives a link to http://object.htb:8080/ which is a jenkins interface

Creating an account on the jenkins instance gives you access to create jobs but not trigger builds via the interface
So we create a job and allow builds to be triggered remotely. 
With remote builds being enabled we can trigger the build using http://object.htb:8080/job/test/build?token=123

We also need to add a build action to execute a bash command which below will give us the flag
```
type C:\Users\oliver\Desktop\user.txt
```
```
HTB{c1_cd_c00k3d_up_1337!}
```
