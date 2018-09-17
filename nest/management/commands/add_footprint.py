import os
import json
from operator import itemgetter
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a markdown file base on the images in a folder'

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str, nargs=1,
                            help='Folder name in "static/images/swan/" '
                                 'containing the images to be included in the markdown.')

        parser.add_argument("filename", type=str, nargs=1,
                            help='Filename of the markdown, including ".md".')

    def handle(self, *args, **options):
        folder = options["folder"][0]
        filename = options["filename"][0]
        image_dir = os.path.join(settings.BASE_DIR, "static", "images", "swan", folder)
        markdown_file = os.path.join(settings.BASE_DIR, "data", "markdown", "swan", filename)
        images = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
        images.sort()
        with open(markdown_file, 'w') as f:
            f.write("#\n\n")
            f.write("_June 8th, 2018_\n\n")
            for image in images:
                f.write("![](../../../static/images/swan/%s/%s)\n\n" % (folder, image))
