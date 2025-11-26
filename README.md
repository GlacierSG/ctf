# CTF
## Usage
```python
# pip install git+https://github.com/GlacierSG/ctf.git
from ctf import *

install('pwntools')
from pwn import *

dbg(l2b(1337))

s = getclient(proxy=True) # httpx client
r = dbg(s.get('https://example.com'))
print(urle(py2json(r.json())))
```

