from .util_math import *
# For each number base, sort it based on entropy
def misc_sort_base_entropy(value, top=10, log=True):
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
        return f"\033[38;2;{red};{green};0m{value:.4f}{RESET}"


    print('entropy\tbase\tlength')
    v = []
    for b in list(range(2,64+1))+list(range(-64,-1)):
        base_value = i2base(value,b)
        entropy_v = entropy(base_value, conv_base_charset[:abs(b)])
        v.append((base_value, b, entropy_v))

    out = (sorted(v, key=lambda x: x[2]))
    if top is not None:
        out = out[:top]
    if log:
        for (value, b, entropy_v) in out:
            print(f'{colorize(entropy_v)}\t{b}\t{len(value)}')
    return out


