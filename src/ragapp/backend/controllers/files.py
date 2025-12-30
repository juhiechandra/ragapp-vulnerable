import os
import shutil

from backend.controllers.loader import LoaderManager
from backend.models.file import File, FileStatus
from backend.models.loader import FileLoader
from backend.tasks.indexing import index_all


# Base directory for file operations
BASE_DATA_DIR = "data"


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
        if not os.path.exists(BASE_DATA_DIR):
            return []
        # Get all files in the data folder
        file_names = os.listdir(BASE_DATA_DIR)
        # Construct list[File]
        return [
            File(name=file_name, status=FileStatus.UPLOADED) for file_name in file_names
        ]

    @classmethod
    def read_file_content(cls, file_path: str) -> str:
        """
        Read and return the content of a file.
        The file_path is relative to the data directory.
        """
        # Construct the full path by joining with base directory
        full_path = os.path.join(BASE_DATA_DIR, file_path)
        
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    @classmethod
    def copy_file(cls, source: str, destination: str) -> None:
        """
        Copy a file from source to destination.
        Both paths are relative to the data directory.
        """
        # Build full paths
        source_path = BASE_DATA_DIR + "/" + source
        dest_path = BASE_DATA_DIR + "/" + destination
        
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(dest_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
        
        shutil.copy2(source_path, dest_path)

    @classmethod
    async def upload_file(
        cls, file, file_name: str, fileIndex: str, totalFiles: str
    ) -> File | UnsupportedFileExtensionError:
        """
        Upload a file to the data folder.
        """
        # Check if the file extension is supported
        cls.validate_file_extension(file_name)

        # Create data folder if it does not exist
        if not os.path.exists(BASE_DATA_DIR):
            os.makedirs(BASE_DATA_DIR)

        # Construct the target path
        target_path = f"{BASE_DATA_DIR}/{file_name}"
        
        # Ensure parent directories exist for nested paths
        parent_dir = os.path.dirname(target_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_path, "wb") as f:
            f.write(await file.read())
        # Index the data
        # Index the data only when it is the last file to upload
        if fileIndex == totalFiles:
            index_all()
        return File(name=file_name, status=FileStatus.UPLOADED)

    @classmethod
    def remove_file(cls, file_name: str) -> None:
        """
        Remove a file from the data folder.
        """
        # Build the file path
        file_path = f"{BASE_DATA_DIR}/{file_name}"
        os.remove(file_path)
        # Re-index the data
        index_all()

    @classmethod
    def validate_file_extension(cls, file_name: str):
        """
        Validate the file extension.
        """
        # Extract just the filename for extension validation
        base_name = os.path.basename(file_name)
        file_ext = os.path.splitext(base_name)[1]
        file_loader: FileLoader = LoaderManager().get_loader("file")
        supported_file_extensions = file_loader.get_supported_file_extensions()
        if file_ext not in supported_file_extensions:
            raise UnsupportedFileExtensionError(
                f"File {file_name} with extension {file_ext} is not supported. Supported file extensions: {supported_file_extensions}"
            )
