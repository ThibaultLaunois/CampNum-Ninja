import cv2
import os 
import pickle

import mediapipe as mp
import numpy as np

class mediapipeProcessor:
    

    def __init__(self) -> None:
        Holistic = mp.solutions.holistic.Holistic
        self.model = Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        #self.PompeCount = PompeCount
        self.camera = cv2.VideoCapture(0)
        self.nameWindow = "Press q to exit"
        cv2.namedWindow(self.nameWindow)
        cv2.setMouseCallback(self.nameWindow, self.mouse_click)
        self.windowWidth = 80
        #Start Button
        self.startButtonLocations = ((10, 10), (10 + self.windowWidth, 40))
        #Pause Button
        self.pauseButtonLocations = ((320 - self.windowWidth//2, 10), (320 + self.windowWidth//2, 40))
        #Restart Button
        self.restartButtonLocations = ((630 - self.windowWidth, 10), (630, 40))

        self.counterOn = False
        

    def mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.startButtonLocations[0][0] and 
                x < self.startButtonLocations[1][0] and 
                y > self.startButtonLocations[0][1] and
                y < self.startButtonLocations[1][1]
            ):
                self.counterOn = True

        if event == cv2.EVENT_LBUTTONDOWN:
            if (
                x > self.startButtonLocations[0][0] and 
                x < self.startButtonLocations[1][0] and 
                y > self.startButtonLocations[0][1] and
                y < self.startButtonLocations[1][1]
            ):
                self.counterOn = True

    def drawInterface(self, image):
        #start button
        cv2.rectangle(image, self.startButtonLocations[0], self.startButtonLocations[1], (0,0,0), -1)
        text = "Start"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 0, 0)
        thickness = 2
        (w, h), _ = cv2.getTextSize(text, font, font_scale, thickness)
        x_text = self.startButtonLocations[0][0] - w//2
        y_text = (self.startButtonLocations[0][1] - h)//2
        image = cv2.putText(image, text, (x_text, y_text), font, font_scale, color, thickness)
        
        #stop button
        cv2.rectangle(image, self.pauseButtonLocations[0], self.pauseButtonLocations[1], (0,0,0), -1)

        #reset button
        cv2.rectangle(image, self.restartButtonLocations[0], self.restartButtonLocations[1], (0,0,0), -1)

        if self.counterOn:
                #execute step to count pomp
                text = "Counter ON"
                position = (200, 200)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                color = (255, 0, 0)
                thickness = 2
                image = cv2.putText(image, text, position, font, font_scale, color, thickness)
    
    def get_pose_world_landmarks(self, image):
        results = self.model.process(image) 
        return results.pose_world_landmarks
    
    def show_interface(self):
        while self.camera.isOpened():
            #count_pompe = self.PompeCount.getPompeCount
            _, image = self.camera.read()
            image = cv2.flip(image, 1)
            
            #Compute things
            
            self.drawInterface(image)
            cv2.imshow(self.nameWindow, image)


            if cv2.waitKey(5) & 0xFF == ord('q'):
                    break
            
        self.camera.release()
        cv2.destroyAllWindows()

    
    def format_landmarks(self, world_landmarks):
        """
        Transforms the output of `get_pose_world_landmarks()` for a given imagefrom LandmarkList object to 
        a dictionnary containing the index of landmarks, and its corresponding coordinates 
        """
        landmarks = {
            "index": [],
            "X": [],
            "Y": [],
            "Z": []
        }

        for i, lm in enumerate(world_landmarks.landmark[:]):
            landmarks["index"].append(i)
            landmarks["X"].append(lm.x)
            landmarks["Y"].append(lm.y)
            landmarks["Z"].append(lm.z)

        return landmarks
    
    def get_landmarks_from_folder(self, source_path, target_path):
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
                world_landmarks = self.get_pose_world_landmarks(image)
                landmarks = self.format_landmarks(world_landmarks)
                data["filename"].append(filename)
                data["landmarks"].append(landmarks)
            except Exception as e:
                with open(f"{target_path}/log.txt", "a") as f:
                    f.write(f"{filename}\n")
                    f.write(f"{e}\n")

        with open(f'{target_path}/landmarks.pickle', 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
    def landmarks_to_array(self, landmarks):
        res = np.zeros(shape=(33,3))
        res[:,0] = landmarks["X"]
        res[:,1] = landmarks["Y"]
        res[:,2] = landmarks["Z"]
        return res

    
