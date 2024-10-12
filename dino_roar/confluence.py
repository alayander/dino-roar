"""
This file contains functions used to fetch status update from Confluence.
"""

import os
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
CONFLUENCE_URL = os.getenv("CONFLUENCE_PAGE")
USERNAME = os.getenv("ATLASSIAN_USERNAME")
API_TOKEN = os.getenv("ATLASSIAN_TOKEN")

SUBTEAMS = ["Camera", "Game", "ECE Display", "Mech Display"]
UPDATE_CATEGORIES = ["R:", "TWG:"]


def extract_list_items(ul_element):
    """
    Recursively extract list items given a unordered list element.

    Args:
        ul_element (Tag): Unordered list element to extract from

    Returns:
        list: List of elements and subelements
    """
    extracted_items = []
    for item in ul_element.find_all("li", recursive=False):
        item_text = item.p.get_text(strip=True) if item.p else item.get_text(strip=True)
        next_level = item.find("ul")
        if next_level:
            extracted_items.append({item_text: extract_list_items(next_level)})
        else:
            extracted_items.append(item_text)
    return extracted_items


def parse_content(raw_content: str, date: str):
    """
    Parses a raw string from status update page for the substring for the specified date.

    Args:
        raw_content (str): Raw string of contents scraped from the Confluence web page.
        date (str): The date of the status update to be parsed for.

    Returns:
        dict: Dictionary broken down into status update keys.
    """
    update_dict = {}
    soup = BeautifulSoup(raw_content, "html.parser")

    date_heading = soup.find("h2", string=date)

    for subteam in SUBTEAMS:
        update_dict[subteam] = {}
        # Find subteam update
        subteam_heading = date_heading.find_next(string=subteam)
        if subteam_heading:
            for category_heading in UPDATE_CATEGORIES:
                # Find R (results from last week's goals) and TWG (this week's goals)
                section = subteam_heading.find_next(
                    "p", string=lambda text: text and text.strip() == category_heading
                )
                if section:
                    update_dict[subteam][category_heading] = extract_list_items(
                        section.find_next("ul")
                    )

    return update_dict


def fetch_content(date: str):
    """
    Fetches content from Confluence page to parse for status update.

    Args:
        date (str): The date of the status update to be parsed for.

    Returns:
        dict: Dictionary broken down into status update keys.
    """
    response = requests.get(
        CONFLUENCE_URL,
        auth=HTTPBasicAuth(USERNAME, API_TOKEN),
        params={"expand": "body.storage"},
        timeout=5,
    )

    if response.status_code == 200:
        page_content = response.json()
        body = page_content.get("body", {}).get("storage", {}).get("value")
        return parse_content(raw_content=body, date=date)
    print(f"Failed to retrieve page. Status code: {response.status_code}")
    return {}
