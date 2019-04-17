import re
import json
from typing import List


class RegexParser:
    def get_html_from_file(self, file_path: str, encoding=None) -> str:
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
        if encoding is not None:
            return open(file_path, 'r', encoding=encoding).read()
        else:
            return open(file_path, 'r').read()

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

    def parse_overstock(self, html):
        """
        Parses all the necessary information from the HTML content provided and
        return a JSON object in a string.

        The information acquired from the HTML contains: Title, Content, Price, ListPrice, Saving, SavingPercent, Content

        Parameters
        ----------
        html:
            HTML content to parse information from.

        Returns
        -------
        str:
            JSON object with the information in the string format.
        """
        title_regex = r"<td><a href=\"http:\/\/www\.overstock\.com\/cgi-bin\/d2\.cgi\?PAGE=PROFRAME[\S\s]*?<b>(.*)<\/b>"
        list_price_regex = r"<b>List Price:[\S\s]*?<s>(.*)<\/s>"
        price_regex = r"<b>Price:[\S\s]*?<b>(.*)<\/b>"
        saving_regex = r"<span class=\"littleorange\">(.*)\s\("
        saving_percent_regex = r"<span class=\"littleorange\">[\S\s]*?\((.*)\)<\/span>"
        content_regex = r"<span class=\"normal\">([\S\s]*?)<br"

        # find list of lists, that include all matches for each regex
        regex_matches = self.find_all_matches(html=html,
                                              regex_list=[title_regex, list_price_regex, price_regex, saving_regex,
                                                          saving_percent_regex, content_regex])

        # bundle them into items
        items = list(zip(*regex_matches))

        # add labels to parsed elements (in the same order they were parsed by regexes into the regex_matches)
        items_processed = []
        for item in items:
            items_processed.append({
                "title": item[0],
                "list_price": item[1],
                "price": item[2],
                "saving": item[3],
                "saving_percent": item[4],
                "content": item[5],
            })

        parsed_content = {
            "items": items_processed
        }

        return json.dumps(parsed_content)

    def parse_avtonet(self, html):
        """
        Parses all the necessary information from the HTML content provided and
        return a JSON object in a string.

        The information acquired from the HTML contains: Name, FirstRegistration, Kilometers, FuelType, Displacement,
                                                         Power, Transmission, Price

        Parameters
        ----------
        html:
           HTML content to parse information from.

        Returns
        -------
        str:
           JSON object with the information in the string format.
        """
        name_regex = r"<a class=\"Adlink\"[\S\s]*?<span>(.*)<\/span>"
        first_registration_regex = r"<ul>[\s\n\r]*<li>Letnik 1.registracije:(.*)<\/li>"
        kilometers_regex = r"<\/li>[\s\t\n]*<li>([0-9]*) km<\/li>"
        fuel_type_regex = r"<\/li>[\s\t\n]*<li>[0-9]* km<\/li><li>(diesel|bencin)"
        displacement_regex = r"<\/li>[\s\t\n]*<li>[0-9]* km<\/li>[\S\s]*?([0-9]*) ccm"
        power_regex = r"<\/li>[\s\t\n]*<li>[0-9]* km<\/li>[\S\s]*?([0-9]*)\skW"
        transmission_regex = r"<\/li>[\s\t\n]*<li>[0-9]* km<\/li>[\S\s]*?(ročni|avtomatski)\smenjalnik"
        price_regex = r"<div class=\"ResultsAdPriceLogo\"[\S\s]*?([^\t\n>]*?€|Pokličite za ceno!)"

        # find list of lists, that include all matches for each regex
        regex_matches = self.find_all_matches(html=html,
                                              regex_list=[name_regex, first_registration_regex, kilometers_regex,
                                                          fuel_type_regex, displacement_regex, power_regex,
                                                          transmission_regex, price_regex])

        # bundle them into items
        items = list(zip(*regex_matches))

        items_processed = []
        for item in items:
            items_processed.append({
                "name": item[0],
                "first_registration": item[1],
                "kilometers": item[2],
                "fuel_type": "petrol" if item[3] == "bencin" else "diesel",
                "displacement_ccm": item[4],
                "power_kw": item[5],
                "transmission": "automatic" if item[6] == "avtomatski" else "manual",
                "price": None if item[7] == "Pokličite za ceno!" else item[7]
            })

        parsed_content = {
            "items": items_processed
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

    def find_all_matches(self, html: str, regex_list: List[str]) -> List[List]:
        """
        Finds all occurences of regex matches and returns them, bundled as a list of lists of strings.

        Parameters
        ----------
        html:
            HTML source to search for occurences in.
        regex_list:
            List of regular expressions that will be compiled and evaluated on the input HTML.

        Returns
        -------
        List[List]:
            List of lists of regex matches as strings.
        """
        matches = []
        for regex in regex_list:
            compiled = re.findall(regex, html)
            matches.append(compiled)
        return matches


if __name__ == '__main__':
    rp = RegexParser()

    # pageContent = rp.get_html_from_file(
    #     '../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html', encoding="utf-8")
    # print(rp.parse_rtvslo(pageContent))

    # pageContent = rp.get_html_from_file('../input/overstock.com/jewelry01.html')
    # print(rp.parse_overstock(pageContent))

    pageContent = rp.get_html_from_file('../input/avtonet/benz.htm')
    print(rp.parse_avtonet(pageContent))
