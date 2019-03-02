"""
This command updates the Swift blog home page to contain the latest blogs in "data/swift" folder.
"""
import os
import json
import re
from operator import itemgetter
from django.conf import settings
from django.core.management.base import BaseCommand
from nest.lib import parse_markdown, resize_image, get_files

# The folder storing the Markdown files.
# The filename should have the format of 20160101_ArticleName.md, i.e. a date and a name separated by '_'
MARKDOWN_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown")
BLOG_FOLDERS = [
    os.path.join(MARKDOWN_FOLDER, "swan")
]
SWAN_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown", "swan")

# The JSON file storing the Swift home page entries
JSON_OUTPUT = os.path.join(settings.BASE_DIR, "data", "swan.json")

IMAGE_SUB_FOLDER = "static/images"
IMAGE_FOLDER = os.path.join(settings.BASE_DIR, IMAGE_SUB_FOLDER)
THUMBNAIL_FOLDER = os.path.join(settings.BASE_DIR, "static", "images", "swan", "home")


def update_swan_thumbnails():
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


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Load all file names.
        files = []
        for folder in BLOG_FOLDERS:
            files.extend([
                os.path.join(folder, f)
                for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))
            ])
        entries = []
        for filename in files:
            entry_dict = parse_markdown(filename, base_dir=MARKDOWN_FOLDER)
            entries.append(entry_dict)
            
        # Sort by date
        entries = sorted(entries, key=itemgetter('key'), reverse=True)

        # Load existing data from swan
        featured = []
        destinations = []
        if os.path.exists(JSON_OUTPUT):
            with open(JSON_OUTPUT, 'r') as f:
                swan_data = json.load(f)
                featured = swan_data.get("featured", [])
                destinations = swan_data.get("destinations", [])

        # Process images for journeys
        update_swan_thumbnails()
        journeys = []
        existing_entries = [entry["name"] for entry in featured + destinations if entry.get("name")]
        for entry in entries[1:]:
            # Skip if entry is in featured or destinations
            if entry["name"] in existing_entries:
                continue
            thumbnail = os.path.join(THUMBNAIL_FOLDER, entry["name"].replace("swan/", "") + ".jpg")
            if os.path.exists(thumbnail):
                entry["image"] = thumbnail.replace(settings.BASE_DIR, "")
            journeys.append(entry)

        # Process last trip image
        if entries[0]["image"]:
            image_file = settings.BASE_DIR + entries[0]["image"]
            thumbnail = os.path.join(THUMBNAIL_FOLDER, entries[0]["name"].replace("swan/", "") + "_L.jpg")
            resize_image(image_file, thumbnail, 1000, 500)
            entries[0]["image"] = thumbnail.replace(settings.BASE_DIR, "")

        # Save the data
        with open(JSON_OUTPUT, 'w') as output:
            json.dump({
                "title": "Swan",
                "last_trip": entries[0],
                "journeys": journeys,
                "featured": featured,
                "destinations": destinations
            }, output)
