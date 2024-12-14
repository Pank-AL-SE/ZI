import random
from math import gcd

# Символы мастей карт
SPADE = "\u2660"
CLUB = "\u2663"
HEART = "\u2665"
DIAMOND = "\u2666"

def modul_pow(base, exp, modulus):
    """Возведение числа base в степень exp по модулю modulus"""
    result = 1
    base %= modulus
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % modulus
        base = (base ** 2) % modulus
        exp //= 2
    return result % 52 + 2

def inversion(a, m):
    """Находит обратный элемент a по модулю m"""
    g, x, y = extended_euclidean_algorithm(a, m)
    if g != 1:
        raise Exception('Модулярные обратные элементы не существуют')
    else:
        return x % m

def extended_euclidean_algorithm(a, b):
    """Расширенный алгоритм Евклида для нахождения НОД и коэффициентов"""
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_euclidean_algorithm(b % a, a)
        return g, x - (b // a) * y, y

def gen_mutually_prime(m):
    """Генерация взаимно простого числа с m"""
    while True:
        num = random.randint(2, m - 1)
        if gcd(num, m) == 1:
            return num

def gen_prime_p_and_q():
    # Возвращает большое простое число для безопасного шифрования
    return 2147483647  # Например, 2^31 - 1, большое простое число

def deck_generation():
    suits = [SPADE, CLUB, HEART, DIAMOND]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    deck = {}
    for i in range(len(suits)):
        for j in range(len(ranks)):
            deck[len(ranks)*i + j + 2] = ranks[j] + suits[i]

    for key, value in deck.items():
        print(f"{value}({key}) ", end="")
    print("\n")
    return deck

def poker(players_count):
    if players_count > 22:
        print("TOO MANY PLAYERS")
        return

    P = gen_prime_p_and_q()
    print(f"P = {P}")

    c = []
    d = []
    for _ in range(players_count):
        ci = gen_mutually_prime(P - 1)
        di = inversion(ci, P - 1)
        c.append(ci)
        d.append(di)

    print("DECK:")
    deck = deck_generation()
    print()

    numbers = list(range(2, 54))  # Создаем список чисел от 2 до 53
    random.shuffle(numbers)       # Перемешиваем этот список

    hands = [[0, 0] for _ in range(players_count)]
    for i in range(players_count):
        hands[i][0] = numbers.pop()   # Берём две верхние карты для каждого игрока
        hands[i][1] = numbers.pop()

    # Оставшиеся карты идут на стол
    table = numbers[:5]

    for i in range(players_count):
        for card in table:
            card = modul_pow(card, d[i], P)

    print("CARDS ON TABLE:")
    for card in table:
        print(f"{deck[card]}({card}) ", end="")
    print()

    for i in range(players_count):
        for j in range(players_count):
            if i != j:
                hands[i][0] = modul_pow(hands[i][0], d[j], P)
                hands[i][1] = modul_pow(hands[i][1], d[j], P)
        hands[i][0] = modul_pow(hands[i][0], d[i], P)
        hands[i][1] = modul_pow(hands[i][1], d[i], P)

    print("\nCARDS ON PLAYERS:")
    for i in range(players_count):
        print(f"PLAYER {i + 1}")
        print(f"{deck[hands[i][0]]}({hands[i][0]}) {deck[hands[i][1]]}({hands[i][1]})\n")

    print("KEYS:")
    for i in range(players_count):
        print(f"C({i + 1}) = {c[i]}\t\tD({i + 1}) = {d[i]}")