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
print(py2json(r.json()))
```

## Local Setup
```bash
mkdir -p ~/.config/ && cd ~/.config/
git clone https://github.com/GlacierSG/ctf.git
python3 ~/.config/ctf/src/ctf/template_default.py
source ~/.cache/ctf/venv*/bin/activate
```

### For python interactive interpreter
```
export PYTHONSTARTUP="$HOME/.config/ctf/src/ctf/template_default.py"
```
