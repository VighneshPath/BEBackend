from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from services.GetSignData import predict_class_for_video
from services.GetVideo import get_video
from fastapi import HTTPException


origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    with open("temp.mp4", "wb") as f:
        f.write(file.file.read())
    return {"predicted_class": predict_class_for_video("temp.mp4","ASL")}

@app.post("/uploadfileISL/")
async def create_upload_fileISL(file: UploadFile = File()):
    with open("temp.mp4", "wb") as f:
        f.write(file.file.read())
    return {"predicted_class": predict_class_for_video("temp.mp4","ISL")}


@app.get("/get-video/{text}")
async def get_video_from_text(text):
    vids = get_video(text.strip().lower(),"ASL")
    if(vids == []):
        raise HTTPException(status_code=400, detail= "word doesn't exist")
    
    return FileResponse(vids[0])

@app.get("/get-video-isl/{text}")
async def get_video_from_text(text):
    vids = get_video(text.strip().lower(),"ISL")
    if(vids == []):
        raise HTTPException(status_code=400, detail= "word doesn't exist")
    
    return FileResponse(vids[0])

