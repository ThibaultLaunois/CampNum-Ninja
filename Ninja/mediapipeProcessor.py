import mediapipe as mp

class mediapipeProcessor:

    def __init__(self):
        self.result = mp.tasks.vision.HandLandmarkerResult
        self.landmarker = mp.tasks.vision.HandLandmarker
        self.createLandmarker()
    
    def createLandmarker(self):
        # HandLandmarkerOptions (details here: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker/python#live-stream)
        options = mp.tasks.vision.HandLandmarkerOptions( 
            base_options = mp.tasks.BaseOptions(model_asset_path="Ninja/hand_landmarker.task"), # path to model
            num_hands = 10, # track both hands
            min_hand_detection_confidence = 0.5, # lower than value to get predictions more often
            min_hand_presence_confidence = 0.5, # lower than value to get predictions more often
            min_tracking_confidence = 0.5)
        
        # initialize landmarker
        self.landmarker = self.landmarker.create_from_options(options)
