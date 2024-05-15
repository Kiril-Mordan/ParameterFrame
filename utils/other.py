import datetime
import os
import random
from fastapi import UploadFile

from typing import List
from pathlib import Path
import shutil

def generate_random_name():
    # Get current datetime
    current_datetime = datetime.datetime.now()

    # Format datetime as string without microseconds
    datetime_str = current_datetime.strftime("%Y%m%d%H%M%S")

    # Generate 3 random digits
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(3)])

    # Concatenate datetime string and random digits
    random_name = f"{datetime_str}_{random_digits}"

    return os.path.join("persist", random_name)

def process_and_store_files(files: List[UploadFile], directory: str):
    # Create the upload directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Process each file and store them in the specified directory
    for uploaded_file in files:
        file_path = os.path.join(directory, uploaded_file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)