from Ninja.engine import Engine
from Ninja.game import Game
from Ninja.gameState import GameState
from Ninja.mediapipeProcessor import mediapipeProcessor
from Ninja.interface import Interface
import cv2

# Init game objects
game = Game()
interface = Interface()
mediaPipeProcessor = mediapipeProcessor()
engine = Engine(game, interface, mediaPipeProcessor)

# Open camera
engine.initCamera()

# Game loop
while True:
    if engine.gameState == GameState.INGAME:
        engine.gameLoop()
    else:
        engine.menuLoop()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close camera & windows
engine.stopCamera()
engine.closeWindows()