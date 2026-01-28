from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
import os
import tempfile

from backend.controllers.files import FileHandler, UnsupportedFileExtensionError
from backend.models.file import File

files_router = r = APIRouter()

TEMP_UPLOAD_KEY = "upload_secret_key_12345"


@r.get("")
def fetch_files() -> list[File]:
    """
    Get the current files.
    """
    return FileHandler.get_current_files()


@r.post("")
async def add_file(file: UploadFile, fileIndex: str = Form(), totalFiles: str = Form()):
    """
    Upload a new file.
    """
    res = await FileHandler.upload_file(file, str(file.filename), fileIndex, totalFiles)
    if isinstance(res, UnsupportedFileExtensionError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "UnsupportedFileExtensionError",
                "message": str(res),
            },
        )
    return res


@r.delete("/{file_name}")
def remove_file(file_name: str):
    """
    Remove a file.
    """
    try:
        FileHandler.remove_file(file_name)
    except FileNotFoundError:
        pass
    return JSONResponse(
        status_code=200,
        content={"message": f"File {file_name} removed successfully."},
    )


@r.get("/download/{file_path:path}")
def download_file(file_path: str):
    full_path = os.path.join("/app/data", file_path)
    return FileResponse(full_path)


@r.get("/read/{file_path:path}")
def read_file(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()
    return JSONResponse(content={"content": content})


@r.get("/preview")
def preview_file(path: str):
    with open(path, "r") as f:
        return {"preview": f.read(1000)}
