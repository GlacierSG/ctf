# CTF

## Setup
```bash
mkdir -p ~/.config/ && cd ~/.config/
git clone https://github.com/GlacierSG/ctf.git
```

### For python interactive interpreter
```
export PYTHONSTARTUP="$HOME/.config/ctf/src/ctf/template_default.py"
```
### For scripts
```python
# From https://github.com/GlacierSG/ctf
__import__('sys').path.insert(1,__import__('os').path.expanduser("~/.config/ctf/src/ctf"));
from template_default import *
```
