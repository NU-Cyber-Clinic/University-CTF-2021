Analysing the exe in virus total indicates its colbalt strike
https://www.virustotal.com/gui/file/5a27fe712d3aada1694166560b6fd1e60a05f50f5b5d3ce06927c8ba3e0e5290

Doing some searching around for how to decrypt the traffic from it we found the below site which shows how to decrypt the traffic using the pcap and dmp

https://isc.sans.edu/forums/diary/Decrypting+Cobalt+Strike+Traffic+With+Keys+Extracted+From+Process+Memory/28006/

Dump the raw data. We specify an unknown key to get the hex bytes for later use
```
python3 ./cs-parse-http-traffic.py ./forensics_strike_back/capture.pcap -k unknown > http.txt
```
```
Packet number: 217
HTTP response (for request 214 GET)
Length raw data: 80
7076675dbed9bafd4ffcc36ed8d9eecc2bfed095de2439e347aea08157e01978eb7b7cab86bea3d97e7062c9990bf7407ee88eab9ee07bc9761a6371323f285bba8c2d1d4b4a04a09655d675e3ac7e8e
```

Pass the dumped hex bytes along with the dmp file to find the key
```
python3 cs-extract-key.py ./forensics_strike_back/freesteam.dmp -t 7076675dbed9bafd4ffcc36ed8d9eecc2bfed095de2439e347aea08157e01978eb7b7cab86bea3d97e7062c9990bf7407ee88eab9ee07bc9761a6371323f285bba8c2d1d4b4a04a09655d675e3ac7e8e
```
```
File: ./forensics_strike_back/freesteam.dmp
Searching for AES and HMAC keys
Searching after sha256\x00 string (0x4048a)
AES key position: 0x00447f81
AES Key:  3ae7f995a2392c86e3fa8b6fbc3d953a
HMAC key position: 0x0044b2a1
HMAC Key: bf2d35c0e9b64bc46e6d513c1d0f6ffe
SHA256 raw key: bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a
Searching for raw key
Searching after sha256\x00 string (0x441a49)
AES key position: 0x00447f81
AES Key:  3ae7f995a2392c86e3fa8b6fbc3d953a
HMAC key position: 0x0044b2a1
HMAC Key: bf2d35c0e9b64bc46e6d513c1d0f6ffe
Searching for raw key
```

Using the key found we can dump the unencrypted traffic
```
bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a
```
```
python3 ./cs-parse-http-traffic.py ./forensics_strike_back/capture.pcap -k bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a > http.decrypt.txt
```

Looking through the traffic we dont find anything of intrest other than a download for a `C:\Users\npatrick\Desktop\orders.pdf`. So then using the `-e` flag to extract the files we can dump it and then rename to open and get the flag.

```
python3 ./cs-parse-http-traffic.py ./forensics_strike_back/capture.pcap -k bf2d35c0e9b64bc46e6d513c1d0f6ffe:3ae7f995a2392c86e3fa8b6fbc3d953a -e
mv payload-00f542efefccd7a89a55c133180d8581.vir payload-00f542efefccd7a89a55c133180d8581.pdf
```
```
HTB{Th4nk_g0d_y0u_f0und_1t_0n_T1m3!!!!}
```