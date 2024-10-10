"""
This file contains functions used to fetch status update from Confluence.
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()
CONFLUENCE_URL = os.getenv("CONFLUENCE_PAGE")
USERNAME = os.getenv("ATLASSIAN_USERNAME")
API_TOKEN = os.getenv("ATLASSIAN_TOKEN")

SUBTEAMS = ["Camera", "Game", "ECE Display", "Mech Display"]
UPDATE_CATEGORIES = ["LWG", "R", "TWG"]


def form_update_dict(raw_update: str):
    """
    Returns a dictionary after parsing the raw string from the Confluence page scrape

    Args:
        raw_update (str): Status update string scraped from a web page.

    Returns:
        dict: Dictionary broken down into status update keys.
    """
    update_dict = {}
    soup = BeautifulSoup(raw_update, "html.parser")

    date = soup.find("h2").text
    update_dict[date] = {}

    # TODO - Iterate through soup to form dictionary

    return update_dict


def parse_content(content: str, date: str):
    """
    Parses a raw string from status update page for the substring for the specified date

    Args:
        content (str): Raw string of contents scraped from the Confluence web page.
        date (str): The date of the status update to be parsed for.

    Returns:
        dict: Dictionary broken down into status update keys.
    """
    # TODO - adjust regex pattern
    weekly_update_pattern = re.compile(
        rf"<h2>{date}.*?</ac:rich-text-body></ac:structured-macro><p />"
    )
    weekly_update = re.match(weekly_update_pattern, content)
    if weekly_update:
        return form_update_dict(weekly_update.group())
    return {}


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
        return parse_content(content=body, date=date)
    print(f"Failed to retrieve page. Status code: {response.status_code}")
    return {}
