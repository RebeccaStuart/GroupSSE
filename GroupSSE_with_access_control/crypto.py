from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def prf_512(sk, msg):#根据密钥sk给消息msg加密为512位密文，如果sk是相同的，那么加密结果也是相同的
    if type(msg) is bytes:
        b_msg = msg
    else:
        b_msg = bytes(msg, 'utf-8')
    h = hmac.HMAC(sk, hashes.SHA512(), backend=default_backend())
    h.update(b_msg)
    value = (h.finalize())
    return value


def prf_256(sk, msg):#根据密钥sk给消息msg加密为256位密文，如果sk是相同的，那么加密结果也是相同的
    if type(msg) is bytes:
        b_msg = msg
    else:
        b_msg = bytes(msg, 'utf-8')
    h = hmac.HMAC(sk, hashes.SHA256(), backend=default_backend())
    h.update(b_msg)
    value = (h.finalize())
    return value


def egcd(a, b):#求a和b的最大公约数的
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def mod_inv(a, m):#求a关于模数m的逆
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def enc(key, iv, msg):
    padder = padding.PKCS7(128).padder()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    bmsg = bytes(msg, "utf-8")
    ct = encryptor.update(padder.update(bmsg) + padder.finalize()) + encryptor.finalize()
    return ct

def dec(key, iv, ct):
    unpadder = padding.PKCS7(128).unpadder()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    pplaintext = decryptor.update(ct) + decryptor.finalize()
    plaintext = unpadder.update(pplaintext) + unpadder.finalize()
    return plaintext


if __name__ == '__main__':
    print(egcd(22, 121)[0])
    print(mod_inv(3, 17))
    msg = 'abdwsdsx'.encode()
    result = prf_256('sssss'.encode(), msg)
    print(result, type(result))
