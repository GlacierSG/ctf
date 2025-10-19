import sys, os
p = os.path.expanduser("~/.config/ctf")
if p not in sys.path:
    sys.path.insert(1, p)
from template_util import *
from template_math import *
