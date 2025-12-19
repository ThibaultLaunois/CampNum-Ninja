import numpy as np

class Object:
    def __init__(self, type, position=(0,500), vitesse=(0,150), acceleration =(0,0), radius=20, color=(255,255,255)):
        width_image = 800
        self.fps = 30
        self.position = (np.random.randint(position[0] + 0.05*position[1], position[1]*0.95), -radius)
        self.type = type
        self.vitesse = vitesse
        self.acceleration = acceleration
        self.radius = radius
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

