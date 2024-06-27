import json
import os
import shutil


def read_package_json(path):
    """
    Read and parse the package.json file.

    Args:
    path (str): Path to the package.json file

    Returns:
    dict: Parsed content of package.json

    Raises:
    FileNotFoundError: If package.json doesn't exist
    json.JSONDecodeError: If package.json is not valid JSON
    """
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"package.json not found at {path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON in package.json at {path}")


def write_package_json(path, data):
    """
    Write data to package.json file.

    Args:
    path (str): Path to the package.json file
    data (dict): Data to write to package.json

    Raises:
    PermissionError: If writing to the file is not permitted
    """
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    except PermissionError:
        raise PermissionError(f"Permission denied when writing to {path}")


def create_directory(path):
    """
    Create a directory if it doesn't exist.

    Args:
    path (str): Path of the directory to create

    Raises:
    PermissionError: If creating the directory is not permitted
    """
    try:
        os.makedirs(path, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"Permission denied when creating directory {path}")


def remove_directory(path):
    """
    Remove a directory and all its contents.

    Args:
    path (str): Path of the directory to remove

    Raises:
    PermissionError: If removing the directory is not permitted
    FileNotFoundError: If the directory doesn't exist
    """
    try:
        shutil.rmtree(path)
    except PermissionError:
        raise PermissionError(f"Permission denied when removing directory {path}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory not found: {path}")


def copy_file(src, dst):
    """
    Copy a file from source to destination.

    Args:
    src (str): Path of the source file
    dst (str): Path of the destination

    Raises:
    FileNotFoundError: If the source file doesn't exist
    PermissionError: If copying is not permitted
    """
    try:
        shutil.copy2(src, dst)
    except FileNotFoundError:
        raise FileNotFoundError(f"Source file not found: {src}")
    except PermissionError:
        raise PermissionError(f"Permission denied when copying {src} to {dst}")


def list_directory(path):
    """
    List contents of a directory.

    Args:
    path (str): Path of the directory to list

    Returns:
    list: List of items in the directory

    Raises:
    FileNotFoundError: If the directory doesn't exist
    PermissionError: If reading the directory is not permitted
    """
    try:
        return os.listdir(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Directory not found: {path}")
    except PermissionError:
        raise PermissionError(f"Permission denied when reading directory {path}")


def file_exists(path):
    """
    Check if a file exists.

    Args:
    path (str): Path of the file to check

    Returns:
    bool: True if the file exists, False otherwise
    """
    return os.path.isfile(path)


def directory_exists(path):
    """
    Check if a directory exists.

    Args:
    path (str): Path of the directory to check

    Returns:
    bool: True if the directory exists, False otherwise
    """
    return os.path.isdir(path)
