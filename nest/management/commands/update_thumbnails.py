import os
import json
from operator import itemgetter
from django.conf import settings
from django.core.management.base import BaseCommand
from nest.lib import resize_image, get_files



SKYLARK_IMAGE_FOLDER = os.path.join(settings.BASE_DIR, "static", "images", "skylark")


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
