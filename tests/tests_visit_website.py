import os
from io import StringIO
from collections import deque
from lxml import etree
from django.test import SimpleTestCase


class VisitWebsiteTestCase(SimpleTestCase):
    """Includes tests for visiting the website and following the links.
    """
    def visit(self, url):
        """Gets the response of visiting a URL.
        This method will follow the redirects (for at most 10 times) 
            and return the final response.
        
        Args:
            url (str): The URL as a string.
        
        Returns:
            Response: The final response.
            This response object includes an additional attribute "url",
                which is the URL returning the final response (after redirect).
            See also：
            https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.Response
        """
        response = self.client.get(url)
        counter = 0
        # Follow redirects
        while 300 <= response.status_code <= 308:
            url = response.get("location")
            response = self.client.get(url)
            counter += 1
            # Break if there are too many redirects.
            if counter > 10:
                self.assertLess(counter, 10, "Too many redirects... Last URL: %s" % url)
                break
        response.url = url
        return response

    def find_links(self, response_content):
        """Finds all the links from the "href" attributes of <a> tags in an HTML response content.
        
        Args:
            response_content (bytes): The content (containing HTML) of the response.
        
        Returns:
            list: a list of URLs, which are the "href" attributes of the <a> tags.
            The URLs may be absolute or relative paths.
        """
        tree = etree.parse(StringIO(response_content.decode('utf-8')), etree.HTMLParser())
        root = tree.getroot()
        links = [element.get("href") for element in root.findall(".//a")]
        return links

    def test_visit_all_links(self):
        """Tests visiting all links on a website by sending get requests.
        This test will fail if the final response code (after any redirects) 
            of a get request is not 200.
        Links are visited based on depth first search.
        
        Absolute paths starting with "http" are skipped, as these are usually external links.
        Django test client does not seem to be able to visit external links (it will return 404).
        
        Links to static files (starts with "/static/") are skipped.
        Django test client does not seem to be able to get static files correctly.
        """
        queue = deque()
        queue.append("/")
        visited_links = {}
        while len(queue) > 0:
            url = queue.pop()
            response = self.visit(url)
            visited_links[url] = True
            self.assertEqual(
                response.status_code, 
                200,
                "URL: %s, Response Code: %d" % (url, response.status_code) 
            )
            links = self.find_links(response.content)
            for link in links:
                if link.startswith("http"):
                    continue
                if visited_links.get(link):
                    continue
                if not link.startswith("/"):
                    link = os.path.abspath(os.path.join(response.url, link))
                if link.startswith("/static/"):
                    continue
                queue.append(link)
        sitemap_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sitemap.txt")
        with open(sitemap_file, 'w') as f:
            for url in visited_links.keys():
                f.write("https://qqin.page%s\n" % url)
