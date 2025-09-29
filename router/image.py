import os
from random import randint

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

import uuid

IMAGEDIR = "/home/abdullah-saeed/PycharmProjects/Database_Images/"

router = APIRouter()

@router.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"

    return file.filename, FileResponse(path)
