import json
import os
from django.conf import settings


def load_json(file_path, default=None):
    """Loads data from a JSON file to a Python dictionary

    Args:
        file_path: file path of a json file.
        default: default value to be returned if the file does not exist.
            If default is None and file is not found , an empty dictionary will be returned.

    Returns: A python dictionary containing data from the json file.
    """
    if os.path.exists(file_path):
        with open(file_path) as f:
            data = json.load(f)
    else:
        print("File %s Not Found." % file_path)
        if default:
            data = default
        else:
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
            return absolute_path
    return None


def summarize_markdown(filename, base_dir):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Title of the blog
        title = None
        # Date of the blog
        date = None
        # The first image
        image = None
        # Introduction text
        intro = ""
        for line in lines:
            if title and date and image and intro:
                break
            line = line.replace('\r', '').replace('\n', '')
            if len(line) == 0:
                continue
            if not title and line[0] == '#':
                title = line[1:].strip(' ')
                continue
            if not date and line[0] == '_' and line[-1] == '_':
                date = line.strip('_')
                continue
            if not image and line.startswith('!['):
                image = line[line.find("/static/"):].strip(')')
                continue
            if not intro and line[0].isalpha():
                if len(line) > 90:
                    intro = line[:line.find(' ', 90)]
                else:
                    intro = line
                intro = intro + '...'
                continue
        return {
            "title": title,
            "summary": intro,
            "date": date,
            "link": filename.split('.')[0].replace(base_dir, "")[1:],
            "image": image,
        }


class AImage:

    def __init__(self, filename):
        self.image_file = filename
        if not os.path.exists(self.image_file):
            raise IOError("File %s not found." % self.image_file)

    def resize_and_crop(self, output_file, to_width, to_height):
        from PIL import Image
        im = Image.open(self.image_file)
        w, h = im.size
        # Resize the image
        # w/h < to_w/to_h means the image is too tall
        if (w / h) < (to_width / to_height):
            # Preserve the width if the image is too tall
            im.thumbnail((to_width, to_width * 10), Image.ANTIALIAS)
        else:
            # Preserve the height if the image is too wide
            im.thumbnail((to_height * 10, to_height), Image.ANTIALIAS)
        w, h = im.size
        mid_w = w / 2
        mid_h = h / 2
        im = im.crop((mid_w - to_width / 2, mid_h - to_height / 2, mid_w + to_width / 2, mid_h + to_height / 2))
        im.save(output_file, "JPEG")


def resize_image(image_file, output_file, to_width, to_height):
    try:
        AImage(image_file).resize_and_crop(output_file, to_width, to_height)
        print("Re-sized %s" % image_file)
    except IOError as ex:
        print(ex)
        print("Cannot create thumbnail for '%s'" % image_file)


class AFolder:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

    @property
    def files(self):
        return [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]

    @property
    def folders(self):
        return [f for f in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, f))]

    def create(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def empty(self):
        for f in self.files:
            os.remove(os.path.join(self.path, f))
