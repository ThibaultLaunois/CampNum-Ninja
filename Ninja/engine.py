import cv2

from Ninja.game import Game
from Ninja.interface import Interface

class Engine:
    """
    
    """
    def __init__(self, game:Game, interface:Interface):
        self.game = Game
        self.interface = Interface
        self.gameOn = False
        self.objects = []


    def initCamera(self):
        '''
        Turn on camera and set up video window
        '''
        self.video = cv2.VideoCapture(0)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
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


    def show_interface(self):
        while self.camera.isOpened():
            _, image = self.camera.read()
            image = cv2.flip(image, 1)
            
            cv2.imshow(self.nameWindow, image)
            self.interface.drawInterface(image)


            if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
            
        self.camera.release()
        cv2.destroyAllWindows()


    def startGame(self):
        pass

    def endGame(self):
        pass

    def updateInterface(self):
        pass
