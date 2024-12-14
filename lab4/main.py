import sys

sys.path.insert(0, './')  #файл poker.py находится в той же директории

from poker import poker

def main():
    poker(3)

if __name__ == "__main__":
    main()