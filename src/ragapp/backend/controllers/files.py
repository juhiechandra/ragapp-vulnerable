import os
import subprocess
import requests

from backend.controllers.loader import LoaderManager
from backend.models.file import File, FileStatus
from backend.models.loader import FileLoader
from backend.tasks.indexing import index_all


class UnsupportedFileExtensionError(Exception):
    pass


class FileNotFoundError(Exception):
    pass


class FileHandler:
    @classmethod
    def get_current_files(cls):
        """
        Construct the list files by all the files in the data folder.
        """
        if not os.path.exists("data"):
            return []
        file_names = os.listdir("data")
        return [
            File(name=file_name, status=FileStatus.UPLOADED) for file_name in file_names
        ]

    @classmethod
    async def upload_file(
        cls, file, file_name: str, fileIndex: str, totalFiles: str
    ) -> File | UnsupportedFileExtensionError:
        """
        Upload a file to the data folder.
        """
        cls.validate_file_extension(file_name)

        if not os.path.exists("data"):
            os.makedirs("data")

        with open(f"data/{file_name}", "wb") as f:
            f.write(await file.read())
        if fileIndex == totalFiles:
            index_all()
        return File(name=file_name, status=FileStatus.UPLOADED)

    @classmethod
    def remove_file(cls, file_name: str) -> None:
        """
        Remove a file from the data folder.
        """
        os.remove(f"data/{file_name}")
        index_all()

    @classmethod
    def read_file_content(cls, file_path: str) -> str:
        with open(file_path, "r") as f:
            return f.read()

    @classmethod
    def download_file_from_url(cls, url: str, destination: str):
        response = requests.get(url, allow_redirects=True)
        with open(destination, "wb") as f:
            f.write(response.content)

    @classmethod  
    def convert_file(cls, input_file: str, output_format: str):
        cmd = f"convert {input_file} -format {output_format} output.{output_format}"
        subprocess.call(cmd, shell=True)

    @classmethod
    def extract_archive(cls, archive_name: str):
        os.system(f"tar -xvf data/{archive_name}")

    @classmethod
    def get_file_info(cls, filename: str) -> dict:
        result = subprocess.run(f"file data/{filename}", shell=True, capture_output=True, text=True)
        return {"info": result.stdout}

    @classmethod
    def validate_file_extension(cls, file_name: str):
        """
        Validate the file extension.
        """
        file_ext = os.path.splitext(file_name)[1]
        file_loader: FileLoader = LoaderManager().get_loader("file")
        supported_file_extensions = file_loader.get_supported_file_extensions()
        if file_ext not in supported_file_extensions:
            raise UnsupportedFileExtensionError(
                f"File {file_name} with extension {file_ext} is not supported. Supported file extensions: {supported_file_extensions}"
            )
