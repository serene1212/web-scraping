import json

from bs4 import BeautifulSoup

from scrawl import scrawl_instance


class Scrape:
    def __init__(self):
        self.soup = {}  # {"urls": "soup object"}
        self.htm_content = scrawl_instance.html_content
        self.parse_html_content()

    def parse_html_content(self):
        for url, content_list in self.htm_content.items():
            self.soup[url] = [BeautifulSoup(content, "html.parser") for content in content_list]

    def extract_titles(self):
        titles = {}
        for url, soup_list in self.soup.items():
            titles[url] = [soup.title.string if soup.title else "No title" for soup in soup_list]
        return titles

    def extract_links(self):
        links = {}
        for url, soup_list in self.soup.items():
            links[url] = [a["href"] for soup in soup_list for a in soup.find_all("a", href=True)]
        return links

    @staticmethod
    def save_json_extracted(data, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def save_all_html_content(self):
        for url, content_list in self.htm_content.items():
            for i, content in enumerate(content_list):
                filename = f"data/{url.replace('https://', '').replace('/', '_')}_{i}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)


scrape_instance = Scrape()
