import sys, os, subprocess

def _get_base_prefix_compat():
    return (getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix)
def is_virtualenv():
    base = _get_base_prefix_compat()
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
