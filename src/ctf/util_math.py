from math import factorial, log2
from collections import Counter
from .util_math import *

# Not normal base64 alphabet
conv_base_charset = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"

# From number to base
def i2base(n, base, charset = conv_base_charset):
    if base == 0 or base == 1 or base == -1:
        raise ValueError("Base must not be 0, 1, or -1.")
    if n == 0:
        return "0"
    
    digits = []
    while n != 0:
        n, r = divmod(n, base)
        if r < 0:
            r -= base
            n += 1
        digits.append(r)

    return ''.join(charset[d] for d in reversed(digits))

def base2i(s, base, charset=conv_base_charset) -> int:
    s = b2s(s).strip()
    if 10 < base < 36: 
        s = s.upper()
    value = 0
    for ch in s:
        if ch not in charset[:abs(base)]:
            raise ValueError(f"Invalid digit '{ch}' for base {base}")
        value = value * base + charset.index(ch)
    return value

# Calculates shannon entropy with a known charset
def entropy(s, charset=list(range(256))):
    L = len(s)
    counts = Counter(s)
    probs = [counts[c]/L for c in charset]
    
    # Shannon entropy
    H = -sum(p * log2(p) for p in probs if p > 0)
    H_max = log2(len(charset))

    out = H / H_max
    return 0.0 if out == 0.0 else out # remove -0.0


