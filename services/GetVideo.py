import json
import cv2
import os

JSON_PATH_ASL= "F:/Academics/sem7/handPoseEstimation/dataset/WLASL_v0.3.json"
VIDEOS_PATH_ASL= f"F:/Academics/sem7/handPoseEstimation/dataset/videos/"

VIDEOS_PATH_ISL = f"F:/Academics/sem8/ISL_Data/videos/"
JSON_PATH_ISL = "F:/Academics/sem8/ISL_Data/WLISL_v0.1.json"


def get_video_ids(word,data):
    results = []
    for i in data:
        if(i['gloss'] == word):
            for j in i['instances']:
                results.append(j['video_id'])
    return results

def get_video(text,lang):
    JSON_PATH = ""
    VIDEOS_PATH = ""
    
    if(lang=="ASL"):
        JSON_PATH = JSON_PATH_ASL
        VIDEOS_PATH = VIDEOS_PATH_ASL
    else:
        JSON_PATH = JSON_PATH_ISL
        VIDEOS_PATH= VIDEOS_PATH_ISL

    with open(JSON_PATH) as f:
        data = json.loads(f.read())

    listOfVideoIDS = get_video_ids(text,data)
    listOfVideoPaths = []
    for wordID in listOfVideoIDS:
        path_to_video = VIDEOS_PATH + f"{wordID}.mp4"
        if(not os.path.exists(path_to_video)):
            continue
        listOfVideoPaths.append(path_to_video)
    return listOfVideoPaths