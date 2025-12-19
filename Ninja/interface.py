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

        #Boxes sizes
        self.widthEmpty = 400
        self.heightEmpty = 900
        self.widthBox = 300
        self.heightBox = 200
        self.spaceBetweenStartStopBox = 10
        self.widthStartStopBox = (self.widthBox - self.spaceBetweenStartStopBox) // 2
        self.heightStartStopBox = 100
        self.smallHeightBox = 100

        self.shadowOffset = 4
        
        # FPS
        self.FPSposition = (self.menuThickness, self.windowHeight - self.menuThickness)

        #Objects for Interface
        self.rockMenuBGR, self.rockMenuAlpha = self.initImageAlphaBlending(plt.imread("data/images/heart.png"), 1)

        #Interface
        self.menuInterface = self.designMenuInterface()

    def float32ToUint8(self, image):
        new_image = (image.copy() * 255).astype(np.uint8)
        return new_image
    
    def initMenuBoxes(self):
        #Score Combo Multi
        self.scoreBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight // 3 * 0.5))
        self.scoreBox = self.computeBoxCorner(self.scoreBoxMiddle, self.widthBox, self.heightBox)

        #Difficulty

        #minus difficulty

        #plus difficulty

        #Start
        self.startBoxMiddle = ((self.widthEmpty - self.spaceBetweenStartStopBox - self.widthStartStopBox) // 2, int(self.windowHeight // 3 * 1.5))
        self.startBox = self.computeBoxCorner(self.startBoxMiddle, self.widthStartStopBox, self.heightStartStopBox)

        #Stop
        self.stopBoxMiddle = ((self.widthEmpty + self.spaceBetweenStartStopBox + self.widthStartStopBox) // 2, int(self.windowHeight // 3 * 1.5))
        self.stopBox = self.computeBoxCorner(self.stopBoxMiddle, self.widthStartStopBox, self.heightStartStopBox)

        #Quit
        self.quitBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight * 0.9))
        self.quitBox = self.computeBoxCorner(self.quitBoxMiddle, self.widthBox, self.smallHeightBox)

    def computeBoxCorner(self, middle, width, height):
        corners = (
            (middle[0] - width // 2, middle[1] - height // 2),
            (middle[0] + (width - width // 2), middle[1] + (height - height // 2))
        )
        return corners
    
    def designMenuInterface(self):
        #Init parameters for the boxes, needed for the mouse
        self.initMenuBoxes()

        #background image
        shape = (self.windowHeight, self.windowWidth)
        num_channels = 3
        base_image = np.full((*shape, num_channels), self.backgroundColor).astype(np.uint8)

        base_image = self.drawMenuBorder(base_image)
        base_image = self.drawStartStop(base_image)
        #Quit Button
        base_image = self.drawBoxAndText(base_image, "Quit (or q)", self.quitBox)
        #Draw ScoreMultiCombo Box without text
        base_image = self.drawRoundedBoxWithShadow(base_image, self.scoreBox)
        #Draw a random rock
        #base_image = self.putImageThere(base_image, self.rockMenuBGR, (200, 300), alpha=self.rockMenuAlpha)
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
        new_image = self.drawRoundedBoxWithShadow(image.copy(), coordinates)
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
        x_start = x - (w // 2)
        x_end = x + w - (w // 2)
        y_start = max(y - (h // 2), 0)
        y_end = min(y + h - (h // 2), new_image.shape[0])
        real_height = y_end - y_start
        
        #Alpha blending
        if y_start == 0:
            new_image[y_start:y_end, x_start:x_end] = (
                bgr[h-real_height:, :] * alpha[h-real_height:, :, np.newaxis] + 
                new_image[y_start:y_end, x_start:x_end] * (1 - alpha[h-real_height:, :, np.newaxis])
            )
        else:
            new_image[y_start:y_end, x_start:x_end] = (
                bgr[:(real_height), :] * alpha[:(real_height), :, np.newaxis] + 
                new_image[y_start:y_end, x_start:x_end] * (1 - alpha[:(real_height), :, np.newaxis])
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
    
    def drawRoundedBoxWithShadow(self, image, coordinates, radius=22, color=(255, 200, 230)):
        new_image = image.copy()
        coordinatesShadow = self.shadow(coordinates, self.shadowOffset)

        new_image = self.drawRoundedBox(new_image, coordinatesShadow, radius=radius, color=(0,0,0))
        new_image = self.drawRoundedBox(new_image, coordinates, radius=radius, color=color)
        return new_image

    def shadow(self, coordinates, offset):
        coordNp = np.array(coordinates)
        #coordNp -= offset
        coordNp += offset
        coordNew = (
            (coordNp[0][0], coordNp[0][1]),
            (coordNp[1][0], coordNp[1][1])
        )
        return coordNew

    def drawRoundedBox(self, image, coordinates, radius=22, color=(255, 200, 230)):
        new_image = image.copy()
        x1, y1 = coordinates[0]
        x2, y2 = coordinates[1]
        radius = int(max(0, min(radius, abs(x2-x1)//2, abs(y2-y1)//2)))
        
        new_image = cv2.rectangle(new_image, (x1+radius, y1), (x2-radius, y2), color, -1)
        new_image = cv2.rectangle(new_image, (x1, y1+radius), (x2, y2-radius), color, -1)
        new_image = cv2.circle(new_image, (x1+radius, y1+radius), radius, color, -1)
        new_image = cv2.circle(new_image, (x2-radius, y1+radius), radius, color, -1)
        new_image = cv2.circle(new_image, (x1+radius, y2-radius), radius, color, -1)
        new_image = cv2.circle(new_image, (x2-radius, y2-radius), radius, color, -1)

        return new_image
    
    def drawComboAndMulti(self, image, combo, multi):
        text = f"Combo: {combo} (x{multi})"
        new_image = cv2.putText(image.copy(), text, (40,40), self.font, 1, self.textColor, 1)
        return new_image