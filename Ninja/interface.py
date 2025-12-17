#from Ninja.engine import Engine
#from Ninja.game import Game
from Ninja.gameMode import gameMode
import cv2
import numpy as np
import matplotlib.pyplot as plt

class Interface:
    def __init__(self):
        #Window
        self.nameWindow = "Press q to exit"
        self.windowWidth = 1600
        self.windowHeight = 900
        cv2.namedWindow(self.nameWindow)

        #Colors
        self.mainColor = (32, 165, 218)

        #BackGround
        self.backgroundColor = (225, 202, 253)

        #Text
        self.textColor = (218, 85, 32)
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.fontScale = 2
        self.textThickness = 2

        #Menu
        self.menuColor = (32, 72, 218)
        self.menuThickness = 10

        #Boxes
        self.widthEmpty = 400
        self.heightEmpty = 900
        self.widthBox = 300
        self.heightBox = 200

        #rock
        # self.rock = plt.imread("data/images/rock_1.png")
        # new_size = (100, 100)
        # self.rockAlpha = cv2.resize(self.rock[:, :,-1], new_size)
        # self.rockBGR = cv2.cvtColor(cv2.resize(self.rock[:, :, :3], new_size), cv2.COLOR_RGB2BGR)
        # self.rockBGR = (self.rockBGR * 255).astype(np.uint8)

        self.scoreBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight // 3 * 0.5))
        self.scoreBox = self.computeBoxCorner(self.scoreBoxMiddle)

        self.startBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight // 3 * 1.5))
        self.startBox = self.computeBoxCorner(self.startBoxMiddle)

        self.stopBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight // 3 * 2.5))
        self.stopBox = self.computeBoxCorner(self.stopBoxMiddle)
    
    def computeBoxCorner(self, middle):
        corners = (
            (middle[0] - self.widthBox // 2, middle[1] - self.heightBox // 2),
            (middle[0] + self.widthBox // 2, middle[1] + self.heightBox // 2)
        )
        return corners

    def drawInterface(self, image, score):
        shape = (self.windowHeight, self.windowWidth)
        num_channels = 3
        base_image = np.full((*shape, num_channels), self.backgroundColor).astype(np.uint8)
        #base_image[:0:self.windowWidth] = self.backgroundColor
        base_image = self.drawMenuBorder(base_image)
        base_image = self.drawStartStop(base_image)
        base_image = self.drawScore(base_image, score)
        base_image = self.drawVideo(base_image)
        #base_image = self.drawArock(base_image, 800, 320)

        cv2.imshow(self.nameWindow, base_image)

    # def drawArock(self, image, x, y):
    #     new_image = image.copy()
    #     w, h, _ = self.rockBGR.shape
    #     x_start = x - w // 2
    #     x_end = x + w - w // 2
    #     y_start = y - h // 2
    #     y_end = y + h - h // 2
    #     new_image[y_start:y_end, x_start:x_end] = (
    #         self.rockBGR * self.rockAlpha[..., np.newaxis] + 
    #         new_image[y_start:y_end, x_start:x_end] * (1 - self.rockAlpha[..., np.newaxis])
    #     )

        return new_image
    
    def drawMenuBorder(self, image):
        top_left = (0, 0)
        bottom_right = (self.widthEmpty, self.heightEmpty)
        new_image = cv2.rectangle(image, top_left, bottom_right, self.menuColor, self.menuThickness)
        return new_image

    def drawStartStop(self, image):
        #Start
        new_image = self.drawBox(image, "Start", self.startBox)
        #Stop
        new_image = self.drawBox(image, "Stop", self.stopBox)
        return new_image

    def drawScore(self, image, score):
        #Get real score
        text = f"Score: {score}"
        new_image = self.drawBox(image, text, self.scoreBox)
        return new_image
    
    def drawBox(self, image, text, coordinates):
        #draw box
        top_left = coordinates[0]
        bottom_right = coordinates[1]
        cv2.rectangle(image, top_left, bottom_right, self.mainColor, -1)
        #add a border ? add a shadow ?

        #center text
        (w,h), _ = cv2.getTextSize(text, self.font, self.fontScale, self.textThickness)
        x_text = top_left[0] + (bottom_right[0] - top_left[0] - w) // 2
        y_text = top_left[1] + (bottom_right[1] - top_left[1] + h) // 2

        #draw text
        new_image = cv2.putText(image, text, (x_text, y_text), self.font, self.fontScale, self.textColor, self.textThickness)

        return new_image

    def drawVideo(self, image):
        #get video on draw on top
        new_image = image
        return new_image