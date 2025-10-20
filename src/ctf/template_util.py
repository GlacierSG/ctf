import sys, os, string, re, base64, json, subprocess, itertools, random

from .setup_venv import * 

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

def install(modules):
    if isinstance(modules, str):
        modules = [modules]

    for module in modules:
        if not isinstalled(module):
            subprocess.check_call([f"{VENV_PATH}/bin/python", "-m", "pip", "install", module])

install([
    'requests',
    'pycryptodome'
])

from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util.Padding import pad as _pad, unpad as _unpad
from Crypto.Cipher import AES
from ast import literal_eval 
import hashlib
import requests
from urllib.parse import unquote, quote

urld = lambda value: unquote(value)
urle = lambda value: quote(value)

def unpad(value, size=16):
    try:
        return _unpad(s2b(value), size)
    except ValueError as e:
        raise ValueError(f"Invalid padding: padding = {value[-size:]}, padding size = {size}")
pad = lambda value, size=16: _pad(s2b(value), size)

aes_ecb_enc = lambda value, key: AES.new(key=s2b(key), mode=AES.MODE_ECB).encrypt(pad(value, 16))
aes_ecb_dec = lambda value, key: unpad(AES.new(key=s2b(key), mode=AES.MODE_ECB).decrypt(value), 16)

aes_cbc_enc = lambda value, key, iv: AES.new(key=s2b(key), iv=iv, mode=AES.MODE_CBC).encrypt(pad(value, 16))
aes_cbc_dec = lambda value, key, iv: unpad(AES.new(key=s2b(key), iv=iv, mode=AES.MODE_CBC).decrypt(value), 16)

l2b = long_to_bytes
b2l = bytes_to_long
i2b = l2b
b2i = b2l

b2s = lambda value: value.decode() if isinstance(value, bytes) or isinstance(value, bytearray) else value
s2b = lambda value: value if isinstance(value, bytes) or isinstance(value, bytearray) else value.encode()

lit2py = lambda value: literal_eval(b2s(value))

json2py = lambda value: json.loads(b2s(value))
py2json = lambda value: json.dumps(value)

# Little endian
l2b_le = lambda value: l2b(value)[::-1]
b2l_le = lambda value: b2l(value[::-1])

hex2b = lambda value: (v:=b2s(value).replace(' ','').strip(), bytes.fromhex(v.zfill(len(v)+(len(v))%2)))[1]
hex2l = lambda value: b2l(hex2b(value))


bin2b = lambda value: bytes([int(value[max(0,i-8):i], 2) for i in range(len(value), 0, -8)][::-1])


# Little endian
hex2b_le = lambda value: hex2b(value)[::-1]
hex2l_le = lambda value: b2l(hex2b(value)[::-1])

b64e = lambda value: base64.b64encode(s2b(value))
b64d = lambda value: base64.b64decode(s2b(value) + b"="*(-len(value)%4))
urlsafe_b64e= lambda value: base64.urlsafe_b64encode(s2b(value))
urlsafe_b64d = lambda value: base64.urlsafe_b64decode(s2b(value) + b"="*(-len(value)%4))

# Sorted by freq analysis on flags (ignoring flag{} and random flags)
string.flag = r"""_3tnr0es1a4hloiducympgfb5w7kT!vS2-RCENDAL6IPH98UYOMF.GxzW?BjK@Vq/: X$,#QJZ'~\{}<&+=>()*|%;"[]^`"""
string.lowercase = string.ascii_lowercase
string.uppercase = string.ascii_uppercase
string.letters = string.ascii_letters

run_shell = lambda cmd: subprocess.run(cmd, shell=True, capture_output=True) # x.stdout, x.stderr, x.returncode

readlines = lambda name: open(name, 'r').read().split('\n')
writefile = lambda name, value: open(name, 'wb').write(v) if isinstance(value, bytes) else open(name, 'w').write(value)
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

getproxy = lambda x: {"http": f"http://{x}", "https": f"http://{x}"}
def getsession(proxy=False, proxies=getproxy('127.0.0.1:8080')):
    s = requests.Session()
    if proxy:
        s.proxies = proxies
        s.verify = False
    return s

def getwebhook(data="", cors=False, content_type='text/html', status_code=200, onlytoken=False):
    r = requests.post("https://webhook.site/token", json={"default_content": data, "cors": cors, "default_content_type": content_type, "default_status":status_code})
    return r.json()['uuid'] if onlytoken else 'https://webhook.site/'+r.json()['uuid']
def webhook_ui(token):
    token = token.replace('https://webhook.site/','')
    return f'https://webhook.site/#!/view/{token}'
def webhook_results(token):
    token = token.replace('https://webhook.site/','')
    r = requests.get(f'https://webhook.site/token/{token}/requests?sorting=newest')
    return r.json()['data']

def setdbg(value):
    global LOG_DBG
    LOG_DBG = value
LOG_DBG = True
def dbg(value):
    if LOG_DBG:
        frame = __import__('inspect').currentframe().f_back
        code_ctx = __import__('inspect').getframeinfo(frame).code_context
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
