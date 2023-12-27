from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
import zipfile
import os
import re

app = FastAPI(title='Files storing app')


@app.post("/upload_file/{zipping}", response_model=int)
def upload_file(file: UploadFile, zipping: bool):
    """
    :param file: File to save on server
    :param zipping: Bool, whether add given file to zip or not

    :return: Unique id of stored file. Can be used to access certain file
    """
    # There is no need to write HTTPException 424, because "file" field is
    # required and user cannot run the query without attaching the file
    file_id = 0
    while os.path.isfile(f"id{file_id}_{file.filename}"):
        file_id += 1
    if not zipping:
        with open(f"id{file_id}_{file.filename}", "wb") as f:
            f.write(file.file.read())
        return file_id
    else:
        with open(f"id{file_id}_{file.filename}", "wb") as f:
            f.write(file.file.read())
        with zipfile.ZipFile(f"id{file_id}_{file.filename}.zip", 'w') as zipf:
            zipf.write(f"id{file_id}_{file.filename}")
        os.remove(f"id{file_id}_{file.filename}")
        return file_id


@app.get("/download_file/{file_id}", response_model=UploadFile)
def download_file(file_id: int):
    """
    :param file_id: Unique file id, used in uploading phase

    :return: File. It may be both original format or zipped, if zipped=True was provided during uploading
    """
    for file in os.listdir("../Task910"):
        if re.match(f"^id{file_id}_*", file):
            offset = 3 + len(str(file_id))  # to cut "id{file_id}_" from return file
            return FileResponse(file, filename=file[offset:])
    raise HTTPException(status_code=404, detail='No file with such id')
