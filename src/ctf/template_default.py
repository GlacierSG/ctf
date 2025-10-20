import sys, os
p = os.path.expanduser("~/.config/ctf/src/ctf")
if p not in sys.path:
    sys.path.insert(1, p)
from setup_venv import *

from importlib.metadata import version, PackageNotFoundError
def isinstalled(modules):
    if isinstance(modules, str):
        modules = [modules]
    
    found = True
    for module in modules:
        try:
            version(module)
        except PackageNotFoundError:
            found = False
    return found

run_shell = lambda cmd: subprocess.run(cmd, shell=True, capture_output=True) # x.stdout, x.stderr, x.returncode
if not isinstalled('ctf'):
    out = (run_shell([f"{VENV_PATH}/bin/python -m pip install ~/.config/ctf/"]))
    if out.returncode != 0:
        raise Exception(f'Could not install ctf: {out.stderr.decode()}')
from ctf import *
