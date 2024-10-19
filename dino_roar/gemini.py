"""
This file contains functions used to interact with Google Gemini.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("GEMINI_TOKEN")


def gemini_summarize(prompt: str):
    """
    Interact with Gemini and feed given prompt.

    Args:
        prompt (str): The prompt to be given to Gemini.

    Returns:
        str: Output summary from Gemini.
    """
    genai.configure(api_key=API_TOKEN)
    model = genai.GenerativeModel("gemini-1.5-flash")

    payload = f"""Summarize the following content into a similar format 1500 characters or less.
    Maintain headings of each subteam (Camera, Game, ECE Display, Mech Display), but no title.
    R means results, TWG means this week's goals. Replace the subheadings with Progress and Action Items.
    {prompt}"""

    result = model.generate_content(payload).text
    return result
