import tensorflow as tf
import numpy as np
import mediapipe as mp
import cv2

checkpoint_path = "services\\Checkpoints"
model = tf.keras.models.load_model(checkpoint_path +"\\no_face_with_aug.h5")

words = np.array(["book","drink","computer","before","chair","go","clothes","who","candy","cousin","deaf","fine","help","no","thin"])

mp_holistic = mp.solutions.holistic # human pose, face landmarks, and hand tracking 
mp_drawing = mp.solutions.drawing_utils # To draw the keypoints

MIN_FRAME_COUNT=24

def mp_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # By deafult captured image isn't rgb
    image.flags.writeable = False # Can't edit during processing
    results = model.process(image)
    image.flags.writeable = True 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    #return np.concatenate([pose, face, lh, rh])
    return np.concatenate([pose, lh, rh])

def predict_class_for_video(video_location):
    sequence = []
    #sentence = []
    predictions = {}
    #final_word = ""
    #threshold = 0.95
    
    cap = cv2.VideoCapture(video_location)
    cur_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    curr_skip_len = cur_len//MIN_FRAME_COUNT
    fram_no = 0
    count=0
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            # read frame
            ret, frame = cap.read()
            
            if(not(ret)):
                break
            
            # Make detections
            _, results = mp_detection(frame, holistic)
            
            keypoints = extract_keypoints(results)
            
            sequence.append(keypoints)
            sequence = sequence[-MIN_FRAME_COUNT:]

            fram_no += curr_skip_len
            count+=1
            if(count+1 >= MIN_FRAME_COUNT):
                break
            #currentPos = cap.get(cv2.CAP_PROP_POS_FRAMES)

            cap.set(cv2.CAP_PROP_POS_FRAMES, fram_no)
        
        res = model.predict(np.expand_dims(sequence, axis=0),verbose = 0)[0]
        #if(res[np.argmax(res)] > threshold):
        predictions.setdefault(words[np.argmax(res)], [1, res[np.argmax(res)]])
        predictions[words[np.argmax(res)]][0] += 1
        predictions[words[np.argmax(res)]][1] += res[np.argmax(res)]
            
    for key, value in predictions.items():
        predictions[key] = [value[0], value[1]/value[0]]
    #print(predictions)
    mylist = sorted(predictions.items(), key=lambda item: (-item[1][0], -item[1][1]))
    #print(mylist)
    return mylist[0]

