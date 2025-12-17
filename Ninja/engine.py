from Ninja.game import Game
from Ninja.gameState import GameState
from Ninja.interface import Interface
from Ninja.mediaPipeProcessor import MediaPipeProcessor
import cv2

class Engine:
    """
    
    """
    def __init__(self, game:Game, interface:Interface):
        self.game = Game
        self.interface = interface
        self.camera = cv2.VideoCapture(0)
        self.gameState = GameState.MENU
        self.objects = []

    
    def startGame(self):
        self.gameOn = GameState.INGAME

    def endGame(self):
        self.gameOn = GameState.RECAPSCORE
    
    def returnToMenu(self):
        self.gameOn = GameState.MENU

    def updateObjectPositions(self):
        for _, i in enumerate(self.objects):
            self.objects[i].updatePosition()

    def updateInterface(self):
        pass

    def stopCamera(self):
        self.camera.release()
