
Author: KS
Date: 2025-06-14
Description: This script automatically updates the README.md file with a daily quote from the user's Goodreads profile.
'''

import os
import re
import requests
from bs4 import BeautifulSoup

URL = os.getenv("PROFILE_URL", "https://www.goodreads.com/user/show/99699399-cat-the-bookworm-semi-hiatus-ish")
HEADERS = {"User-Agent": "Mozilla/5.0"}
README_PATH = ".tmp/Goodreads Quote.md.tpl"
START_MARKER = "<!-- QUOTE_START -->"
END_MARKER = "<!-- QUOTE_END -->"

try:
   
    res = requests.get(URL, headers=HEADERS)
    res.raise_for_status() 
    soup = BeautifulSoup(res.text, "html.parser")

  
    quote_block = soup.select_one("div.quoteDetails")
    if not quote_block:
        raise RuntimeError("Quote container not found")

 
    text_div = quote_block.find("div", class_="quoteText")
    if not text_div:
        raise RuntimeError("Quote text element not found")
    
 
    full_text = text_div.get_text(separator=" ", strip=True)
    quote_text = ""
    author = "Unknown"

    
    match = re.search(r'^(“.*?”|".*?")(.*?)$', full_text)
    if match:
        quote_text = match.group(1).strip()
        author_part = match.group(2).strip()
        author = re.sub(r'^[―–—\s]+', '', author_part).split('\n')[0].strip()
    else:
        quote_text = full_text.split('Delete')[0].strip()

   
    img_tag = quote_block.find("img")
    author_img_url = img_tag['src'] if img_tag else None
    

    markdown_content = '<table><tr>\n'
    
    # Left column for image (if available)
    if author_img_url:
        markdown_content += '<td width="30%" align="center">\n'
        markdown_content += f'  <img src="{author_img_url}" alt="{author}" width="150" style="border-radius:50%">\n'
        markdown_content += '</td>\n'
    
    # Right column for quote
    markdown_content += '<td width="70%" valign="center">\n'
    markdown_content += f'  <p style="font-size: 16px; font-style: italic;">{quote_text}</p>\n'
    markdown_content += f'  <p align="right" style="font-weight: bold;">― {author}</p>\n'
    markdown_content += '</td>\n'
    
    markdown_content += '</tr></table>'

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.index(START_MARKER) + len(START_MARKER)
    end_idx = content.index(END_MARKER)
    
    new_content = (
        content[:start_idx] +
        "\n\n" + markdown_content + "\n\n" +
        content[end_idx:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README updated successfully!")
    print(f"Quote: {quote_text[:50]}...")
    print(f"Author: {author}")
    print(f"Image: {'Found' if author_img_url else 'Not found'}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
