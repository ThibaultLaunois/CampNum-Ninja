import mediapipe as mp

from Ninja.engine import Engine
from Ninja.game import Game
from Ninja.gameState import GameState
from Ninja.mediapipeProcessor import mediapipeProcessor
from Ninja.interface import Interface
import cv2
import time
from argparse import ArgumentParser

#Parser
parser = ArgumentParser()
parser.add_argument('--debug', type=bool, required=False)
args = parser.parse_args()

# Init game objects
game = Game()
interface = Interface()
mediaPipeProcessor = mediapipeProcessor()
engine = Engine(game, interface, mediaPipeProcessor)
frame_duration = 1 / 30
# Open camera
engine.initCamera()

with mp.solutions.hands.Hands(max_num_hands=2,
                              min_detection_confidence=0.5,
                              min_tracking_confidence=0.3) as hands:
# Game loop
    while True:
        t_start = time.time()
        if engine.gameState == GameState.INGAME:
            engine.gameLoop(hands)
        else:
            engine.menuLoop(hands)
        t_end = time.time()
        duration = t_end - t_start
        engine.updateFPS(duration)
        if duration < frame_duration:
            time.sleep(frame_duration - duration)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if engine.close:
            break

# Close camera & windows
engine.stopCamera()
engine.closeWindows()