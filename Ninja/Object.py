import numpy as np

class Object:
    def __init__(self, type, vitesse=(0,20), acceleration =(0,0), taille=5, color=(0,0,0)):
        width_image = 800
        self.fps = 30
        self.position = (np.random.randint(0, width_image), 0)
        self.type = type
        self.vitesse = vitesse
        self.acceleration = acceleration
        self.taille = taille
        self.color = color


    def setColor(self, color_val):
        '''
        Changes the color of the object
        
        :param color_val: RGB value for color
        '''
        self.color = color_val


    def updatePos(self):
        '''
        Updates the position of the object each time the frame changes
        '''
        x_pos = self.position[0] + self.vitesse[0] * (1/self.fps) + 0.5 * self.acceleration[0] * (1/self.fps)**2
        y_pos = self.position[1] + self.vitesse[1] * (1/self.fps) + 0.5 * self.acceleration[1] * (1/self.fps)**2
        self.position = (x_pos, y_pos)

