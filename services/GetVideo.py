import json
import cv2
import os

JSON_PATH = "C:/Users/nerfl/Downloads/archive/WLASL_v0.3.json"
VIDEOS_PATH = f"C:/Users/nerfl/Downloads/archive/videos/"

with open(JSON_PATH) as f:
    data = json.loads(f.read())

def get_video_ids(word):
    results = []
    for i in data:
        if(i['gloss'] == word):
            for j in i['instances']:
                results.append(j['video_id'])
    return results

def get_video(text):
    listOfVideoIDS = get_video_ids(text)
    listOfVideoPaths = []
    for wordID in listOfVideoIDS:
        path_to_video = VIDEOS_PATH + f"{wordID}.mp4"
        if(not os.path.exists(path_to_video)):
            continue
        listOfVideoPaths.append(path_to_video)
    return listOfVideoPaths