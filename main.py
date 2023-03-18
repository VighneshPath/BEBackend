from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from services.GetSignData import predict_class_for_video
from services.GetVideo import get_video

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    with open("temp.mp4", "wb") as f:
        f.write(file.file.read())
    return {"predicted_class": predict_class_for_video("temp.mp4")}


@app.post("/get-video/{text}")
async def get_video_from_text(text):
    vids = get_video(text.strip().lower())
    if(vids == []):
        return {"error": "word doesn't exist"}
    
    return FileResponse(vids[0])
