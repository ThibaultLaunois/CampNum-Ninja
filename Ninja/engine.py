from Ninja.game import Game
from Ninja.gameState import GameState
from Ninja.interface import Interface
from Ninja.mediapipeProcessor import mediapipeProcessor
from Ninja.Object import Object
import random

import cv2


class Engine:
    """
    
    """

    def __init__(self, game:Game, interface:Interface, mediapipeProcessor:mediapipeProcessor):
        self.game = Game()
        self.interface = interface
        self.gameState = GameState.MENU
        self.mediapipeProcessor = mediapipeProcessor
        self.objects = []
        self.validRadius = 5
        self.imageShape = False


    def initCamera(self):
        '''
        Turn on camera and set up video window
        '''
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        self.fps = self.camera.get(cv2.CAP_PROP_FPS)
        cv2.setMouseCallback(self.interface.nameWindow, self.mouse_click)



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
        self.gameState = GameState.INGAME
        self.game = Game()

    def endGame(self):
        self.gameState = GameState.RECAPSCORE
        self.objects = []
    
    def returnToMenu(self):
        self.gameState = GameState.MENU

    def updateObjectPositions(self):
        for i, _ in enumerate(self.objects):
            self.objects[i].updatePos()
    
    def stopCamera(self):
        self.camera.release()
        
    def closeWindows(self):
        cv2.destroyAllWindows()

    def gameLoop(self):

        # Get image
        _, image = self.camera.read()
        image = cv2.flip(image, 1)

        # Check if object to delete
        right_landmarks = self.mediapipeProcessor.get_right_hand_landmarks(image)
        left_landmarks = self.mediapipeProcessor.get_left_hand_landmarks(image)
        self.detectTouch(right_landmarks, left_landmarks)

        # Update position of objects
        self.updateObjectPositions()

        # Randomly generate object (probability = 0.05 * difficulty)
        self.RandomAddObject()
        
        # Add object to current image
        image = self.drawObjects(image)

        # Add interface on top of current image and show the result
        self.interface.drawInterface(image, self.game.getScore())

    def menuLoop(self):

        # Get image
        _, image = self.camera.read()
        image = cv2.flip(image, 1)
        if (not self.imageShape) and (image is not None):
            self.image_height, self.image_width, _ = image.shape
            self.imageShape = True
        # Check if object to delete
        #right_landmarks = self.mediapipeProcessor.get_right_hand_landmarks(image)
        #left_landmarks = self.mediapipeProcessor.get_left_hand_landmarks(image)

        # Add interface on top of current image and show the result
        self.interface.drawInterface(image, self.game.getScore())

    def RandomAddObject(self):
        x = random.random() #between 0 and 1
        p = 0.1 * self.game.getDifficulty()
        if x < p:
            obj = Object(type=None, position=(0, self.image_width))
            self.objects.append(obj)

    def drawObjects(self,image):
        for object in self.objects:
            image = cv2.circle(image, center=(int(object.position[0]),int(object.position[1])), 
                               radius=object.radius, 
                               color=object.color, 
                               thickness=-1)
        return image

    def detectTouch(self, right_landmarks, left_landmarks):
        ind_to_delete = []
        for ind, object in enumerate(self.objects):     
            x, y = object.position[0], object.position[1]
            try:
                x_loc = right_landmarks.landmark[9].x * self.image_width
                y_loc = right_landmarks.landmark[9].y * self.image_height
                if (((x - x_loc < object.radius) &
                    (x + object.radius > x_loc) &
                    (y - object.radius < y_loc) &
                    (y + object.radius > y_loc))):
                    self.game.updateScore(5)
                    ind_to_delete.append(ind)
            except:
                pass

            try:
                x_loc = left_landmarks.landmark[9].x * self.image_width
                y_loc = left_landmarks.landmark[9].y * self.image_height
                if ((x - object.radius < x_loc) &
                    (x + object.radius > x_loc) &
                    (y - object.radius < y_loc) &
                    (y + object.radius > y_loc)):
                    self.game.updateScore(5)
                    ind_to_delete.append(ind)
            except:
                pass

            if y > self.image_height:
                ind_to_delete.append(ind)

        for index in sorted(ind_to_delete, reverse=True):
            del self.objects[index]