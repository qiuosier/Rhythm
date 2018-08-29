import os
import json
from operator import itemgetter
from django.conf import settings
from django.core.management.base import BaseCommand

# The folder storing the Markdown blog files.
# The filename should have the format of 20160101_ArticleName.md, i.e. a date and a name separated by '_'
BLOGS_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown", "swift")

# The JSON file storing the Swift home page entries
JSON_OUTPUT = os.path.join(settings.BASE_DIR, "data", "swift.json")

# The size array for the blog entries showing on the home page.
# Each number indicates the width of the blog entry on the page.
# This number is the same number as the ones used in the bootstrap column width (e.g., col-md-8).
# The page has a full width of 12
SIZE_ARRRY = [8, 4, 4, 4, 4, 6, 6, 4, 4, 4, 6, 6]

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Load all file names.
        files = [os.path.join(BLOGS_FOLDER, f) for f in os.listdir(BLOGS_FOLDER) if os.path.isfile(os.path.join(BLOGS_FOLDER, f))]
        entries = []
        for filename in files:
            with open(filename, 'r') as f:
                lines = f.readlines()
                # Title of the blog
                title = None
                # Date of the blog
                date = None
                # The first image
                image = None
                # Introduction text
                intro = None
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
                        image = line.rsplit('/', 1)[1].strip(')')
                        continue
                    if not intro and line[0].isalpha():
                        if len(line) > 90:
                            intro = line[:line.find(' ', 90)]
                        else:
                            intro = line
                        intro = intro + '...'
                        continue
                entries.append({
                    "title": title,
                    "image": image,
                    "summary": intro,
                    "date": date,
                    "name": os.path.basename(filename).split('.')[0],
                    "key": os.path.basename(filename).split('_')[0],
                    "class": "col-md-6"
                })
        # Sort by date
        entries = sorted(entries, key=itemgetter('key'), reverse=True)
        # Take only the first 12 entries
        if len(entries) > 12:
            entries = entries[:12]
        # Set entry width
        i = 0
        for entry in entries:
            entry["class"] = "col-md-" + str(SIZE_ARRRY[i])
            i += 1
        # Save the data
        with open(JSON_OUTPUT, 'w') as output:
            json.dump({
                "title": "The Swift Blog",
                "blogs": entries
            }, output)
        
