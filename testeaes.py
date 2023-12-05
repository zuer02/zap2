import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

backend = default_backend()

key = os.urandom(32) # gerando uma key aleatoria para criptografar
iv = os.urandom(16) # vetor de inicialização

aes = algorithms.AES(key)
cbc = modes.CBC(iv)
cipher = Cipher(aes, cbc, backend=backend)
encryptor = cipher.encryptor() # encriptador

MSG = input('\n')
b_msg = bytearray(MSG, encoding="utf8")
# ou
# b_msg = bytes(MSG, 'utf-8')

block_size = 16
n = len(b_msg)
spaces_add = block_size - n % block_size
new_b_msg = bytearray(MSG + ' ' * spaces_add, encoding="utf8")
padder = padding.PKCS7(128).padder()
msg_pad = padder.update(new_b_msg) + padder.finalize()
print(msg_pad)
ct = encryptor.update(msg_pad) + encryptor.finalize()
# ct_e = base64.b64encode(ct)

print(ct,'\n')

unpadder = padding.PKCS7(128).unpadder()

decryptor = cipher.decryptor()
dec_ct = decryptor.update(ct) + decryptor.finalize()
print(dec_ct)

msg_unpad = unpadder.update(dec_ct) #+ unpadder.finalize() #unpad antes ou depois??
print(msg_unpad)



#from Crypto.Cipher import AES
# from secrets import token_bytes

# key = token_bytes(16)

# def encrypt(msg):
#     cipher = AES.new(key, AES.MODE_EAX)
#     nonce = cipher.nonce
#     ciphertext, tag = cipher.encrypt_and_digest(msg.encode('ascii'))
#     return nonce, ciphertext, tag

# def decrypt(nonce, ciphertext, tag):
#     cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
#     plaintext = cipher.decrypt(ciphertext)
#     try:
#         cipher.verify(tag)
#         return plaintext.decode('ascii')
#     except Exception as e:
#         print(f'Decryption failed: {e}')
#         return False
    
# msg = input('\n')

# nonce, ciphertext, tag = encrypt(msg)

# plaintext = decrypt(nonce, ciphertext, tag)

# if not plaintext:
#     print('deu ruim')
# else:
#     print(plaintext)

