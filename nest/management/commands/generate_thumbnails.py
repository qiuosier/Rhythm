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


class Command(BaseCommand):
    help = 'Creates a thumbnail for the first image of each markdown file in the swan folder.'

    def handle(self, *args, **options):
        image_pattern = r"!\[.*\]\(.*/%s/.*jpg\)" % IMAGE_SUB_FOLDER
        markdown_files = [f for f in os.listdir(SWAN_FOLDER) if os.path.isfile(os.path.join(SWAN_FOLDER, f))]
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
