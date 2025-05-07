# /app/utils/file_utils.py
import os
import shutil
import uuid
from fastapi import UploadFile
from typing import Optional

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads") # Get from .env or default

def save_upload_file_sync(upload_file: UploadFile) -> Optional[str]:
    """Saves an uploaded file synchronously to the UPLOAD_DIR."""
    if not upload_file or not upload_file.filename:
        return None

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    _, ext = os.path.splitext(upload_file.filename)
    unique_filename = f"{uuid.uuid4()}{ext}"
    destination_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(destination_path, "wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    except Exception as e:
        print(f"Error saving file {unique_filename}: {e}")
        # Clean up partially written file if error occurs
        if os.path.exists(destination_path):
            os.remove(destination_path)
        return None # Indicate failure
    finally:
        upload_file.file.close() # Ensure file handle is closed

    return unique_filename