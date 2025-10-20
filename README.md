# CTF

# Dependencies
Install `git`, `python3`, `python3-venv`
## Ubuntu
```
apt update
apt install -y git python3 python3-venv
```

## Usage
```python
# pip install git+https://github.com/GlacierSG/ctf.git
from ctf import *

install('pwntools')
from pwn import *

dbg(l2b(1337))

s = getsession(proxy=True)
r = dbg(s.get('https://example.com'))
print(urle(py2json(r.json())))
```

## Local Setup
```bash
mkdir -p ~/.config/ && cd ~/.config/
git clone https://github.com/GlacierSG/ctf.git
python3 ~/.config/ctf/setupvenv.py
source ~/.cache/ctf/venv*/bin/activate
```
### For scripts
So you dont have to think about virtual environments
```python
import os, runpy ### https://github.com/GlacierSG/ctf
(_path:=os.path.expanduser("~/.config/ctf/setupvenv.py"), \
 runpy.run_path(_path) if os.path.exists(_path) else None)

from ctf import *
```
### For python interactive interpreter
```
export PYTHONSTARTUP="$HOME/.config/ctf/setupvenv.py"
```
