from .util_math import *
from dataclasses import dataclass


@dataclass(slots=True)
class Enumerate():
    ip: str
    
    def __post_init__(self):
        if not self.ip:
            raise ValueError("Enumerate needs to have an ip")
    def _run_comand(cmd):
        out = subprocess.run(cmd, capture_output=True)
        if out.returncode == 0:
            return out.stdout
        else:
            print(f"\033[1;31m[STDERR]\033[0m {''.join(cmd)} resulted in {out.stderr}", file=sys.stderr)


Enumerate.nmap_fast = lambda self: \
    self._run_command(['nmap', self.ip]).split('\n')
