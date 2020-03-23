# API call tools
import requests
from bs4 import BeautifulSoup

from apps.api_key import *
from apps.url_tools import *
from apps.json_tools import *


def cited_cases(url, url_data):
    """citedCases call

    Returns formatted lists of case name strings. Uses the API to collect cases
    that are reported on CanLII, and a basic scraper to collect the ones that
    are not"""

    database_id = url_data['database_id']
    case_id = url_data['case_id']
    key = generate_key()
    api_url = ("https://api.canlii.org/v1/caseCitator/en/"
               f"{database_id}/{case_id}/citedCases?api_key={key}")

    # Formats the styles of cause to McGill 7E standard
    # Hosted cases
    hosted_cases = []
    canlii_url_list = []

    # generate_json() is being depreciated: replace with requests.json()
    case_dictionary = generate_json(api_url)['citedCases']
    for case in case_dictionary:

        style_of_cause = f"{case['title'].replace('.', '')}, {case['citation']}"
        case_url = url_constructor_case(case)
        hosted_cases.append((style_of_cause, case_url))


    # Unhosted cases
    unhosted_cases = cited_cases_unhosted(url)

    return hosted_cases, unhosted_cases

def cited_cases_unhosted(url):
    """Scrapes a valid CanLII decision page for cited cases not available on
    CanLII
    """

    html = requests.get(url)
    data = BeautifulSoup(html.content, 'html.parser')
    results = data.find_all("div", class_='col flex-wrap')
    unhosted_cases = []

    for result in results:

        if "(not available on CanLII)" in result.text:
            unhosted_cases.append(
                result.text.strip().replace('.', '')
                .replace('(not available on CanLII)', '')
            )

    return unhosted_cases

def metadata_call_case(url_data):
    """Metadata API call"""

    language = url_data['language']
    database_id = url_data['database_id']
    case_id = url_data['case_id']
    key = generate_key()
    api_url = ('https://api.canlii.org/v1/caseBrowse/'
               f'{language}/{database_id}/{case_id}/?api_key={key}')

    # generate_json() is being depreciated: replace with requests.json()
    return generate_json(api_url)
