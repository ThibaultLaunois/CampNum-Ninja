import cv2
import os 
import pickle

import mediapipe as mp
import numpy as np

class mediapipeProcessor:

    def __init__(self) -> None:
        Holistic = mp.solutions.holistic.Holistic
        self.model = Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)


    def get_body_landmarks(self, image):
        results = self.model.process(image) 
        return results.pose_landmarks
    

    def get_right_hand_landmarks(self, image):
        results = self.model.process(image) 
        return results.right_hand_landmarks
    

    def get_left_hand_landmarks(self, image):
        results = self.model.process(image) 
        return results.left_hand_landmarks
    

    def format_landmarks(self, landmarks_in):
        """
        Transforms landmarks obtained from an image to a dictionary containing the index of 
        the landmarks and their corresponding coordinates.
        """
        landmarks = {
            "index": [],
            "X": [],
            "Y": [],
            "Z": []
        }

        for i, lm in enumerate(landmarks_in.landmark[:]):
            landmarks["index"].append(i)
            landmarks["X"].append(lm.x)
            landmarks["Y"].append(lm.y)
            landmarks["Z"].append(lm.z)

        return landmarks
    

    def get_hand_landmarks_from_folder(self, source_path, target_path):
        """
        
        """
        data = {
            "filename": [],
            "landmarks": []
        }
        for file in os.listdir(source_path):
            filename = f"{source_path}/{file}"
            try:
                image = cv2.imread(filename)
                right_hand = self.get_right_hand_landmarks(image)
                left_hand = self.get_left_hand_landmarks(image)
                if right_hand:
                    right_hand = self.format_landmarks(right_hand)
                    data["filename"].append(filename)
                    data["landmarks"].append(right_hand)
                if left_hand:
                    left_hand = self.format_landmarks(left_hand)
                    data["filename"].append(filename)
                    data["landmarks"].append(left_hand)
            except Exception as e:
                with open(f"{target_path}/log.txt", "a") as f:
                    f.write(f"{filename}\n")
                    f.write(f"{e}\n")

        with open(f'{target_path}/hand_landmarks.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            

    def landmarks_to_array(self, landmarks):
        res = np.zeros(shape=(33,3))
        res[:,0] = landmarks["X"]
        res[:,1] = landmarks["Y"]
        res[:,2] = landmarks["Z"]
        return res

    
