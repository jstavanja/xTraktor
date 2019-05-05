from implementation.utils import get_html_from_file
from bs4 import BeautifulSoup, NavigableString


class RoadRunner:
    def __init__(self, page_one_path, page_two_path):
        self.page_one = get_html_from_file(page_one_path)
        self.page_two = get_html_from_file(page_two_path)
        self.soup_one = BeautifulSoup(self.page_one, "lxml")
        self.soup_two = BeautifulSoup(self.page_two, "lxml")
        self.dom_walker(self.soup_one)

    def dom_walker(self, soup):
        if soup.name is not None:
            for child in soup.children:

                # ignore whitespaces, tabs and newlines between nodes that we dont need to match
                if isinstance(child, NavigableString) and (str(child) == '\n' or str(child) == '\t' or str(child) == ''):
                    continue

                print(str(child.name) + ":" + str(type(child)))
                self.dom_walker(child)
        else:
            # if it's not a tag, it's a string
            print(soup.strip())


if __name__ == "__main__":
    rr = RoadRunner('../input/test/one.html', '../input/test/two.html')
