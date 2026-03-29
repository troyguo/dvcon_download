import urllib.request
import urllib.parse
import os
import re
import sys
import codecs
from urllib.error import HTTPError, URLError
import requests

# ===================== Configuration =====================
BASE_URL = "https://dvcon-proceedings.org/document-library"
SAVE_DIR = "dvcon_pdfs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close"
}

visited = set()
# =========================================================

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_html(url):
    """Fetch HTML content with headers"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Failed to fetch page: {url} | Error: {str(e)}")
        return None

def download_pdf(pdf_url, save_path):
    """Download a single PDF file"""
    try:
        response = requests.get(pdf_url, stream=True, timeout=30)
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
            print(f"✅ Download succeeded: {save_path}")
    except Exception as e:
        print(f"❌ Download failed: {pdf_url} | Error: {str(e)}")

def crawl(url):
    """Recursively crawl pages and download PDFs"""
    if url in visited:
        return
    visited.add(url)

    #print(f"\nCrawling: {url}")
    html = get_html(url)
    if not html:
        return

    # Find and download all PDFs
    pdf_pattern = r'href="(https?://[^"]+\.pdf)"'
    pdf_links = re.findall(pdf_pattern, html, re.IGNORECASE)

    for pdf_link in pdf_links:
        pdf_link = urllib.parse.urljoin(BASE_URL, pdf_link)
        filename = os.path.basename(pdf_link.split("?")[0])
        save_path = os.path.join(SAVE_DIR, filename)
        if(not os.path.exists(save_path)):
            print(f"Prepare to download: {pdf_link, save_path}")
            download_pdf(pdf_link, save_path)

    # Find internal links to crawl
    link_pattern = r'href="(https?://dvcon-proceedings\.org[^"]+)"'
    page_links = re.findall(link_pattern, html)

    for link in page_links:
        if link not in visited and not link.lower().endswith(".pdf"):
            crawl(link)

if __name__ == "__main__":
    print("Starting recursive PDF crawler...")
    crawl(BASE_URL)
    print(f"\nCrawling finished! All PDFs saved in: {os.path.abspath(SAVE_DIR)}")
