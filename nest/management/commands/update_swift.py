import os
import json
from operator import itemgetter
from django.conf import settings
from django.core.management.base import BaseCommand


BLOGS_FOLDER = os.path.join(settings.BASE_DIR, "data", "markdown", "swift")

JSON_OUTPUT = os.path.join(settings.BASE_DIR, "data", "swift.json")

SIZE_ARRRY = [8, 4, 4, 4, 4, 6, 6, 4, 4, 4, 6, 6]

class Command(BaseCommand):
    def handle(self, *args, **options):
        files = [os.path.join(BLOGS_FOLDER, f) for f in os.listdir(BLOGS_FOLDER) if os.path.isfile(os.path.join(BLOGS_FOLDER, f))]
        entries = []
        for filename in files:
            with open(filename, 'r') as f:
                lines = f.readlines()
                title = None
                date = None
                image = None
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
        entries = sorted(entries, key=itemgetter('key'), reverse=True)
        if len(entries) > 12:
            entries = entries[:12]
        
        i = 0
        for entry in entries:
            entry["class"] = "col-md-" + str(SIZE_ARRRY[i])
            i += 1

        with open(JSON_OUTPUT, 'w') as output:
            json.dump({
                "title": "The Swift Blog",
                "blogs": entries
            }, output)
        
