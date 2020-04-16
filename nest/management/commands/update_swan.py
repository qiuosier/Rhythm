"""
This command updates the Swan page to contain the latest entries in "data/swan" folder.
"""
import os
import json
import re
from operator import itemgetter
from django.conf import settings
from django.core.management.base import BaseCommand
from Aries.storage import StorageFolder
from nest.lib import summarize_markdown, resize_image

# The folder storing the Markdown files.
# The filename should have the format of 20160101_ArticleName.md, i.e. a date and a name separated by '_'
MARKDOWN_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown")
SWAN_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown", "swan")

JOURNEYS_JSON = os.path.join(settings.BASE_DIR, "data", "swan", "journeys.json")

# The JSON file storing the Swift home page entries
JSON_OUTPUT = os.path.join(settings.BASE_DIR, "data", "swan.json")

IMAGE_SUB_FOLDER = "static/images"
IMAGE_FOLDER = os.path.join(settings.BASE_DIR, IMAGE_SUB_FOLDER)
THUMBNAIL_FOLDER = os.path.join(settings.BASE_DIR, "static", "images", "swan", "home")


def add_journeys():
    if not os.path.exists(JOURNEYS_JSON):
        return

    with open(JOURNEYS_JSON, 'r') as f:
        journeys = json.load(f).get("journeys")

    for journey in journeys:
        filename = "%s.md" % journey.get("name")
        markdown_file = os.path.join(SWAN_FOLDER, filename)
        if not os.path.exists(markdown_file):
            image = journey.get("image")
            with open(markdown_file, 'w') as f:
                f.write("# %s\n\n" % journey.get("title"))
                f.write("_%s_\n\n" % journey.get("date"))
                f.write("![](../../../static/images/swan/journeys/%s)\n\n" % image)
                f.write("%s\n" % journey.get("summary", ""))
            print("Created %s." % markdown_file)


def update_swan_thumbnails():
    """Generates thumbnails using the first image appear in each Markdown file.

    """
    image_pattern = r"!\[.*\]\(.*/%s/.*jpg\)" % IMAGE_SUB_FOLDER
    markdown_files = StorageFolder(SWAN_FOLDER).file_names
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

        add_journeys()

        # Load all swan markdown entries.
        files = StorageFolder(SWAN_FOLDER).file_names
        entries = []
        for filename in files:
            entry_dict = summarize_markdown(os.path.join(SWAN_FOLDER, filename), base_dir=MARKDOWN_FOLDER)
            entries.append(entry_dict)

        # Load existing data from swan
        featured = []
        destinations = []
        if os.path.exists(JSON_OUTPUT):
            with open(JSON_OUTPUT, 'r') as f:
                swan_data = json.load(f)
                featured = swan_data.get("featured", [])
                destinations = swan_data.get("destinations", [])

        update_swan_thumbnails()

        # Get journeys
        journeys = []
        existing_entries = [entry["link"] for entry in featured + destinations if entry.get("link")]
        for entry in entries:
            # Skip if entry is in featured or destinations
            if entry["link"] not in existing_entries:
                journeys.append(entry)

        # Sort by date
        journeys = sorted(journeys, key=lambda k: k["link"].rsplit("/", 1)[-1], reverse=True)

        # Process last trip image thumbnail
        if journeys[0]["image"]:
            image_file = settings.BASE_DIR + journeys[0]["image"]
            thumbnail = os.path.join(THUMBNAIL_FOLDER, journeys[0]["link"].replace("swan/", "") + "_L.jpg")
            resize_image(image_file, thumbnail, 1000, 500)
            journeys[0]["image"] = thumbnail.replace(settings.BASE_DIR, "")

        # Set other journeys thumbnail
        for entry in journeys[1:]:
            thumbnail = os.path.join(THUMBNAIL_FOLDER, entry["link"].replace("swan/", "") + ".jpg")
            if os.path.exists(thumbnail):
                entry["image"] = thumbnail.replace(settings.BASE_DIR, "")

        # Save the data
        with open(JSON_OUTPUT, 'w') as output:
            json.dump({
                "title": "Swan",
                "journeys": journeys,
                "featured": featured,
                "destinations": destinations
            }, output)
