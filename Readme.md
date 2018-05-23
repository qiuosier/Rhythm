# Rhythm - The Bird Nest Project
Qiu's personal website, designed for Google App Engine standard environment.
This project uses Python 2 and Django 1.9.

## Folders and Files
Brief descriptions of the folders and files:
* "app.yaml": App Engine app's settings. For more details, see https://cloud.google.com/appengine/docs/standard/python/config/appref
* "appengine_config.py": App Engine python module configuration. For more details, see https://cloud.google.com/appengine/docs/standard/python/tools/appengineconfig
* "requirement.txt": Lists python package dependencies.
* "static": Stores static files for the website.
* "data": Stores data files, including json and markdown files.
* "rhythm": Stores Django project settings.
* "nest": This is the main Django App for the website
* "log_http_request": A Django App providing logging middleware.

## Design Pattern
This is a Python Django project, so it follows most of the Django project patterns. In addition, this project has some additional design patterns.

### Data Format
Other than the logging middleware, this project does not use external database. The data for rendering web pages are stored in the "data" folder with as "JSON" or "Markdown" format. In addition, HTML templates for rendering the data are stored in the "nest/templates/nest" folder.

### Rendering Webpage with Data
The `nest/view.py` module contains two basic view functions for rendering the "JSON" and "Markdown" data, respectively. 
* The `load_data_and_render` function loads a JSON file from the data folder and render an HTML template in the tempalte folder (most likely with the same filename, e.g. hello.json and hello.html).
* The `page` function loads a markdown file and render it with the `page.html` template. The URL pattern for displaying a "page" is `www.example.com/nest/page/<file_path>/`, in which `<file_path>` is the file path of a markdown file stored in `/data/markdown/`. Since both the URL and the file path are two level down from the root, relative paths in the markdown file will be able to point to the same location when the file is being viewed by a local editor or rendered by the web application. The images used in the markdown files are stored in `/static/images/`.

## Updating Pages with Management Commands
### Update Swift
The Swift home page displays blog entries. It loads data from `/data/swift.json`, which should be updated as new blogs are added. The `update_swift` management command is designed to update the `/data/swift.json`. The command loads the blogs, generate summaries and updates the entries to be displayed on the Swift home page.

### Update Swan
