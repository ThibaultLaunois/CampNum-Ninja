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
        self.mainColor = (255, 210, 162)
        self.plusMinusColor = (204, 175, 255)

        #BackGround
        self.backgroundColor = (221, 200, 255)

        #Text for menu
        self.textColor = (0, 0, 0)#(219, 180, 205)
        self.font = cv2.FONT_HERSHEY_DUPLEX #cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.fontScale = 1 #2
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
        self.smallBoxSize = 50
        #determine box size dynamically ??
        #determine box position dynamically ??

        #Shadow of boxes
        self.shadowOffset = 4
        # FPS
        self.FPSposition = (self.menuThickness, self.windowHeight - self.menuThickness)
        #Objects for Interface
        self.rockMenuBGR, self.rockMenuAlpha = self.initImageAlphaBlending(plt.imread("data/images/rock_1.png"), 0.03)
        #Interface
        self.menuInterface = self.designMenuInterface()

    def float32ToUint8(self, image):
        new_image = (image.copy() * 255).astype(np.uint8)
        return new_image
    
    def initMenuBoxes(self):
        #Time
        self.timeBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight * 0.1))
        self.timeBox = self.computeBoxCorner(self.timeBoxMiddle, self.widthBox, self.smallHeightBox)
        #Score Combo Multi
        self.scoreBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight * 0.3))
        self.scoreBox = self.computeBoxCorner(self.scoreBoxMiddle, self.widthBox, self.heightBox)
        #Difficulty
        self.difficultyBoxMiddle = (self.widthEmpty // 2, int(self.windowHeight * 0.55))
        self.difficultyBox = self.computeBoxCorner(self.difficultyBoxMiddle, self.widthBox, self.heightBox)
        #minus difficulty
        self.minusBoxMiddle = self.computeMinusBoxMiddle()
        self.minusBox = self.computeBoxCorner(self.minusBoxMiddle, self.smallBoxSize, self.smallBoxSize)
        #plus difficulty
        self.plusBoxMiddle = self.computePlusBoxMiddle()
        self.plusBox = self.computeBoxCorner(self.plusBoxMiddle, self.smallBoxSize, self.smallBoxSize)
        #Start
        self.startBoxMiddle = ((self.widthEmpty - self.spaceBetweenStartStopBox - self.widthStartStopBox) // 2, int(self.windowHeight * 0.75))
        self.startBox = self.computeBoxCorner(self.startBoxMiddle, self.widthStartStopBox, self.heightStartStopBox)
        #Stop
        self.stopBoxMiddle = ((self.widthEmpty + self.spaceBetweenStartStopBox + self.widthStartStopBox) // 2, int(self.windowHeight * 0.75))
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
    
    def computeMinusBoxMiddle(self):
        heightDifficultyBox = self.difficultyBox[1][1] - self.difficultyBox[0][1]
        widthDifficultyBox = self.difficultyBox[1][0] - self.difficultyBox[0][0]

        y = self.difficultyBoxMiddle[1] + heightDifficultyBox // 4
        x = self.difficultyBoxMiddle[0] - widthDifficultyBox // 6
        return (x, y)
    
    def computePlusBoxMiddle(self):
        heightDifficultyBox = self.difficultyBox[1][1] - self.difficultyBox[0][1]
        widthDifficultyBox = self.difficultyBox[1][0] - self.difficultyBox[0][0]

        y = self.difficultyBoxMiddle[1] + heightDifficultyBox // 4
        x = self.difficultyBoxMiddle[0] + widthDifficultyBox // 6
        return (x,y)
    
    def designMenuInterface(self):
        #Init parameters for the boxes, needed for the mouse
        self.initMenuBoxes()

        #background image
        shape = (self.windowHeight, self.windowWidth)
        num_channels = 3
        base_image = np.full((*shape, num_channels), self.backgroundColor).astype(np.uint8)

        base_image = self.drawMenuBorder(base_image)
        base_image = self.drawStartStop(base_image)
        base_image = self.drawDifficultyBox(base_image)
        #Quit Button
        base_image = self.drawBoxAndText(base_image, "Quit (or q)", self.quitBox)
        #Draw ScoreMultiCombo Box without text
        base_image = self.drawRoundedBoxWithShadow(base_image, self.scoreBox)
        #Draw time box without text
        base_image = self.drawRoundedBoxWithShadow(base_image, self.timeBox)
        
        #Draw decorative elements
        #base_image = self.putImageThere(base_image, self.rockMenuBGR, (200, 300), alpha=self.rockMenuAlpha)
        return base_image

    def drawBox(self, image, coordinates):
        top_left = coordinates[0]
        bottom_right = coordinates[1]
        new_image = cv2.rectangle(image.copy(), top_left, bottom_right, self.mainColor, -1)
        return new_image
        
    def drawTextInBox(self, image, text, coordinates, line = 1, lineTotal = 1, align = "middle"):
        #get coordinates
        top_left = coordinates[0]
        bottom_right = coordinates[1]

        if align == "middle":
            #center text
            widthBox = bottom_right[0] - top_left[0]
            heightBox = bottom_right[1] - top_left[1]
            (w, h), _ = cv2.getTextSize(text, self.font, self.fontScale, self.textThickness)
            x_text = top_left[0] + (bottom_right[0] - top_left[0] - w) // 2
            y_text = top_left[1] + heightBox * line // (lineTotal+1) + h // 2
        elif align == "left":
            
            pass
        elif align == "right":
            print("To implement")
        else:
            print(f"{align}: Option does not exists")

        #draw text
        new_image = cv2.putText(image.copy(), text, (x_text, y_text), self.font, self.fontScale, self.textColor, self.textThickness)
        return new_image
    
    def drawBoxAndText(self, image, text, coordinates, color=None):
        if color is None:
            color = self.mainColor
        #draw box
        new_image = self.drawRoundedBoxWithShadow(image.copy(), coordinates, color)
        #put text
        new_image = self.drawTextInBox(new_image, text, coordinates)
        return new_image

    def drawInterface(self, image, game, FPS):
        base_image = self.menuInterface.copy()
        #Dynamic text in game
        base_image = self.drawTime(base_image, game.duration)
        base_image = self.drawScoreComboMulti(base_image, game.score, game.combo, game.scoreMulti)
        base_image = self.drawFPS(base_image, FPS)
        base_image = self.drawDifficulty(base_image, game.difficulty)
        #Video
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

    def drawDifficultyBox(self, base_image):
        base_image = self.drawRoundedBoxWithShadow(base_image.copy(), self.difficultyBox)
        base_image = self.drawBoxAndText(base_image, "+", self.plusBox, color=self.plusMinusColor)
        base_image = self.drawBoxAndText(base_image, "-", self.minusBox, color=self.plusMinusColor)
        return base_image

    def drawDifficulty(self, base_image, difficulty):
        text = f"Difficulty: {difficulty}"
        new_image = self.drawTextInBox(base_image.copy(), text, self.difficultyBox, line=1, lineTotal=2)
        return new_image

    def drawScoreComboMulti(self, base_image, score, combo, multi):
        #Get real score
        text = f"Score: {score}"
        new_image = self.drawTextInBox(base_image.copy(), text, self.scoreBox, line=1, lineTotal=2)
        #Combo and multi
        text = f"Combo: {combo} (x{multi})"
        new_image = self.drawTextInBox(new_image, text, self.scoreBox, line=2, lineTotal=2)
        return new_image

    def drawTime(self, base_image, time):
        text = f"Time left: {int(time)}"
        new_image = self.drawTextInBox(base_image.copy(), text, self.timeBox)
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
    
    def drawRoundedBoxWithShadow(self, image, coordinates, color=None, radius=22):
        if color is None:
            color = self.mainColor
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

    def drawRoundedBox(self, image, coordinates, radius=22, color=None):
        if color is None:
            color = self.mainColor
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