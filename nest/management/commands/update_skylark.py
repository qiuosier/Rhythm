"""
This command updates the Skylark Gallery, including:
    Generating thumbnails for the images in each collection.

Images in the Skylark Gallery are stored in collections, each collection is folder.
All collections are stored in the "Skylark Image Folder".
i.e. the images will have a path like ".../skylark/collection/image.jpg".

"""
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from nest.lib import resize_image, AFolder

# The folder storing the skylark images
SKYLARK_IMAGE_FOLDER = os.path.join(settings.BASE_DIR, "static", "images", "skylark")


def generate_thumbnails(folder):
    """Generate thumbnails for images inside each sub-folder of the root folder.
    The thumbnails are saved into a folder named "thumbnails" inside each sub-folder.

    Args:
        folder: The skylark root image folder (root folder) storing the collections.

    Returns: None

    """
    for collection in AFolder(folder).folders:
        # Skip the home folder
        if collection == "home":
            continue
        collection_folder = os.path.join(folder, collection)
        images = AFolder(collection_folder).files
        thumbnails_dir = os.path.join(collection_folder, "thumbnails")
        # Create the thumbnails folder in case it does not exist
        AFolder(thumbnails_dir).create()
        # Delete the existing thumbnails
        AFolder(thumbnails_dir).empty()
        # Generate thumbnail for each image
        for image in images:
            image_path = os.path.join(collection_folder, image)
            thumb_path = os.path.join(collection_folder, "thumbnails", image)
            resize_image(image_path, thumb_path, 400, 300)


class Command(BaseCommand):
    help = 'Updates the Skylark Gallery.'

    def handle(self, *args, **options):
        generate_thumbnails(SKYLARK_IMAGE_FOLDER)
