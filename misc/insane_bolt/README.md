Connecting the server using netcat reveals a simple menu with that we can see the instructions of the challenge

These state that we need to solve the maze by collecting wrenches and ending up and the diamond along with the input format

So if we then attempt to solve the maze by hand we get a message saying we were too slow or wrong, so script time.

Looking about for an ascii maze solver I came accross https://gist.github.com/Tak31337/5314032 which with some minor modifications can solve our maze

So then I pulled in the pwntools library and wrote some quick handling code to connect to the server parse the data and feed it to the solver.
Running that and waiting a few mins for it to solve 500 mazes and then we get the flag :)


```
$ nc 64.227.38.214 31758

1. Instructions
2. Play
> 1

🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 
🔩                                                                            🔩
🔩  [*] Help the 🤖 reach the 💎.                                             🔩
🔩  [*] You need to find the shortest route.                                  🔩
🔩  [*] You need to collect 500 💎 and at least 5000 🔩.                      🔩
🔩  [*] The solution should be given in the format: DLR (Down, Left, Right)   🔩
🔩                                                                            🔩
🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 

1. Instructions
2. Play
> 2

🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 
🔥 ☠  ☠  ☠  ☠  ☠  ☠  🤖 ☠  ☠  ☠  ☠  🔥 
🔥 ☠  ☠  ☠  🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔩 🔥 
🔥 ☠  ☠  ☠  🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  🔩 🔩 🔩 🔩 🔩 ☠  ☠  ☠  ☠  ☠  🔥 
🔥 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  🔩 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  🔩 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  🔩 🔩 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  ☠  ☠  🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  ☠  ☠  🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 🔩 🔩 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  ☠  ☠  🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  ☠  ☠  🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 🔩 🔩 🔩 🔩 ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 ☠  💎 ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  ☠  🔥 
🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 🔥 

> 

[-] Wrong answer or time limit exceeded!
```
...
```
[+] You have 500 💎!

[+] You have 10129 🔩 !

[+] Congratulations! This is your reward!

HTB{w1th_4ll_th353_b0lt5_4nd_g3m5_1ll_cr4ft_th3_b35t_t00ls}
```