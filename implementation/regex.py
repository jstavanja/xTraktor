import re
import json
from typing import List


class RegexParser:
    def get_html_from_file(self, file_path: str) -> str:
        """
        Gets raw HTML from a saved .html file.

        Parameters
        ----------
        file_path : string
            Path to the file containing the HTML.

        Returns
        -------
        str
            HTML content fetched from the file in a string.
        """
        return open(file_path, 'r', encoding='utf-8').read()

    def parse_rtvslo(self, html: str) -> str:
        """
        Parses all the necessary information from the HTML content provided and
        return a JSON object in a string.

        The information acquired from the HTML contains: Author, PublishedTime,
        Title, SubTitle, Lead and Content.

        Parameters
        ----------
        html:
            HTML content to parse information from.

        Returns
        -------
        str:
            JSON object with the information in the string format.
        """
        author_regex = r"<div class=\"author-name\">(.*)<\/div>"
        published_time_regex = r"<div class=\"publish-meta\">\n\s\t(.*?)<br>"
        title_regex = r"<header class=\"article-header\">[\S\s]*?<h1>(.*)<\/h1>"
        subtitle_regex = r"<header class=\"article-header\">[\S\s]*?<div class=\"subtitle\">(.*)<\/div>"
        lead_regex = r"<header class=\"article-header\">[\S\s]*?<p class=\"lead\">(.*)<\/p>"
        content_regex = r"<div class=\"article\-body\">([\S\s]*)<\/div>"

        regex_matches = self.find_first_matches(html=html, regex_list=[author_regex, published_time_regex, title_regex,
                                                                       subtitle_regex, lead_regex, content_regex])

        parsed_content = {
            "author": regex_matches[0],
            "published_time": regex_matches[1],
            "title": regex_matches[2],
            "subtitle": regex_matches[3],
            "lead": regex_matches[4],
            "content": regex_matches[5]
        }

        return json.dumps(parsed_content)

    def find_first_matches(self, html: str, regex_list: List[str]) -> List[str]:
        """
        Finds first occurences of regex matches and returns them, bundled as a list of strings.

        Parameters
        ----------
        html:
            HTML source to search for occurences in.
        regex_list:
            List of regular expressions that will be compiled and evaluated on the input HTML.

        Returns
        -------
        List[str]:
            List of regex matches as strings.
        """
        matches = []
        for regex in regex_list:
            compiled = re.compile(regex).search(html)
            matches.append(compiled.group(1))
        return matches


if __name__ == '__main__':
    rp = RegexParser()

    pageContent = rp.get_html_from_file(
        '../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html')

    print(rp.parse_rtvslo(pageContent))
