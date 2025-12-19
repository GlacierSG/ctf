from .util_basic import *


def crypto_cpa(encrypt_oracle, idx, block_size, threads=1, charset=bytes(range(256)), known=b'', amount=None):
    ## Chosen Plaintext Attack
    # Usage:
    '''python
known = b'ojadfsoije'
prefix = b'asdfjd'
secret = b'oiwejfo23j09wejf09j09jw09fejijfd'
block_size = 16
oracle = lambda x: AES.new(key=b'a'*16, mode=AES.MODE_ECB).encrypt(pad(prefix+x+known+secret, block_size))
assert(crypto_cpa(oracle, idx=len(prefix), block_size=16, threads=10, known=known, amount=8) == secret[:8])
    '''
    charset = s2b(charset)
    msg = bytearray(s2b(known))
    idx += len(known)
    
    i = 0
    while True if amount is None else i < amount:
        pad_len = (-idx - 1) % block_size
        if pad_len:
            prefix = bytearray(b'a') * pad_len
        else:
            prefix = bytearray()

        base = encrypt_oracle(prefix)

        values = runner(encrypt_oracle, [prefix + msg + bytes([c]) for c in charset], threads=threads)
        blk_idx = (idx//block_size)*block_size
        for c, enc in zip(charset, values):
            if enc[blk_idx:blk_idx+block_size] == base[blk_idx:blk_idx+block_size]:
                msg += bytearray([c])
                logging.info(f'Found character: {bytes(msg)}')
                break
        else:
            break
        idx += 1
        i += 1
    return bytes(msg[len(known):])


def crypto_pa(padding_oracle, encrypted, block_size, threads=1, charset=bytes(range(256)), known=b'', amount=None):

    charset = s2b(charset)
    out = bytearray(s2b(known))
    
    enc = bytearray(encrypted)
    cur_pad = len(out) % block_size
    i = 0
    while True if amount is None else i < amount:
        valid = padding_oracle(enc) if i % block_size == 0 else False 
        l = -block_size-cur_pad
        o = enc[l]
        values = runner(padding_oracle, [enc[:l]+bytes([c])+enc[l+1:] for c in charset], threads=threads)
        for c, ispad in zip(charset, values):
            if valid and c == o:
                continue
            if ispad:
                v = o ^ c ^ cur_pad
                out = [v] + out
                break
        else:
            if i % block_size == 0:
                out = [1] + out
            else:
                break
        cur_pad = (cur_pad + 1) % 16
        if cur_pad == 0:
            enc = enc[:-block_size]
            if len(enc) < block_size*2:
                break
