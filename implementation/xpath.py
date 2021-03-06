from lxml import html as lxml_html
from implementation.utils import get_html_from_file
import json


def parse_rtvslo(html):
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
    author_query = "//*[@class=\"author-name\"]/text()"
    published_time_query = "//*[@class=\"publish-meta\"]/text()[1]"
    title_query = "//*[@class=\"article-header\"]/h1/text()"
    subtitle_query = "//*[@class=\"subtitle\"]/text()"
    lead_query = "//*[@class=\"lead\"]/text()"
    content_query = "//*[@class=\"Body\"]/text()"

    query_matches = find_first_matches(html=html,
                                       query_list=[author_query, published_time_query, title_query,
                                                   subtitle_query, lead_query])

    # Find all <p class="Body">...</p> elements and get their texts
    # Take the first element from the matches, as we get a list of lists back for all queries in the query_list.
    content_matches = find_all_matches(html=html, query_list=[content_query])[0]

    # Join all string matches into a single string.
    content = " ".join(content_matches)

    parsed_content = {
        "author": query_matches[0],
        "published_time": query_matches[1].strip(),
        "title": query_matches[2],
        "subtitle": query_matches[3],
        "lead": query_matches[4],
        "content": content
    }

    return json.dumps(parsed_content, ensure_ascii=False)


def parse_overstock(html):
    """
    Parses all the necessary information from the HTML content provided and
    return a JSON object in a string.

    The information acquired from the HTML contains:  Title, Content, Price, 
    ListPrice, Saving, SavingPercent, Content

    Parameters
    ----------
    html:
        HTML content to parse information from.

    Returns
    -------
    str:
        JSON object with the information in the string format.
    """
    # Base location for each item
    item_base_location = """/html/body/table/tbody/tr/td[5]
                    /table/tbody/tr/td
                    /table/tbody/tr/td
                    /table/tbody/tr/td"""

    title_query = item_base_location + "/a/b/text()"
    list_price_query = item_base_location + """/table/tbody/tr/td
                    /table/tbody/tr/td/s/text()"""
    price_query = item_base_location + """/table/tbody/tr/td
                    /table/tbody/tr/td/span/b/text()"""
    saving_fixed_and_percent_query = item_base_location + """/table/tbody/tr/td
                    /table/tbody/tr/td/span/text()"""
    content_query = item_base_location + "/table/tbody/tr/td/span/text()"

    #  Find all matches for the items
    query_matches = find_all_matches(html=html,
                                     query_list=[title_query, list_price_query, price_query,
                                                 saving_fixed_and_percent_query, content_query])

    items = list(zip(*query_matches))
    #  Place all products in a list
    items_processed = []
    for item in items:
        items_processed.append({
            "title": item[0],
            "list_price": item[1],
            "price": item[2],
            "saving": item[3].split(" ")[0],
            "saving_percent:": (item[3].split(" ")[1]).replace('(', '').replace(')', ''),
            "content": item[4]
            })

    parsed_content = {
        "items": items_processed
    }

    return json.dumps(parsed_content, ensure_ascii=False)


def parse_avtonet(html):
    """
    Parses all the necessary information from the HTML content provided and
    return a JSON object in a string.

    The information acquired from the HTML contains:  Name, First Registration,
    Kilometers, Fuel Type, Displacement, Power, Transmission, Price

    Parameters
    ----------
    html:
        HTML content to parse information from.

    Returns
    -------
    str:
        JSON object with the information in the string format.
    """
    data_base_query = "//*[@class=\"ResultsAdDataTop\"]"

    name_query = data_base_query + "/a/span/text()"
    first_registration_query = data_base_query + "/ul/li[1]/text()"
    kilometers_query = data_base_query + "/ul/li[2]/text()"
    fuel_type_displacement_power_query = data_base_query + "/ul/li[3]/text()"
    transmission_query = data_base_query + "/ul/li[4]/text()"
    # this is hacked together, but wcyd (normalizing spaces did not help)
    price_query = "//div[@class='ResultsAdPrice']/text()[contains(., '\n\t\t\t\t\t\t')]|" \
                  "//div[@class='ResultsAdPrice ResultsAdPriceAkcija']/p[@class='AkcijaCena']/text()"

    #  Find all matches for the items
    query_matches = find_all_matches(html=html,
                                     query_list=[name_query, first_registration_query,
                                                 kilometers_query, fuel_type_displacement_power_query,
                                                 transmission_query, price_query])

    items = list(zip(*query_matches))
    #  Place all products in a list
    items_processed = []
    for item in items:
        try:
            kilometers = item[2]
            fuel_type = item[3].split(',')[0]
            displacement = item[3].split(',')[1]
            power = item[3].split(',')[2]
            transmission = item[4]
            # \x80 is Latin encoding for '€'
            price = item[5].replace('\x80', '€').strip()
        except IndexError:
            # Sometimes there are no kilometers of a car displayed
            kilometers = 0
            fuel_type = item[2].split(',')[0]
            displacement = item[2].split(',')[1]
            power = item[2].split(',')[2]
            transmission = item[3]
            price = item[4].replace('\x80', '€').strip()

        items_processed.append({
            "title": item[0],
            "first_registration": item[1][-4:],  # Last 4 characters represent year
            "kilometers": kilometers,
            "fuel_type": "petrol" if fuel_type == "bencin" else "diesel",
            "displacement": displacement,
            "power": power,
            "transmission": "automatic" if transmission == "avtomatski" else "manual",
            "price": None if price == "Pokličite za ceno!" else price
            })

    parsed_content = {
        "items": items_processed
    }

    return json.dumps(parsed_content, ensure_ascii=False)


def find_first_matches(html, query_list):
    """
    Finds first occurences of xPath results and returns them, bundled as a list of strings.

    Parameters
    ----------
    html:
        HTML source to search for occurences in.
    query_list:
        List of xPath queries that will be evaluated on the input HTML.

    Returns
    -------
    List[str]:
        List of elements in the HTML tree found by the xPath queries as strings.
    """
    tree = lxml_html.fromstring(html)
    matches = []
    for query in query_list:
        matches.append(str(tree.xpath(query)[0]))
    return matches


def find_all_matches(html, query_list):
    """
    Finds all occurences of xPath results and returns them, bundled as a list of lists of strings.

    Parameters
    ----------
    html:
        HTML source to search for occurences in.
    query_list:
        List of xPath queries that will be evaluated on the input HTML.

    Returns
    -------
    List[List]:
        List of elements in the HTML tree found by the xPath queries as strings.
    """
    tree = lxml_html.fromstring(html)
    matches = []
    for query in query_list:
        curr_query_matches = []
        for match in tree.xpath(query):
            curr_query_matches.append(str(match))
        matches.append(curr_query_matches)
    return matches


if __name__ == '__main__':
    pageContent = get_html_from_file(
        '../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html',
        encoding='iso 8859-1') 
    print(parse_rtvslo(pageContent))

    pageContent = get_html_from_file(
        '../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html',
        encoding='iso 8859-1')
    print(parse_rtvslo(pageContent))

    pageContent = get_html_from_file('../input/overstock.com/jewelry01.html', encoding='iso 8859-1')
    print(parse_overstock(pageContent))

    pageContent = get_html_from_file('../input/overstock.com/jewelry02.html', encoding='iso 8859-1')
    print(parse_overstock(pageContent))

    pageContent = get_html_from_file('../input/avtonet/benz.htm', encoding='iso 8859-1')
    print(parse_avtonet(pageContent))

    pageContent = get_html_from_file('../input/avtonet/bmw.htm', encoding='iso 8859-1')
    print(parse_avtonet(pageContent))

    # f = open("../output/xPath/avtonet2.json","w+")
    # f.write(parse_avtonet(pageContent))
    # f.close() 
