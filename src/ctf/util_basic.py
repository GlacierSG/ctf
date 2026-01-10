import sys, os, string, re, base64, json, subprocess, itertools, random, secrets, time
from importlib.metadata import version, PackageNotFoundError
from multiprocessing import Process as _Process, Queue as _Queue
import importlib

def _checkall(args, checktype):
    for x in args:
        assert isinstance(x, checktype), f"Expected {str(x)} to be {checktype}"
    if len(args) == 1:
        return args[0]
    elif len(args) == 0:
        return None
    return args

def asiter(*args):
    for x in args:
        assert hasattr(x, '__iter__'), f"Expected {str(x)} to be iterable"
    if len(args) == 1:
        return args[0]
    elif len(args) == 0:
        return None
    return args

asint = lambda *args: _checkall(args, int)
asstr = lambda *args: _checkall(args, str)
asbytes = lambda *args: _checkall(args, bytes)
aslist = lambda *args: _checkall(args, list)


def isinstalled(modules):
    if isinstance(modules, str):
        modules = [modules]
    
    found = True
    for module in modules:
        if importlib.util.find_spec(module) is None:
            try:
                version(module)
            except PackageNotFoundError:
                found = False
    return found

class MissingDependency:
    def __init__(self, package, instruction, installerr):
        self.__installerr = installerr
        self.__instruction = instruction
        self.__package= package
    def __call__(self, *args):
        instruction = f"\ninstall using\n{self.__instruction}" if self.__instruction is not None else ''
        raise RuntimeError(f"{self.__installerr}{instruction}")
    def __getattribute__(self, name):
        if name in ['_MissingDependency__installerr', '_MissingDependency__instruction', '_MissingDependency__package']:
            return object.__getattribute__(self, name.replace('_MissingDependency',''))
        instruction = f"\ninstall using\n{self.__instruction}" if self.__instruction is not None else ''
        raise RuntimeError(f"{self.__installerr}{instruction}")

    def __setattr__(self, name, value):
        if name in ['_MissingDependency__installerr', '_MissingDependency__instruction', '_MissingDependency__package']:
            object.__setattr__(self, name.replace('_MissingDependency',''), value)
            return
        instruction = f"\ninstall using\n{self.__instruction}" if self.__instruction is not None else ''
        raise RuntimeError(f"{self.__installerr}{instruction}")

def import_or_err(package, elements='*', instruction=None):
    if not isinstance(elements, list):
        elements = [elements]
    try:
        dep =__import__(package, fromlist=elements)
        if elements is not None:
            out = tuple(getattr(dep, f) for f in elements)
            if len(out) == 1: return out[0]
            else: return tuple(out)
        else:
            return dep
    except Exception as e:
        return MissingDependency(package, instruction, e)


from ast import literal_eval 
import inspect, hashlib, uuid as _uuid
from urllib.parse import unquote, quote
from multiprocessing.pool import ThreadPool
from copy import deepcopy as clone
import logging, html as _html

logdisable = lambda _=True: logging.getLogger().setLevel(logging.WARNING)
loginfo = lambda v=True: logging.getLogger().setLevel(logging.INFO) if v else logdisable(True)
logdebug = lambda v=True: logging.getLogger().setLevel(logging.DEBUG) if v else logdisable(True)



uuid4 = lambda: str(_uuid.uuid4())

b2s = lambda value: value.decode() if isinstance(value, bytes) or isinstance(value, bytearray) else value
s2b = lambda value: value if isinstance(value, bytes) or isinstance(value, bytearray) else value.encode()

urld = lambda value: unquote(value)
urle = lambda value: quote(value)

htmle = lambda value: _html.escape(value)
htmld = lambda value: _html.unescape(value)

i2b = lambda v: v.to_bytes((v.bit_length() + 7) // 8 if v.bit_length() != 0 else 1, 'big')
b2i = lambda v: int.from_bytes(s2b(v), 'big')

# Little endian
i2b_le = lambda v: v.to_bytes((v.bit_length() + 7) // 8 if v.bit_length() != 0 else 1, 'little')
b2i_le = lambda v: int.from_bytes(s2b(v), 'little')

def xor(a, b): 
    if len(a) == 0: return b
    if len(b) == 0: return a
    a, b = s2b(a), s2b(b)
    return bytes(a[i % len(a)] ^ b[i % len(b)] for i in range(max(len(a), len(b))))


lit2py = lambda value: literal_eval(b2s(value))

s2obj = lambda value: json.loads(b2s(value))
obj2s = lambda value: json.dumps(value)


hex2b = lambda value: (v:=b2s(value).replace(' ','').strip(), bytes.fromhex(v.zfill(len(v)+(len(v))%2)))[1]
hex2i = lambda value: b2i(hex2b(value))


bin2b = lambda value: bytes([int(value[max(0,i-8):i], 2) for i in range(len(value), 0, -8)][::-1])


# Little endian
hex2b_le = lambda value: hex2b(value)[::-1]
hex2i_le = lambda value: b2i(hex2b(value)[::-1])

b64e = lambda value: base64.b64encode(s2b(value))
b64d = lambda value: base64.b64decode(s2b(value) + b"="*(-len(value)%4))
b64e_url = lambda value: base64.urlsafe_b64encode(s2b(value))
b64d_url = lambda value: base64.urlsafe_b64decode(s2b(value) + b"="*(-len(value)%4))

# Sorted by freq analysis on flags (ignoring .*{} and random flags)
string.flag = '''_3tnr0es1a4hloiducympgfb5w7kT!vS2R-ECNDAL6IPH9U8YOMF.GxzW?BK@jVq/: X$,\\#QZJ'~{<&}>=+)(|*;%]`[^"'''
string.lowercase = string.ascii_lowercase
string.uppercase = string.ascii_uppercase
string.letters = string.ascii_letters
string.alphanumeric = string.letters + string.digits
string.base64 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
string.base64_url = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'

rand = lambda length, alphabet=string.letters+string.digits: ''.join(random.choice(alphabet) for _ in range(length))
securerand = lambda length, alphabet=string.letters+string.digits: ''.join(secrets.choice(alphabet) for _ in range(length))

run_shell = lambda cmd: subprocess.run(cmd, shell=True, capture_output=True) # x.stdout, x.stderr, x.returncode

readlines = lambda name: open(name, 'r').read().split('\n')
writefile = lambda name, value: open(name, 'wb').write(value) if isinstance(value, bytes) else open(name, 'w').write(value)
readfile = lambda name: open(name, 'rb').read()


md5 = lambda value: hashlib.md5(s2b(value)).digest()
sha1 = lambda value: hashlib.sha1(s2b(value)).digest()
sha128 = lambda value: hashlib.sha128(s2b(value)).digest()
sha224 = lambda value: hashlib.sha224(s2b(value)).digest()
sha256 = lambda value: hashlib.sha256(s2b(value)).digest()
sha384 = lambda value: hashlib.sha384(s2b(value)).digest()
sha512 = lambda value: hashlib.sha512(s2b(value)).digest()
sha3_128 = lambda value: hashlib.sha3_128(s2b(value)).digest()
sha3_224 = lambda value: hashlib.sha3_224(s2b(value)).digest()
sha3_256 = lambda value: hashlib.sha3_256(s2b(value)).digest()
sha3_384 = lambda value: hashlib.sha3_384(s2b(value)).digest()
sha3_512 = lambda value: hashlib.sha3_512(s2b(value)).digest()


def runner(func, params, threads=1):
    if threads == 1:
        for args in params:
            yield func(*(args if isinstance(args, tuple) else (args,)))
    else:
        def w(args): return func(*(args if isinstance(args, tuple) else (args,)))
        with ThreadPool(processes=threads) as pool:
            for result in pool.imap(w, params):
                yield result 

def withtimeout(func, args, timeout):
    if args is None: args = ()
    if not isinstance(args, tuple): args = (args,)
    q = _Queue()
    def worker():
        out = func(*args)
        q.put(out)

    t = _Process(target=worker)
    t.start()
    t.join(timeout=timeout)

    if t.is_alive():
        t.terminate()
        return "TIMEOUT"
    else:
        return q.get()


def setdbg(value):
    global LOG_DBG
    LOG_DBG = value
LOG_DBG = True
def dbg(value):
    if LOG_DBG:
        frame = inspect.currentframe().f_back
        code_ctx = inspect.getframeinfo(frame).code_context
        if code_ctx is None: 
            print(f"\033[1;31m[DEBUG]\033[0m {value!r}", file=sys.stderr)
            return value
        line = code_ctx[0].strip()
        m = re.search(r'\bdbg\s*\(', line)
        
        if not m: f_input="?"
        depth, i = 1, m.end()
        while i < len(line) and depth:
            depth += (line[i] == '(') - (line[i] == ')')
            i += 1
        f_input = line[m.end():i-1] if depth == 0 else "?"
        print(f"\033[1;31m{frame.f_code.co_filename}:{frame.f_lineno}\033[0m {f_input} = {value!r}", file=sys.stderr)
    return value

def bsearch(func, lo, hi): # func(x): if x <= 1: True; else: False # outputs 1 
    out = 0
    while lo <= hi: # [lo, hi]: inclusive
        m = (lo+hi)//2
        if func(m):
            out = m
            lo = m+1
        else:
            hi = m-1
    return out

def product(*args):
    *pools, repeat = args
    if not isinstance(repeat, int):
        raise TypeError("Last argument must be an integer")

    isstr = True
    isbytes = True
    isbytearray = True
    for pool in pools:
        if not isinstance(pool, str):
            isstr = False
        if not isinstance(pool, bytes):
            isbytes = False
        if not isinstance(pool, bytearray):
            isbytearray = False

    pools = pools * repeat

    def _gen(i, acc):
        if i == len(pools):
            yield tuple(acc)
            return
        for v in pools[i]:
            acc.append(v)
            yield from _gen(i + 1, acc)
            acc.pop()
    if isstr:
        for v in _gen(0, []):
            yield ''.join(v)
    elif isbytes:
        for v in _gen(0, []):
            yield bytes(v)
    elif isbytearray:
        for v in _gen(0, []):
            yield bytearray(v)
    else:
        yield from _gen(0, [])

