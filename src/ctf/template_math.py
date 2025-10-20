import math
from collections import Counter
from .template_util import *

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
def shannon_entropy(s, charset):
    L = len(s)
    counts = Counter(s)
    probs = [counts[c]/L for c in charset]
    
    # Shannon entropy
    H = -sum(p * math.log2(p) for p in probs if p > 0)
    H_max = math.log2(len(charset))

    return H / H_max


# For each number base, sort it based on entropy
def sorted_base_entropy(value, max_values=10, log=True):
    if not isinstance(value, int):
        raise Exception(f"input should be int")
    RESET = "\033[0m"
    def colorize(value, min_val=0.0, max_val=1.0):
        ratio = (value - min_val) / (max_val - min_val)
        ratio = max(0.0, min(1.0, ratio))

        if ratio < 0.8:
            red = int(255 * (ratio / 0.8))
            green = 255
        else:
            red = 255
            green = int(255 * (1 - (ratio - 0.8) / 0.2))

        return f"\033[38;2;{red};{green};0m{value:.5f}{RESET}"


    print('entropy\tbase\tlength')
    v = []
    for b in list(range(2,64+1))+list(range(-64,-1)):
        base_value = i2base(value,b)
        entropy = shannon_entropy(base_value, conv_base_charset[:abs(b)])
        v.append((base_value, b, entropy))

    out = (sorted(v, key=lambda x: x[2]))[:max_values]
    if log:
        for (value, b, entropy) in out:
            print(f'{colorize(entropy)}\t{b}\t{len(value)}')
    return out


