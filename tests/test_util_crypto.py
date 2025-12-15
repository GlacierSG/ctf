from ctf import *
from Crypto.Util.Padding import pad as _pad, unpad as _unpad
from Crypto.Cipher import AES

aes_ecb_enc = lambda value, key: AES.new(key=s2b(key), mode=AES.MODE_ECB).encrypt(pad(value, 16))
enc_oracle = lambda x: aes_ecb_enc(x+b'asdfjoidsjfoie9fj9jeifj', b'a'*16)

known = b'ABCDEFGH'
prefix = b'0123456'
secret = b'abcdefghijklmnopqrstuvwxyz'
block_size = 16
oracle = lambda x: AES.new(key=b'a'*16, mode=AES.MODE_ECB).encrypt(pad((prefix+x+known+secret), block_size))
assert(crypto_cpa(oracle, idx=len(prefix), block_size=16, threads=10, known=known, amount=8) == secret[:8])


print(crypto_cpa(lambda x: aes_ecb_enc(x+b'asdfjoidsjfoie9fj9jeifj', b'a'*16), 0, 16, threads=10))
print(crypto_cpa(lambda x: aes_ecb_enc(b'asdf'+x+b'asdfjoidsjfoie9fj9jeifj', b'a'*16), 4, 16, threads=10))
print(crypto_cpa(lambda x: aes_ecb_enc(b'a'*131+x+b'asdfjoidsjfoie9fj9jeifj', b'a'*16), 131, 16, threads=10, known=b'asdfjoi', amount=3))
