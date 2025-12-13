from .util_basic import *

def crypto_cpa(encrypt_oracle, idx, block_size, threads=1, charset=bytes(range(256))):
    msg = bytearray()
  
    while True:
        presize = 16 if idx % block_size == 0 else (-idx) % block_size

        base = encrypt_oracle((presize-1) * bytearray(b'a'))

        values = runner(encrypt_oracle, [(presize-1) * bytearray(b'a') + msg + bytes([c]) for c in charset], threads=threads)
        blk_idx = (idx//block_size)*block_size
        for c, enc in zip(charset, values):
            if enc[blk_idx:blk_idx+block_size] == base[blk_idx: blk_idx+block_size]:
                msg += bytearray([c])
                break
        else:
            break
        idx += 1
    return msg

