from .util_basic import *


if isinstalled('pycryptodome'):
    from Crypto.Util.Padding import pad as _pad, unpad as _unpad
    from Crypto.Cipher import AES
    from Crypto.Util.number import getPrime, isPrime
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



def crypto_cpa(encrypt_oracle, idx, block_size, threads=1, charset=bytes(range(256)), known=b'', amount=None):
    ## Chosen Plaintext Attack
    # Usage:
    '''python
from Crypto.Cipher import AES

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
    '''
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

block_size = 16
known  = b"ojadfsoije"
prefix = b"asdfjd"
secret = b"oiwejfo23j09wejf09j09jw09fejijfd"

def encrypt():
    cipher = AES.new(b'a'*16, AES.MODE_CBC, b'a'*16)
    pt = pad(prefix + known + secret, block_size)
    return b'a'*16 + cipher.encrypt(pt)

ciphertext = encrypt()

def padding_oracle(x: bytes) -> bool:
    try:
        cipher = AES.new(b'a'*16, AES.MODE_CBC, b'a'*16)
        pt = cipher.decrypt(x[16:]) # remove IV
        unpad(pt, block_size)
        return True
    except ValueError:
        return False

assert(crypto_pa(padding_oracle, ciphertext, block_size=block_size) == secret)
    '''

    charset = s2b(charset)
    out = bytearray(s2b(known))
    enc = bytearray(encrypted)

    i = 0
    while amount is None or i < amount:
        cur_pad = i % block_size
        padval = cur_pad + 1

        l = -block_size - 1 - cur_pad
        o = enc[l]

        base = bytearray(enc)

        tail_plain = out[:cur_pad]

        for j in range(1, cur_pad + 1):
            idx = l + j
            pk = tail_plain[j - 1]
            base[idx] = pk ^ enc[idx] ^ padval

        valid = padding_oracle(bytes(enc)) if cur_pad == 0 else False

        probes = [bytes(base[:l] + bytes([c]) + base[l+1:]) for c in charset]
        values = runner(padding_oracle, probes, threads=threads)

        for c, ispad in zip(charset, values):
            if valid and c == o:
                continue
            if ispad:
                v = o ^ c ^ padval
                out.insert(0, v)
                break
        else:
            break

        i += 1

        if (i % block_size) == 0:
            enc = enc[:-block_size]
            if len(enc) < block_size * 2:
                break

    try:
        return unpad(bytes(out), block_size)
    except ValueError:
        return bytes(out)

