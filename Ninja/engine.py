from Ninja.game import Game
from Ninja.gameMode import gameMode
from Ninja.gameState import GameState
from Ninja.interface import Interface
from Ninja.mediapipeProcessor import mediapipeProcessor
from Ninja.Object import Object
import random

import cv2
import numpy as np


class Engine:
    """
    
    """

    def __init__(self, game:Game, interface:Interface, mediapipeProcessor:mediapipeProcessor):
        self.game = Game()
        self.interface = interface
        self.gameMode = gameMode.PUSH
        self.gameState = GameState.MENU
        self.mediapipeProcessor = mediapipeProcessor
        self.objects = []
        self.validRadius = 5
        self.imageShape = False
        self.currentFPS = 30
        self.close = False

    def updateFPS(self, duration):
        self.currentFPS = min(int(1/duration), 30)


    def initCamera(self):
        '''
        Turn on camera and set up video window
        '''
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        self.fps = self.camera.get(cv2.CAP_PROP_FPS)
        cv2.setMouseCallback(self.interface.nameWindow, self.mouse_click)

    def mouse_click(self, event, x, y, flags, param):
        #start Game
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.interface.startBox[0][0] and 
                x < self.interface.startBox[1][0] and 
                y > self.interface.startBox[0][1] and
                y < self.interface.startBox[1][1]
            ):
                self.startGame()
        #Stop game
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.interface.stopBox[0][0] and 
                x < self.interface.stopBox[1][0] and 
                y > self.interface.stopBox[0][1] and
                y < self.interface.stopBox[1][1]
            ):
                self.endGame()
        #Close window
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.interface.quitBox[0][0] and 
                x < self.interface.quitBox[1][0] and 
                y > self.interface.quitBox[0][1] and
                y < self.interface.quitBox[1][1]
            ):
                self.close = True
        #Increase difficulty
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.interface.plusBox[0][0] and 
                x < self.interface.plusBox[1][0] and 
                y > self.interface.plusBox[0][1] and
                y < self.interface.plusBox[1][1]
            ):
                self.game.increaseDifficulty()
        #Decrease difficulty
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.interface.minusBox[0][0] and 
                x < self.interface.minusBox[1][0] and 
                y > self.interface.minusBox[0][1] and
                y < self.interface.minusBox[1][1]
            ):
                self.game.decreaseDifficulty()


    def startGame(self):
        self.gameState = GameState.INGAME
        self.game = Game(difficulty=self.game.difficulty)

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

    def gameLoop(self, hands, results_prev = None):
        '''
        Draws the interface when in game mode
        
        :param hands: hand detection object
        '''
        # Get image
        _, image = self.camera.read()
        image = cv2.flip(image, 1)

        if self.gameMode == gameMode.POP:
            results = self.mediapipeProcessor.get_hands(image, hands)

            # display landmarks
            image = self.displayLandmark(image, results)

            # detect touch
            self.detectTouchPop(results)
                
            # Update position of objects
            self.updateObjectPositions()

            # Randomly generate object (probability = 0.05 * difficulty)
            self.RandomAddObject()


        elif self.gameMode == gameMode.PUSH:
            results = self.mediapipeProcessor.get_hands(image, hands)

            # display landmarks
            image = self.displayLandmark(image, results)

            # detect touch
            self.detectTouchPush(results, results_prev)
                
            # Update position of objects
            self.updateObjectPositions()

            # Randomly generate object (probability = 0.05 * difficulty)
            self.RandomAddObject()
        
        # Add object to current image
        image = self.drawObjects(image)

        # Update duration left
        self.game.updateDuration()

        # Add interface on top of current image and show the result
        self.interface.drawInterface(image, self.game, self.currentFPS)

        # End game if time's up
        if self.game.duration < 0:
            self.endGame()

        return results


    def menuLoop(self, hands):
        '''
        Draws the interface when not in game mode (start menu and after quit)
        
        :param hands: hand detection object
        '''
        # Get image
        _, image = self.camera.read()
        image = cv2.flip(image, 1)
        if (not self.imageShape) and (image is not None):
            self.image_height, self.image_width, _ = image.shape
            self.imageShape = True

        results = self.mediapipeProcessor.get_hands(image, hands)

        image = self.displayLandmark(image, results)

        # Add interface on top of current image and show the result
        self.interface.drawInterface(image, self.game, self.currentFPS)

    def RandomAddObject(self):
        x = random.random() #between 0 and 1
        p = 0.01 * self.game.getDifficulty()
        if x < p:
            radius = np.random.randint(10, 20)
            obj = Object(type=None, position=(0, self.image_width), radius=radius)
            self.objects.append(obj)

    def drawObjects(self,image):
        for object in self.objects:
            image = cv2.circle(image, center=(int(object.position[0]),int(object.position[1])), 
                               radius=object.radius, 
                               color=object.color, 
                               thickness=-1)
            image = cv2.circle(image, center=(int(object.position[0]),int(object.position[1])), 
                               radius=object.radius+1, 
                               color=(55,55,55), 
                               thickness=1)
        return image
    
    def overlay_shape(self, image, landmark, shape_type='circle', color=(0, 0, 255), radius=5):
        '''
        Docstring for overlay_shape
        
        :param image: image that objects are detected from
        :param landmark: landmark that we want to draw on
        :param shape_type: the type of shape to overlay on the landmark
        :param color: the color of the overlaid shape
        :param radius: the radius of the overlaid shape
        '''
        height, width, _ = image.shape
        x = int(landmark.x * width)
        y = int(landmark.y * height)

        if shape_type == 'circle':
            cv2.circle(image, (x, y), radius, color, -1)
        elif shape_type == 'square':
            cv2.rectangle(image, (x - radius, y - radius), (x + radius, y + radius), color, -1)
        elif shape_type == 'star':
            pts = []
            for i in range(5):
                angle = i * 2 * np.pi / 5
                x_star = x + radius * np.cos(angle)
                y_star = y + radius * np.sin(angle)
                pts.append((int(x_star), int(y_star)))
            pts.append(pts[0])  # Close the polygon
            cv2.fillPoly(image, [np.array(pts)], color)

        return image
    
    def displayLandmark(self, image, results):
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # wrist = hand_landmarks.landmark[0]
                index_tip = hand_landmarks.landmark[9]
                # middle_tip = hand_landmarks.landmark[12]
                # Apply shapes to the landmarks
                # frame = self.overlay_shape(frame, wrist, shape_type='square', color=(0, 255, 0), radius=10)
                image = self.overlay_shape(image, index_tip, shape_type='circle', color=(255, 0, 0), radius=8)
                # frame = self.overlay_shape(frame, middle_tip, shape_type='circle', color=(0, 0, 255), radius=15)

        return image
    

    def detectTouchPop(self, results):
        '''
        Detect if the object is touched

        :param right_landmarks: landmarks detected for the right hand
        :param left_landmarks: landmarks detected for the left hand
        '''
        ind_to_delete = []
        for ind, object in enumerate(self.objects):     
            x, y = object.position[0], object.position[1]
            # Check if either hand has touched an object

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    x_loc = hand_landmarks.landmark[9].x * self.image_width
                    y_loc = hand_landmarks.landmark[9].y * self.image_height
                    if ((x - x_loc) ** 2 + (y - y_loc) ** 2) < object.radius ** 2:
                        self.game.combo += 1
                        self.game.updateMulti()
                        self.game.updateScore(5)
                        ind_to_delete.append(ind)

            # Store the indices of the objects that have left the frame
            if y > self.image_height:
                self.game.combo = 0
                self.game.updateMulti()
                ind_to_delete.append(ind)

        for index in sorted(list(set(ind_to_delete)), reverse=True):
            del self.objects[index]


    def detectTouchPush(self, results, results_previous=None):
        '''
        Detect if the object is touched

        :param right_landmarks: landmarks detected for the right hand
        :param left_landmarks: landmarks detected for the left hand
        '''

        for ind, object in enumerate(self.objects):     
            x, y = object.position[0], object.position[1]
            # Check if either hand has touched an object
            try:
                lm1 = self.mediapipeProcessor.hand_landmarks_array(results_previous, 9)
                lm2 = self.mediapipeProcessor.hand_landmarks_array(results, 9)

                for ind_array, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    x_loc = hand_landmarks.landmark[9].x * self.image_width
                    y_loc = hand_landmarks.landmark[9].y * self.image_height
                    if ((x - x_loc) ** 2 + (y - y_loc) ** 2) < object.radius ** 2:
                        # print('touched object')
                        # self.game.combo += 1
                        # self.game.updateMulti()
                        # self.game.updateScore(5)
                        ind_prev = np.argmin(np.sum((lm2[ind_array,:]-lm1)**2, axis=1))
                        vel = (self.objects[ind].radius * (lm2[ind_array, 0] - lm1[ind_prev, 0])* self.image_width, 
                               self.objects[ind].radius * (lm2[ind_array, 1] - lm1[ind_prev, 1])* self.image_height)
                        self.objects[ind].vitesse = vel
                        
            except:
                pass


            # # Store the indices of the objects that have left the frame
            # if y > self.image_height:
            #     self.endGame
    