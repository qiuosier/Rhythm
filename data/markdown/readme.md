# Markdown Files
This folder contains files in "[Markdown](daringfireball.net/projects/markdown "The Markdown Project Homepage")" format. These files in this folder are used as the sources of some pages on this website. The Markdown format provides a simple way to write and format lightweight text documents.

## Displaying Markdown Files
The URL pattern for displaying a file in this folder is `/markdown/<file_name>/`, where `<file_name>` is the filename without extension (.md). When user visits the URL, the Django view function (`nest.page`) loads a file in this folder, convert it to HTML, and render it with the `nest/templates/nest/page.html` template.

## Location of this folder
The location of this folder affects the image rendering in the Markdown files. 

Images in the Markdown files are specified in relative path. The images are stored in `/static/markdown` folder. This folder is two levels down from the root of the website, therefore each image path will have a prefix of `../../`. Note that the URL pattern is also two level down from the site root (including the tailing slash). With this location and the URL pattern, the images should be rendered correctly when the file being edited using a local editor and when it is being displayed on the website.