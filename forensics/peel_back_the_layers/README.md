First pull the image
```
docker pull steammaintainer/gearrepairimage 
```

Dump out the image
```
docker save steammaintainer/gearrepairimage
```

Get the image history 
```
docker image history steammaintainer/gearrepairimage --no-trunc
```
```
IMAGE                                                                     CREATED       CREATED BY                                                                                                                 SIZE      COMMENT
sha256:47f41629f1cfcaf8890339a7ffdf6414c0c1417cfa75481831c8710196627d5d   6 days ago    /bin/sh -c #(nop)  CMD ["bin/bash" "-c" "/bin/bash"]                                                                       0B        
<missing>                                                                 6 days ago    /bin/sh -c rm -rf /usr/share/lib/                                                                                          0B        
<missing>                                                                 6 days ago    /bin/sh -c #(nop)  CMD ["bin/bash" "-c" "/bin/bash"]                                                                       0B        
<missing>                                                                 6 days ago    /bin/sh -c #(nop)  ENV LD_PRELOAD=                                                                                         0B        
<missing>                                                                 6 days ago    /bin/sh -c #(nop)  CMD ["bin/bash" "-c" "/bin/bash"]                                                                       0B        
<missing>                                                                 6 days ago    /bin/sh -c #(nop)  ENV LD_PRELOAD=/usr/share/lib/librs.so                                                                  0B        
<missing>                                                                 6 days ago    /bin/sh -c #(nop) COPY file:0b1afae23b8f468ed1b0570b72d4855f0a24f2a63388c5c077938dbfdeda945c in /usr/share/lib/librs.so    16.4kB    
<missing>                                                                 6 days ago    /bin/sh -c #(nop)  CMD ["bin/bash" "-c" "/bin/bash"]                                                                       0B        
<missing>                                                                 4 weeks ago   /bin/sh -c #(nop)  CMD ["bash"]                                                                                            0B        
<missing>                                                                 4 weeks ago   /bin/sh -c #(nop) ADD file:5d68d27cc15a80653c93d3a0b262a28112d47a46326ff5fc2dfbf7fa3b9a0ce8 in /                           72.8MB    

```

We can then look back in the dumped out image to try and find the layer with the strange `/usr/share/lib/librs.so`
That is in `/image/011c8322f085501548c8d04da497c2d7199f9599e9c02b13edd7a8bbb0f8ee77/usr/share/lib/`
Running strings on that gives a slightly corupted flag, then clean that up
```
HTB{1_r3H4lly_l1kH3_st34mpHunk_r0b0Hts!!!}

HTB{1_r34lly_l1k3_st34mpunk_r0b0ts!!!}
```