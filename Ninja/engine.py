from Ninja.game import Game
from Ninja.gameState import GameState
from Ninja.interface import Interface
from Ninja.mediapipeProcessor import mediapipeProcessor

import cv2


class Engine:
    """
    
    """

    def __init__(self, game:Game, interface:Interface, mediapipeProcessor:mediapipeProcessor):
        self.game = Game
        self.interface = interface
        self.gameState = GameState.MENU
        self.mediapipeProcessor = mediapipeProcessor
        self.objects = []


    def initCamera(self):
        '''
        Turn on camera and set up video window
        '''
        self.camera = cv2.VideoCapture(0)
        self.fps = self.camera.get(cv2.CAP_PROP_FPS)
        self.nameWindow = "Press q to exit"
        cv2.namedWindow(self.nameWindow)
        cv2.setMouseCallback(self.nameWindow, self.mouse_click)
        self.windowWidth = 80
        self.counterOn = False


    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.interface.startBox[0][0] and 
                x < self.interface.startBox[1][0] and 
                y > self.interface.startBox[0][1] and
                y < self.interface.startBox[1][1]
            ):
                self.startGame()

        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.interface.stopBox[0][0] and 
                x < self.interface.stopBox[1][0] and 
                y > self.interface.stopBox[0][1] and
                y < self.interface.stopBox[1][1]
            ):
                self.endGame()


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
        
    def closeWindows(self):
        cv2.destroyAllWindows()

    def gameLoop(self):
        # Get image
        _, image = self.camera.read()
        image = cv2.flip(image, 1)
        
        # Generate object maybe

        cv2.imshow(self.nameWindow, image)
        self.interface.drawInterface(image)

    def decideIfDrawObject(self):
