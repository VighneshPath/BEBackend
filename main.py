from typing import Union

from fastapi import FastAPI, File, UploadFile

from models.GetSignData import predict_class_for_video

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    with open("temp.mp4", "wb") as f:
        f.write(file.file.read())
    return {"predicted_class": predict_class_for_video("temp.mp4")}