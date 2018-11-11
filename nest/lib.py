import json
import os
from django.conf import settings


def load_json(filename):
    """Loads data from a JSON file to a Python dictionary
    JSON files are stored in the "/data" folder.

    Args:
        filename: Filename without extension.

    Returns: A python dictionary containing data from the json file.
        An empty dictionary will be returned if the data file is not found.

    """
    root = os.path.join(settings.BASE_DIR, "data")
    
    json_file = None
    file_path = os.path.join(root, filename)
    if os.path.exists(file_path):
        json_file = file_path
    elif os.path.exists(file_path + ".json"):
        json_file = file_path + ".json"
    
    if json_file:
        with open(json_file) as f:
            data = json.load(f)
    else:
        print("File Not Found.")
        data = {}
    return data


def ascii_char(char):
    """Returns the input character if it is an ASCII character, otherwise empty string.
    """
    if ord(char) > 127: 
        return ''
    else: 
        return char


def get_markdown_title(text):
    """Gets the title of a Markdown file.
    """
    lines = text.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line.strip("#").strip("\n").strip(" ")
    return ""


def search_file(search_dirs, filename, root=""):
    for directory in search_dirs:
        relative_path = os.path.join(directory, filename)

        if relative_path.startswith("/"):
            absolute_path = relative_path
        else:
            absolute_path = os.path.join(root, relative_path)

        if os.path.exists(absolute_path):
            return relative_path
    return None
