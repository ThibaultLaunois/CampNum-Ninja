from enum import Enum

class gameMode(Enum):
    MATCH = 0
    BEAT = 1
    DUAL = 2
    POP = 3
    PUSH = 4

if __name__ == "__main__":
    mode = gameMode.MATCH

    print(mode)