# Rhythm - The Bird Nest Project
This is Qiu's personal website, designed for Google App Engine standard environment.
This project uses Python 3.7 and Django 2.1.

## Folders and Files
Brief descriptions of the folders and files:
* "app.yaml": App Engine app's settings. For more details, see https://cloud.google.com/appengine/docs/standard/python/config/appref
* "appengine_config.py": App Engine python module configuration. For more details, see https://cloud.google.com/appengine/docs/standard/python/tools/appengineconfig
* "requirement.txt": Lists python package dependencies.
* "static": Stores static files for the website, including the images.
* "data": Stores content data files, including json and markdown files.
* "rhythm": Stores Django project settings.
* "nest": This is the main Django App for the website.

## Design Pattern
This is a Python Django project, so it follows most of the Django project patterns. In addition, this project has some additional design patterns.

### Content Data
The logging middleware uses [Google Datastore NDB](https://cloud.google.com/appengine/docs/standard/python/ndb/) to store the logs.

Other than the logging middleware, this project does not use external database. The data for rendering web pages are stored in the "data" folder as "JSON" or "Markdown" format. HTML templates for rendering the data are stored in the "nest/templates/nest" folder. The `nest/view.py` module contains two basic view functions for rendering the "JSON" and "Markdown" data, respectively. These two functions handles the rendering of most webpages.

The "data" folder and the "images" folder in the "static" folder contain only content data (user data). These folders are included in the Git repostory intentionally to keep track of the history of content updates.

### Rendering Webpage with HTML Template and Structured JSON Data
Structured data for the website are stored in "JSON" format. The basic webpage rendering pattern for most web frameworks is displaying templates with structured data. The data workflow can be summarized as 3 steps:
1. Loading data
2. Transforming/Manipulating data
3. Rendering data with a template

The `render_template` function in `nest/views.py` serves as an entry point of the above workflow. Search directories are defined in the function for looking up the JSON and HTML files. The data transformation step is optional. It uses functions defined in the `transform.py`.

### Rendering Webpage with Markdown Data
Un-structured data, like blogs or articles are stored in "Markdown" format.

The `page` function in `nest/views.py` is designed to render "Markdown" data in a webpage. It loads a markdown file and render it with the `page.html` template.

The `page.html` template also includes a function to render additional components with AJAX requests, if HTML tags in are defined in the "Markdown" with class "ajax-page-component", e.g.:
```
<div class="ajax-page-component" data-context="[JSON_NAME]" data-template="[HTML_NAME]">
</div>
```
AJAX GET requests will be sent to render additiona components using the `render_template` function. The returned data will be used to replace the whole HTML tag (`<div></div>` in the above example). The `[JSON_NAME]` and `[HTML_NAME]` are the inputs for the `render_template` function.

The URL pattern for displaying a "page" is `www.example.com/page/<file_path>/`, in which `<file_path>` is the file path of a markdown file stored in `/data/markdown/`, including the filename but without the ".md" extension. Since both the URL and the file path are two level down from the root, relative paths in the markdown file will be able to point to the same location when the file is being viewed by a local editor or rendered by the web application. The images used in the markdown files are stored in `/static/images/`.

## Updating Pages with Management Commands
Some pages, like the index page of the "Swift Blog" displays "JSON" data summarized from "Markdown" files. A few management commands are designed to update such "JSON" data automatically.

### Update Blogs Index - Swift
The Swift home page displays blog entries. It loads data from `/data/swift.json`, which should be updated as new blogs are added. The `update_swift` management command is designed to update the `/data/swift.json`. The command loads the blogs, generate summaries and updates the entries to be displayed on the Swift home page.

### Update Footprint Index - Swan
The Swan home page displays my travel entries.
