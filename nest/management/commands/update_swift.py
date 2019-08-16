"""
This command updates the Swift blog home page to contain the latest blogs in "data/swift" folder.
"""
import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from Aries.storage import LocalFolder
from nest.lib import summarize_markdown

# The folder storing the Markdown blog files.
# The filename should have the format of 20160101_ArticleName.md, i.e. a date and a name separated by '_'
MARKDOWN_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown")
BLOG_FOLDERS = [
    os.path.join(MARKDOWN_FOLDER, "swift"),
    os.path.join(MARKDOWN_FOLDER, "swan")
]

# The JSON file storing the Swift home page entries
JSON_OUTPUT_NEW = os.path.join(settings.BASE_DIR, "data", "swift.json")
JSON_OUTPUT_OLD = os.path.join(settings.BASE_DIR, "data", "swift_more.json")

# The size array for the blog entries showing on the home page.
# Each number indicates the width of the blog entry on the page.
# This number is the same number as the ones used in the bootstrap column width (e.g., col-md-8).
# The page has a full width of 12
SIZE_ARRAY = [8, 4, 4, 4, 4, 6, 6, 4, 4, 4, 6, 6]

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Load all file names.
        files = []
        for folder in BLOG_FOLDERS:
            files.extend([os.path.join(folder, f) for f in LocalFolder(folder).file_names])
        entries = []
        for filename in files:
            entry = summarize_markdown(filename, MARKDOWN_FOLDER)
            entry["class"] = "col-md-3"
            entries.append(entry)
        # Sort by date
        # TODO: key?
        entries = sorted(entries, key=lambda k: k["link"].rsplit("/", 1)[-1], reverse=True)
        # Take only the first 12 entries
        # TODO: show 12+ entries?
        if len(entries) > 12:
            new_entries = entries[:12]
            old_entries = entries[12:]
        else:
            new_entries = entries
            old_entries = []
        # Set entry width
        i = 0
        for entry in new_entries:
            entry["class"] = "col-md-" + str(SIZE_ARRAY[i])
            i += 1
            print("%s %s" % (i, entry["title"]))
        # Save the data
        with open(JSON_OUTPUT_NEW, 'w') as output:
            json.dump({
                "title": "The Swift Blog",
                "blogs": new_entries,
                "has_more": True if old_entries else False
            }, output, indent=4)
        with open(JSON_OUTPUT_OLD, 'w') as output:
            json.dump({
                "title": "The Swift Blog - More",
                "blogs": old_entries
            }, output, indent=4)
