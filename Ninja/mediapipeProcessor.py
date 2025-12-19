import cv2
import os 
import pickle

import mediapipe as mp
import numpy as np

class mediapipeProcessor:

    def __init__(self) -> None:
        Holistic = mp.solutions.holistic.Holistic
        self.model = Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # self.model_hands = mp.solutions.hands
        # self.hand_drawing = mp.solutions.drawing_utils


    def get_body_landmarks(self, image):
        '''
        Gets the landmarks for the body
        
        :param image: the image used to find the landmarks
        '''
        results = self.model.process(image) 
        return results.pose_landmarks
    

    def get_right_hand_landmarks(self, image):
        '''
        Gets the landmarks for the right hand
        
        :param image: the image used to find the landmarks
        '''        
        results = self.model.process(image)
        return results.right_hand_landmarks
    

    def get_left_hand_landmarks(self, image):
        '''
        Gets the landmarks for the left hand
        
        :param image: the image used to find the landmarks
        '''     
        results = self.model.process(image) 
        return results.left_hand_landmarks
    
    def get_hands(self, image, hands):
        results = hands.process(image)
        return results
    

    def format_landmarks(self, landmarks_in):
        """
        Transforms landmarks obtained from an image to a dictionary containing the index of 
        the landmarks and their corresponding coordinates

        :param landmarks_in: the landmarks to transform into the dictionary
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
        Find the landmarks for each hand seen in a folder of images

        :param source_path: the folder containing the images
        :param target_path: the folder to save the landmark information
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
            

    def landmarks_to_array(self, landmarks_dict):
        '''
        Converts landmark dictionary to landmark array
        
        :param landmarks_dict: dictionary containing information about the
                               landmarks
        '''
        res = np.zeros(shape=(33,3))
        res[:,0] = landmarks_dict["X"]
        res[:,1] = landmarks_dict["Y"]
        res[:,2] = landmarks_dict["Z"]
        return res
    

    def hand_landmarks_array(self, results, lm_num):
        '''
        Converts landmark dictionary to landmark array
        
        :param landmarks_dict: dictionary containing information about the
                               landmarks
        '''
        lm = np.zeros(shape=(len(results.multi_hand_landmarks), 3))

        for ind, hand_landmarks in enumerate(results.multi_hand_landmarks):

            lm[ind,0] = hand_landmarks.landmark[lm_num].x
            lm[ind,1] = hand_landmarks.landmark[lm_num].y 
            lm[ind,2] = hand_landmarks.landmark[lm_num].z

        return lm

    
