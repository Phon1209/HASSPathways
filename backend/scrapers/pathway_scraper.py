import json
import requests
from bs4 import BeautifulSoup

# finds the pathway name using beautiful soup's .find
def parse_name(page):
    p = page.find("h1")
    return p.get_text()

# finds all body text for the pathway and grabs the courses for each
def parse_body(page):
    body = {}
    body["description"] = page.find("table", "table_default").find("table", "table_default").find_all("p")[1].get_text()
    # body["description"] = page.find_all("p")[0].get_text()
    for tag in page.find_all("div", "acalog-core"):
        header = tag.find_all("h2")
        if len(header) == 0:
            header = tag.find_all("h3")
            
        header = header[0].get_text()
        if header == "Required:":
            temp = []
            for a in tag.find_all("li"):
                txt = a.get_text()
                if txt != 'or' and len(txt) > 0 and txt[0] != '(':
                    temp.append(txt.strip())
            body["required"] = temp
        elif header == "Choose one of the following:":
            temp = []
            for a in tag.find_all("li"):
                txt = a.get_text()
                if txt != 'or' and len(txt) > 0 and txt[0] != '(':
                    temp.append(txt.strip())
            body["one_of"] = temp
        elif header == "Compatible minor:":
            temp = []
            for a in tag.find_all("a"):
                txt = a.get_text()
                if len(txt) > 0 and txt[0] != '(':
                    temp.append(txt.strip())
            body["minor"] = temp
        else:
            body["remaining_header"] = header
            temp = []
            for a in tag.find_all("li"):
                txt = a.get_text()
                if len(txt) > 0 and txt[0] != '(':
                    temp.append(txt.strip())
            body["remaining"] = temp

    return body

def get_soup(i):
    baseURL = "http://catalog.rpi.edu/preview_program.php?catoid=22&poid="
    r = requests.get(baseURL + str(i), headers={"User-Agent": "Mozilla"})
    soup = BeautifulSoup(r.text, features="html.parser")
    return soup


# should generate a beautiful soup of every pathway page
# the #'s after poid are the page number for the pathways which were manually found
# do note these numbers might change and are temporary
def fetch_webpages():
    all_pages = []

    for i in range(5539, 5561):
        all_pages.append(get_soup(i))

    for i in range(5562, 5585):
        all_pages.append(get_soup(i))

    i = 5596
    all_pages.append(get_soup(i))

    return all_pages

def main():
    all_pages = fetch_webpages()
    parsed_pages = {}
    for page in all_pages:
        parsed_pages[parse_name(page)] = parse_body(page)

    pathways = json.dumps(parsed_pages, indent=4, sort_keys=True)

    jsonFile = open("hass_pathways.json", "w")
    jsonFile.write(pathways)
    jsonFile.close()

if __name__ == "__main__":
    main() 