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

        #Text for menu
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
        
        # FPS
        self.FPSposition = (self.menuThickness, self.windowHeight - self.menuThickness)
        
        #rock
        # self.rock = plt.imread("data/images/rock_1.png")
        # new_size = (100, 100)
        # self.rockAlpha = cv2.resize(self.rock[:, :,-1], new_size)
        # self.rockBGR = cv2.cvtColor(cv2.resize(self.rock[:, :, :3], new_size), cv2.COLOR_RGB2BGR)
        # self.rockBGR = (self.rockBGR * 255).astype(np.uint8)

        #Box position
        self.scoreBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight // 3 * 0.5))
        self.scoreBox = self.computeBoxCorner(self.scoreBoxMiddle)

        self.startBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight // 3 * 1.5))
        self.startBox = self.computeBoxCorner(self.startBoxMiddle)

        self.stopBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight // 3 * 2.5))
        self.stopBox = self.computeBoxCorner(self.stopBoxMiddle)

        #Objects for Interface
        self.rockMenuBGR, self.rockMenuAlpha = self.initImageAlphaBlending(plt.imread("data/images/rock_1.png"), 0.03)

        #Interface
        self.menuInterface = self.designMenuInterface()

    def float32ToUint8(self, image):
        new_image = (image.copy() * 255).astype(np.uint8)
        return new_image
    
    def computeBoxCorner(self, middle):
        corners = (
            (middle[0] - self.widthBox // 2, middle[1] - self.heightBox // 2),
            (middle[0] + self.widthBox // 2, middle[1] + self.heightBox // 2)
        )
        return corners
    
    def designMenuInterface(self):
        #background image
        shape = (self.windowHeight, self.windowWidth)
        num_channels = 3
        base_image = np.full((*shape, num_channels), self.backgroundColor).astype(np.uint8)

        base_image = self.drawMenuBorder(base_image)
        base_image = self.drawStartStop(base_image)
        #Draw Score Box without text
        base_image = self.drawBox(base_image, self.scoreBox)
        base_image = self.putImageThere(base_image, self.rockMenuBGR, (200, 300), alpha=self.rockMenuAlpha)
        return base_image

    def drawBox(self, image, coordinates):
        top_left = coordinates[0]
        bottom_right = coordinates[1]
        new_image = cv2.rectangle(image.copy(), top_left, bottom_right, self.mainColor, -1)
        return new_image
        
    def drawTextInBox(self, image, text, coordinates):
        #get coordinates
        top_left = coordinates[0]
        bottom_right = coordinates[1]
        #center text
        (w,h), _ = cv2.getTextSize(text, self.font, self.fontScale, self.textThickness)
        x_text = top_left[0] + (bottom_right[0] - top_left[0] - w) // 2
        y_text = top_left[1] + (bottom_right[1] - top_left[1] + h) // 2
        #draw text
        new_image = cv2.putText(image.copy(), text, (x_text, y_text), self.font, self.fontScale, self.textColor, self.textThickness)
        return new_image
    
    def drawBoxAndText(self, image, text, coordinates):
        #draw box
        new_image = self.drawBox(image.copy(), coordinates)
        #put text
        new_image = self.drawTextInBox(new_image, text, coordinates)
        return new_image

    def drawInterface(self, image, score, FPS, combo, multi):
        base_image = self.drawScore(score)
        base_image = self.drawFPS(base_image, FPS)
        base_image = self.drawComboAndMulti(base_image, combo, multi)
        base_image = self.drawVideo(base_image, image.copy())
        
        cv2.imshow(self.nameWindow, base_image)
    
    def initImageAlphaBlending(self, image, scaleFactor=None):
        new_image = image.copy()

        if scaleFactor is not None:
            new_image = self.scaleImage(new_image, scaleFactor)

        bgr, alpha = self.separateChannels(new_image)

        #Convert float to uint
        if bgr.max() < 1.01:
            bgr = self.float32ToUint8(bgr)
        
        return bgr, alpha
    
    def drawMenuBorder(self, image):
        top_left = (0, 0)
        bottom_right = (self.widthEmpty, self.heightEmpty)
        new_image = cv2.rectangle(image.copy(), top_left, bottom_right, self.menuColor, self.menuThickness)
        return new_image

    def drawStartStop(self, image):
        #Start
        new_image = self.drawBoxAndText(image.copy(), "Start", self.startBox)
        #Stop
        new_image = self.drawBoxAndText(new_image, "Stop", self.stopBox)
        return new_image

    def drawScore(self, score):
        #Get real score
        text = f"Score: {score}"
        new_image = self.drawTextInBox(self.menuInterface, text, self.scoreBox)
        return new_image

    def putImageThere(self, base_image, add_image, coordinates, alpha=None, scaleFactor=None):
        """
        base_image : background image
        add_image : foreground image with alpha channel (output of use plt.imread)
        coordinates : middle of objects will be added there
        scaleFactor: factor to increase or decrease image
        """

        new_image = base_image.copy()
        add_image_resize = add_image.copy()

        #Scale image
        if scaleFactor is not None:
            if alpha is None:
                add_image_resize = self.scaleImage(add_image_resize, scaleFactor)
            else:
                add_image_resize = self.scaleImage(add_image_resize, scaleFactor)
                alpha = self.scaleImage(alpha.copy(), scaleFactor)
        
        #alpha channel
        if alpha is None:
            bgr, alpha = self.separateChannels(add_image_resize)
        else:
            bgr = add_image_resize

        #Convert to uint if float
        if bgr.max() < 1.01:
            bgr = self.float32ToUint8(bgr)

        #determine coordinates
        x, y = coordinates[0], coordinates[1]
        h, w, _ = bgr.shape
        x_start = x - w // 2
        x_end = x + w - w // 2
        y_start = y - h // 2
        y_end = y + h - h // 2
        
        #Alpha blending
        new_image[y_start:y_end, x_start:x_end] = (
            bgr * alpha[..., np.newaxis] + 
            new_image[y_start:y_end, x_start:x_end] * (1 - alpha[..., np.newaxis])
        )
        return new_image

    def separateChannels(self, image):
        rgb = image[..., :3].copy()
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        alpha = image[..., -1].copy()
        return bgr, alpha

    def scaleImage(self, image, scaleFactor):
        hScaled = int(image.shape[0] * scaleFactor)
        wScaled = int(image.shape[1] * scaleFactor)
        image_resize = cv2.resize(image.copy(), (hScaled, wScaled))
        return image_resize

    def drawVideo(self, base_image, video):
        #get video on draw on top
        new_video = cv2.resize(video, (self.windowWidth - self.widthEmpty, self.windowHeight))
        new_image = base_image.copy()
        new_image[0:self.windowHeight, self.widthEmpty:self.windowWidth] = new_video
        return new_image
    
    def drawFPS(self, image, FPS):
        text = f"FPS: {FPS}"
        new_image = cv2.putText(image.copy(), text, self.FPSposition, self.font, 1, self.textColor, 1)
        return new_image
    
    def drawComboAndMulti(self, image, combo, multi):
        text = f"Combo: {combo} (x{multi})"
        new_image = cv2.putText(image.copy(), text, (10,10), self.font, 1, self.textColor, 1)
        return new_image