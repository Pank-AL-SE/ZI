import random
from math import gcd, isqrt
from typing import Tuple


class Euclid:
    def __init__(self, a: int, b: int):
        if a == 0 and b == 0:
            raise ValueError("Both numbers cannot be zero.")
        self.extended_gcd(a, b)

    def extended_gcd(self, a: int, b: int):
        if a < b:
            a, b = b, a
        self.m_a = a
        self.m_b = b
        u = [a, 1, 0]
        v = [b, 0, 1]
        while v[0] != 0:
            q = u[0] // v[0]
            t = [u[0] % v[0], u[1] - v[1] * q, u[2] - v[2] * q]
            u, v = v, t
        self.m_gcd = u[0]
        self.m_x = u[1]
        self.m_y = u[2]

    def a(self): return self.m_a
    def b(self): return self.m_b
    def x(self): return self.m_x
    def y(self): return self.m_y
    def gcd(self): return self.m_gcd

    def print_equation(self):
        print(f"{self.m_a} * {self.m_x} + {self.m_b} * {self.m_y} = {self.m_gcd}")


def mod_pow(base: int, exp: int, mod: int) -> int:
    if base < 0 or exp < 0 or mod <= 0:
        raise ValueError("Base and exponent must be non-negative, and modulus must be positive.")
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


def inversion(c: int, m: int) -> int:
    if c > m:
        c %= m
    euclid = Euclid(m, c)
    if euclid.gcd() != 1:
        raise RuntimeError("Numbers must be mutually simple!")
    res = euclid.y()
    return res + m if res < 0 else res


def miller_test(d: int, n: int) -> bool:
    a = random.randint(2, n - 2)
    x = mod_pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def is_prime(number: int, accuracy: int) -> bool:
    if number <= 1 or number == 4:
        return False
    if number <= 3:
        return True
    if number % 2 == 0:
        return False
    d = number - 1
    while d % 2 == 0:
        d //= 2
    for _ in range(accuracy):
        if not miller_test(d, number):
            return False
    return True


def gen_prime_p_and_q() -> int:
    while True:
        q = random.randint(100000, 1000000000)
        if is_prime(q, 5):
            p = 2 * q + 1
            if is_prime(p, 5):
                return p


def gen_prime(min_value: int, max_value: int) -> int:
    while True:
        q = random.randint(min_value, max_value)
        if is_prime(q, 5):
            return q


def gen_mutually_prime(p: int) -> int:
    while True:
        number = random.randint(100000, p - 1)
        if gcd(number, p) == 1:
            return number


def gen_primitive_root(p: int) -> int:
    while True:
        g = random.randint(2, p - 1)
        if mod_pow(g, p // 2, p) == 1:
            return g


def diffie_hellman() -> int:
    p = gen_prime_p_and_q()
    g = gen_primitive_root(p)
    print(f"P = {p} | g = {g}")
    xa = random.randint(1, p - 1)
    xb = random.randint(1, p - 1)
    print(f"Xa = {xa} | Xb = {xb}")
    ya = mod_pow(g, xa, p)
    yb = mod_pow(g, xb, p)
    print(f"Ya = {ya} | Yb = {yb}")
    zab = mod_pow(yb, xa, p)
    zba = mod_pow(ya, xb, p)
    print(f"Zab = {zab} | Zba = {zba}")
    return zab


def giant_baby_step(a: int, p: int, y: int) -> int:
    m = k = isqrt(p) + 1
    mp = {y % p: 0}
    num = y % p
    for i in range(1, m):
        num = (num * a) % p
        mp[num] = i
    step = mod_pow(a, m, p)
    num = step
    for i in range(1, k + 1):
        if num in mp:
            return m * i - mp[num]
        num = (num * step) % p
    return -1