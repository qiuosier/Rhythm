# Rhythm - Qiu's Bird Nest Project
[https://qiu-nest.appspot.com](https://qiu-nest.appspot.com)

This is Qiu's personal website, designed for Google App Engine standard environment.
This project uses Python 3.7 and Django 2.2.

[![Build Status](https://travis-ci.org/qiuosier/Rhythm.svg?branch=master)](https://travis-ci.org/qiuosier/Rhythm)
[![Coverage Status](https://coveralls.io/repos/github/qiuosier/Rhythm/badge.svg?branch=master)](https://coveralls.io/github/qiuosier/Rhythm?branch=master)

## Architecture
This website includes 4 components, each of them is named with a bird. That's why I called my website "Nest".
* The Swift Blog: My blogs and posts along with pictures.
* Swan's Footprint: My footprints around the world.
* The Skylark Gallery: More about my pictures.
* The Sparrow: My work and personal projects.

## Folders and Files
Brief descriptions of the folders and files:
* "app.yaml": App Engine app's settings. See also [app.yaml Reference](https://cloud.google.com/appengine/docs/standard/python3/config/appref).
* "build.json": Configuration file for Google Cloud Build and Google App Engine. See also [Build configuration overview](https://cloud.google.com/cloud-build/docs/build-config).
* "requirement.txt": Lists python package dependencies.
* "static": Stores static files for the website, including the images.
* "data": Stores content data files, including json and markdown files.
* "rhythm": Stores Django project settings.
* "nest": This is the main Django App for the website.

## Rendering Webpages
This website uses two major patterns for rendering webpages:
* Rendering HTML template with JSON data. This is generally used for index (home) or sub-index (summary) page.
* Rendering Markdown data as HTML page. This is generally used for blogs and posts.

The `nest/view.py` module contains two basic view functions for rendering the "JSON" and "Markdown" data, respectively. These two functions handles the rendering of most webpages.

### Content Data
The "data" folder and the "static/images" folder contain content data (user data). These folders are included in the Git repository intentionally to keep track of the history of content updates.

This project does not use external database for content data. The data for rendering web pages are stored in the "data" folder as "JSON" or "Markdown" format. HTML templates for rendering the data are stored in the "nest/templates/nest" folder. 

### JSON Data Model
Contents of the website are often displayed as "entries". For example, the "Carousel" of the home page is displaying a list of "entries". Similar "entries" are used in different pages. This website uses the following data model for most entries.
```
{
    "title": "",
    "summary": "",
    "description: "",
    "date": "",
    "link": "",
    "image": "",
    "class": "",
}
```

### Rendering HTML Template and Structured JSON Data
Structured data for the website are stored in "JSON" format. The basic webpage rendering pattern for most web frameworks is displaying templates with structured data. The data workflow can be summarized as 3 steps:
1. Loading data
2. Transforming/Manipulating data
3. Rendering data with a template

The `render_template` function in `nest/views.py` serves as an entry point of the above workflow. Search directories are defined in the function for looking up the JSON and HTML files. The data transformation step is optional. It uses functions defined in the `transform.py`.

### Rendering Webpage with Markdown Data
Un-structured data, like blogs or articles are stored in "Markdown" format.

The "Markdown" data files for some content data, e.g. blogs and footprints are named in with an eight-digit date prefix, e.g. `20140504_Toronto.md`. The eight-digit part will be used to sort the entries in the home/summary page.

The `page` function in `nest/views.py` is designed to render "Markdown" data in a webpage. It loads a markdown file and render it with the `page.html` template.

The `page.html` template also includes a function to render additional components with AJAX requests, if HTML tags in are defined in the "Markdown" with class "ajax-page-component", e.g.:
```
<div class="ajax-page-component" data-context="[JSON_NAME]" data-template="[HTML_NAME]">
</div>
```
AJAX GET requests will be sent to render additiona components using the `render_template` function. The returned data will be used to replace the whole HTML tag (`<div></div>` in the above example). The `[JSON_NAME]` and `[HTML_NAME]` are the inputs for the `render_template` function.

The URL pattern for displaying a "page" is `www.example.com/page/<file_path>/`, in which `<file_path>` is the file path of a markdown file stored in `/data/markdown/`, including the filename but without the ".md" extension. Since both the URL and the file path are two level down from the root, relative paths in the markdown file will be able to point to the same location when the file is being viewed by a local editor or rendered by the web application. The images used in the markdown files are stored in `/static/images/`.


## Deployment
The `build.json` file contains steps for deploying the website to Google App Engine using Google Cloud Build.
Some pages, like the index page of the "Swift Blog" displays "JSON" data summarized from "Markdown" files. A few management commands are designed to update such "JSON" data automatically.

### Google Cloud Platform
In order to use Google Cloud Build to deploy code to App Engine, the Cloud Build service account needs "App Engine Admin" role. The roles can be configured in the "IAM & Admin" page.

### Credentials
This website loads credentials from `rhythm/private.py`. This file is NOT included in the Git repository. The file is simply a python file with constants. It should look like:
```
DJANGO_SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```
The `build.json` includes a step to copy the `private.py` file from a private storage location.

### Updating Blog Index
The Swift home page displays blog entries. It loads data from `/data/swift.json`, which should be updated as new blogs are added. The `update_swift` management command is designed to update the `/data/swift.json`. The command loads the blogs, generate summaries and updates the entries to be displayed on the Swift home page.

### Updating Footprint Index
The Swan home page displays my travel entries. It loads data from `/data/swan.json`, which should be updated as new entries are added. The `update_swan` management command is designed to update the `/data/swan.json`. The command also generate thumbnails for each entry to be displayed on the Swan home page.

### Generating Thumbnails for Gallery
The `update_skylark` generates thumbnails for images. Each folder inside the `/static/images/skylark` folder is considered as a collection. This command creates a `thumbnails` folder inside the folder of each collection and saves the thumbnails of the images into it.
