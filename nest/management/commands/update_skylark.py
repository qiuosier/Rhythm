"""
This command updates the Skylark Gallery, including:
    Generating thumbnails for the images in each collection.
    Create or update the index file for each collection.

Images in the Skylark Gallery are stored in collections, each collection is folder.
All collections are stored in the "Skylark Image Folder".
i.e. the images will have a path like ".../skylark/collection/image.jpg".

"""
import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from Aries.storage import StorageFolder
from Aries.files import File
from nest.lib import resize_image

# The folder storing the skylark images
SKYLARK_IMAGE_FOLDER = os.path.join(settings.BASE_DIR, "static", "images", "skylark")
SKYLARK_DATA_FOLDER = os.path.join(settings.BASE_DIR, "data", "skylark")
SKYLARK_INDEX = os.path.join(settings.BASE_DIR, "data", "skylark.json")

class Command(BaseCommand):
    help = 'Updates the Skylark Gallery.'

    def handle(self, *args, **options):
        folder = SKYLARK_IMAGE_FOLDER
        for collection in StorageFolder(folder).folder_names:
            # Skip the home folder
            if collection == "home":
                continue
            collection_folder = os.path.join(folder, collection)
            thumbnails_dir = os.path.join(collection_folder, "thumbnails")
            # Create the thumbnails folder in case it does not exist
            StorageFolder(thumbnails_dir).create()
            
            index_path = os.path.join(SKYLARK_DATA_FOLDER, "%s.json" % collection)
            index_dict = File.load_json(
                index_path, 
                {
                    "title": "%s Collection" % collection.title(),
                    "summary": "",
                    "link": collection,
                }
            )

            photo_entries = index_dict.get("photos", [])
            images = StorageFolder(collection_folder).file_names
            # Generate thumbnail for each image
            for image in images:
                image_path = os.path.join(collection_folder, image)
                thumb_path = os.path.join(collection_folder, "thumbnails", image)
                if not os.path.exists(thumb_path):
                    resize_image(image_path, thumb_path, 400, 300)
                entry_exist = False
                for entry in photo_entries:
                    if entry.get("image") == image:
                        entry_exist = True
                if not entry_exist:
                    photo_entries.append({
                        "title": "%s" % str(image).split(".")[0],
                        "summary": "",
                        "date": "",
                        "link": "",
                        "image": "%s" % image
                    })
            index_dict["photos"] = photo_entries
            with open(index_path, 'w') as f:
                json.dump(index_dict, f)
