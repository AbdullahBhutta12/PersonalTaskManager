from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

import uuid

IMAGEDIR = "/home/abdullah-saeed/Pictures/Screenshots/"

router = APIRouter()

@router.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename": file.filename}