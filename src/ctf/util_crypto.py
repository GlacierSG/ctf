from .util_basic import *


def crypto_cpa(encrypt_oracle, idx, block_size, threads=1, charset=bytes(range(256)), known=b''):
    ## Chosen Plaintext Attack
    # Usage:
    '''python
    known = b'ojadfsoije'
    prefix = b'asdfjd'
    msg = known+b'oiwejfo23j09wejf09j09jw09fejijfd'
    block_size = 16
    oracle = lambda x: AES.new(key=b'a'*16, mode=AES.MODE_ECB).encrypt(pad(prefix+x+msg, block_size))
    print(crypto_cpa(oracle, len(prefix), block_size, threads=10, known=known) == msg+b'\x01')
    '''
    charset = s2b(charset)
    msg = bytearray(s2b(known))
    idx += len(known)
  
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

