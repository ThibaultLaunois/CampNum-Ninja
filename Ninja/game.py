from Ninja.gameMode import gameMode

class Game:
    """
    Class containing the relevant information of the current game.

    ATTRIBUTES
        :score (int):
        :duration (float):
        :gameMode (gameMode):
        :maxObject (int):
        :difficulty (int):
        :detectionRadius (int):
    
    METHODS
        :increaseDifficulty:
        :decreaseDifficulty:
        :changeGameMode:
        :updateScore:
        :updateDuration:
        :getScore:
        :getDuration:
        :getGameMode:
        :getDifficulty:
    """

    def __init__(self):
        self.score = 0
        self.duration = 0
        self.gameMode = gameMode.MATCH
        self.maxObjects = 1
        self.difficulty = 1
        self.detectionRadius = 1

    def increaseDifficulty(self):
        """
        Increase the difficulty by +1 if the current difficulty is smaller than 10.
        The difficulty setting ranges from 1 to 10.
        """
        if self.getDifficulty() < 10:
            self.difficulty += 1

    def decreaseDifficulty(self):
        """
        Decrease the difficulty by -1 if the current difficulty is greater than 1.
        The difficulty setting ranges from 1 to 10.
        """
        if self.getDifficulty() > 1:
            self.difficulty -= 1

    def changeGameMode(self):
        """
        Change game mode according to the following rotation :
        MATCH -> BEAT -> DUAL -> MATCH -> ...
        """
        if self.getGameMode() == gameMode.MATCH:
            self.gameMode = gameMode.BEAT
        elif self.getGameMode() == gameMode.BEAT:
            self.gameMode = gameMode.DUAL
        elif self.getGameMode() == gameMode.DUAL:
            self.gameMode = gameMode.MATCH

    def updateScore(self, scoreToAdd):
        """
        Add given score to total score of current game.
        
        :param scoreToAdd (int): 
        """
        self.score += scoreToAdd

    def updateDuration(self, newDuration):
        """
        Update current duration with the new duration given.
        
        :param newDuration (float): 
        """
        self.duration = newDuration

    def getScore(self):
        """
        Returns current score.
        """
        return self.score

    def getDuration(self):
        """
        Returns current duration.
        """
        return self.duration

    def getGameMode(self):
        """
        Returns current game mode.
        """
        return self.gameMode

    def getDifficulty(self):
        """
        Returns current difficulty.
        """
        return self.difficulty
