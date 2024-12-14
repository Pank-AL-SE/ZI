import random
import time
from typing import Tuple
from crypto_lib import *

def shamir_encode():
    P = gen_prime(100000, 1000000000)
    Ca = gen_mutually_prime(P - 1)
    Da = inversion(Ca, P - 1)
    Cb = gen_mutually_prime(P - 1)
    Db = inversion(Cb, P - 1)
    message = random.randint(100000, P - 1)
    x1 = mod_pow(message, Ca, P)
    x2 = mod_pow(x1, Cb, P)
    x3 = mod_pow(x2, Da, P)
    x4 = mod_pow(x3, Db, P)

    print(f"P = {P}")
    print(f"Ca = {Ca}\t\tCb = {Cb}")
    print(f"Da = {Da}\t\tDb = {Db}")
    print(f"Message = {message}")
    print(f"A calculates x1 = {x1}")
    print(f"B calculates x2 = {x2}")
    print(f"A calculates x3 = {x3}")
    print(f"B calculates x4 = {x4}")


def elgamal():
    P = gen_prime_p_and_q()
    g = gen_primitive_root(P)
    k = random.randint(100000, P - 2)
    r = mod_pow(g, k, P)
    message = random.randint(100000, P - 1)
    Ca = random.randint(100000, P - 2)
    Da = mod_pow(g, Ca, P)
    Cb = random.randint(100000, P - 2)
    Db = mod_pow(g, Cb, P)
    e = (message % P * mod_pow(Db, k, P)) % P
    new_message = (e % P * mod_pow(r, P - 1 - Cb, P)) % P

    print(f"P = {P}")
    print(f"Ca = {Ca}\t\tCb = {Cb}")
    print(f"Da = {Da}\t\tDb = {Db}")
    print(f"Message = {message}")
    print(f"k = {k}")
    print(f"r = {r}")
    print(f"e = {e}")
    print(f"New message = {new_message}")


def vernam(message: str):
    random.seed(time.time())
    code = []
    key = []
    for char in message:
        k = random.randint(0, 255)
        c = k ^ ord(char)
        key.append(k)
        code.append(c)
    encoded_message = ''.join(map(chr, code))
    print(f"Code: {encoded_message}")

    decoded_message = ''.join(chr(c ^ k) for c, k in zip(code, key))
    print(f"Decode: {decoded_message}")


def rsa():
    Pa = gen_prime(1000, 50000)
    Qa = gen_prime(1000, 50000)
    Na = Pa * Qa
    fia = (Pa - 1) * (Qa - 1)
    da = gen_mutually_prime(fia)
    ca = inversion(da, fia)

    Pb = gen_prime(1000, 50000)
    Qb = gen_prime(1000, 50000)
    Nb = Pb * Qb
    fib = (Pb - 1) * (Qb - 1)
    db = gen_mutually_prime(fib)
    cb = inversion(db, fib)

    message = random.randint(1000, Nb - 1)

    print(f"Pa = {Pa}\t\tPb = {Pb}")
    print(f"Qa = {Qa}\t\tQb = {Qb}")
    print(f"Na = {Na}\t\tNb = {Nb}")
    print(f"fia = {fia}\t\tfib = {fib}")
    print(f"da = {da}\t\tdb = {db}")
    print(f"ca = {ca}\t\tcb = {cb}")
    print(f"Message = {message}")

    e = mod_pow(message, db, Nb)
    print(f"E = {e}")
    new_message = mod_pow(e, cb, Nb)
    print(f"New message = {new_message}")