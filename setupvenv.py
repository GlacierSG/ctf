import sys, os, subprocess

def _python_dir():
    return (getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix)
def is_virtualenv():
    base = _python_dir()
    # Fix for Nixos 
    if base.startswith('/nix/store'):
        return False
    return sys.prefix != base 

if is_virtualenv():
    VENV_PATH = sys.prefix
else:
    VENV_PATH = os.path.expanduser(f"~/.cache/ctf/venv{sys.version_info.major}.{sys.version_info.minor}")
    if not os.path.isdir(VENV_PATH):
        subprocess.check_call([sys.executable, "-m", "venv", VENV_PATH])

    sp = f"{VENV_PATH}/lib/python{sys.version_info.major}.{sys.version_info.minor}/site-packages"
    if sp not in sys.path:
        sys.path.insert(0, sp)

    sys.base_prefix = VENV_PATH

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
    out = (run_shell([f"{VENV_PATH}/bin/python{sys.version_info.major} -m pip install ~/.config/ctf/"]))
    if out.returncode != 0:
        raise Exception(f'Could not install ctf: {out.stderr.decode()}')

from ctf import *
