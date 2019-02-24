import os
import json
import re
from operator import itemgetter
from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image


SWAN_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown", "swan")
THUMBNAIL_FOLDER = os.path.join(settings.BASE_DIR, "static", "images", "swan", "home")
IMAGE_SUB_FOLDER = "static/images"
IMAGE_FOLDER = os.path.join(settings.BASE_DIR, IMAGE_SUB_FOLDER)

SKYLARK_IMAGE_FOLDER = os.path.join(settings.BASE_DIR, "static", "images", "skylark")


def get_files(dir_path):
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]


def resize_image(image_file, output_file, to_width, to_height):
    try:
        im = Image.open(image_file)
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
        print("Resized %s" % image_file)
    except IOError as ex:
        print(ex)
        print("Cannot create thumbnail for '%s'" % image_file)


def update_swan_home():
    image_pattern = r"!\[.*\]\(.*/%s/.*jpg\)" % IMAGE_SUB_FOLDER
    markdown_files = get_files(SWAN_FOLDER)
    for markdown_file in markdown_files:
        thumbnail_name = markdown_file.replace(".md", ".jpg")
        thumbnail_file = os.path.join(THUMBNAIL_FOLDER, thumbnail_name)
        image_file = None
        with open(os.path.join(SWAN_FOLDER, markdown_file), 'r') as f:
            # Find the first image
            for line in f:
                if re.match(image_pattern, line):
                    image_file = line[line.find(IMAGE_SUB_FOLDER):]\
                        .replace(IMAGE_SUB_FOLDER, IMAGE_FOLDER)\
                        .split(")")[0]
                    break
        if image_file:
            resize_image(image_file, thumbnail_file, 400, 300)


def update_skylark(folder):
    for collection in [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]:
        if collection == "home":
            continue
        collection_folder = os.path.join(folder, collection)
        images = get_files(collection_folder)
        thumbnails_dir = os.path.join(collection_folder, "thumbnails")
        if not os.path.exists(thumbnails_dir):
            os.mkdir(thumbnails_dir)
        # Delete the existing thumbnails
        for f in get_files(thumbnails_dir):
            os.remove(os.path.join(thumbnails_dir, f))
        for image in images:
            image_path = os.path.join(collection_folder, image)
            thumb_path = os.path.join(collection_folder, "thumbnails", image)
            resize_image(image_path, thumb_path, 400, 300)


class Command(BaseCommand):
    help = 'Creates a thumbnail for the first image of each markdown file in the swan folder.'

    def handle(self, *args, **options):
        # update_swan_home()
        update_skylark(SKYLARK_IMAGE_FOLDER)
