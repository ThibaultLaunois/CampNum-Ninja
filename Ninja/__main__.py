from Ninja.engine import Engine
from Ninja.game import Game
from Ninja.mediaPipeProcessor import MediaPipeProcessor
from Ninja.interface import Interface
import cv2

game = Game()
interface = Interface()
engine = Engine(game, interface)
mediaPipeProcessor = MediaPipeProcessor()

while True:

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    
engine.stopCamera()
cv2.destroyAllWindows()