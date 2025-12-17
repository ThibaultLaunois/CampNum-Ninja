class Game:
    """
    Docstring for Game
    """
    def __init__(self):
        self.score = 0
        self.duration = 0
        self.gameMode = None
        self.maxObjects = 1
        self.diffculty = 1
        self.detectionRadius = 1

    def increaseDifficulty(self):
        pass

    def decreaseDifficulty(self):
        pass

    def changeGameMode(self):
        pass

    def updateScore(self, scoreToAdd):
        pass

    def updateDuration(self, newDuration):
        pass

    def getScore(self):
        pass

    def getDuration(self):
        pass

    def getGameMode(self):
        pass

    def getDifficulty(self):
        pass
