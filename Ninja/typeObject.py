from enum import Enum

class typeObject(Enum):
    ROCK = 0
    PAPER = 1
    SCISSOR = 2

if __name__ == "__main__":
    rock = typeObject.ROCK

    print(rock)