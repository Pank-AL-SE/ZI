import math
from random import seed, randrange, shuffle
from itertools import combinations
from collections import namedtuple
from functools import reduce


def generate_coprime(p):
    result = randrange(2, p - 1)
    while math.gcd(p, result) != 1:
        result = randrange(2, p - 1)
    return result


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def is_prime(p):
    if p <= 1:
        return False
    
    limit = int(math.sqrt(p))
    for i in range(2, limit + 1):
        if p % i == 0:
            return False
    return True


def pow_mod(base, exp, mod):
    result = 1
    base %= mod
    while exp:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


def extended_euclidean_algorithm(a, b):
    if a < b:
        a, b = b, a
        u = (a, 0, 1)
        v = (b, 1, 0)
    else:
        u = (a, 1, 0)
        v = (b, 0, 1)
        
    while v[0]:
        q = u[0] // v[0]
        t = (u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2])
        u = v
        v = t
    return u


def get_prime(left, right):
    while True:
        p = randrange(left, right + 1)
        if is_prime(p):
            return p


Edge = namedtuple('Edge', ['from_', 'to', 'index'])


def read_graph(filename):
    with open(filename, encoding='utf8') as file:
        vertex_num, edge_num = map(int, file.readline().split())
        
        edges = []
        for _ in range(edge_num):
            from_, to = map(int, file.readline().split())
            edges.append(Edge(from_, to, len(edges) + 1))
            
        colors = list(file.read().strip())
        
        return edges, colors, vertex_num

def main():
    seed()
    
    try:
        edges, colors, vertex_num = read_graph('graph_wrong.txt')
    except Exception as e:
        print(f"Ошибка: {e}")
        return 1
    
    print(f"Граф содержит {vertex_num} вершин и {len(edges)} рёбер:")
    for edge in edges:
        print(f"{edge.from_} {edge.to} (ребро {edge.index})")
    
    print("Раскраска:", end=" ")
    print(*colors)
    
    color_names = ['R', 'G', 'B']
    shuffled_color_names = color_names[:]
    while shuffled_color_names == color_names:
        shuffle(shuffled_color_names)

    recolored_colors = []
    for c in colors:
        if c in color_names:
            recolored_colors.append(shuffled_color_names[color_names.index(c)])
        else:
            print(f"Предупреждение: неизвестный цвет '{c}' заменен на 'R'")
            recolored_colors.append('R')
    
    print("Перерекрашенный граф:", end=" ")
    print(*recolored_colors)

    r = [randrange(1000000) for _ in range(vertex_num)]
    p = [get_prime(32500, 45000) for _ in range(vertex_num)]
    q = [get_prime(32500, 45000) for _ in range(vertex_num)]
    n = [p[i] * q[i] for i in range(vertex_num)]
    phi = [(p[i] - 1) * (q[i] - 1) for i in range(vertex_num)]
    d = [generate_coprime(phi[i]) for i in range(vertex_num)]
    c = [extended_euclidean_algorithm(d[i], phi[i])[1] for i in range(vertex_num)]
    for i in range(vertex_num):
        if c[i] < 0:
            c[i] += phi[i]
        Z = [pow_mod(r[i], d[i], n[i]) for i in range(vertex_num)]

    flag = False
    for i, edge in enumerate(edges):
        u = edge.from_ - 1
        v = edge.to - 1
        id = edge.index
        Z1 = pow_mod(Z[u], c[u], n[u])
        Z2 = pow_mod(Z[v], c[v], n[v])

        if (Z1 & 3) != (Z2 & 3):
            print(f"Для ребра {id} два младших бита различны.")
        else:
            flag = True
            print(f"Алиса обманула Боба! Два последних бита совпадают у ребра {id}.")

    if flag:
        print("Алиса обманула Боба!")
    else:
        print("Граф раскрашен правильно!")

    return 0


if __name__ == "__main__":
    main()