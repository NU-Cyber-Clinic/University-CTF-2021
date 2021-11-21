Looking over the downloaded code we cant run any functions directly due the the name needing to be part of the `math` library

But due to a bug with how the dictionaries are handled we can run anything

This checks if the key is not safe and the value is but due to it being an `and` we can just have a safe key and the rest of the check is ignored.
```py
if not is_expression_safe(k) and is_expression_safe(v):
```

Meaning that if we do something as simple as this we get the flag
```py
{"1":open('flag.txt').read()}
```