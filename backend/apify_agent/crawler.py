import requests
from bs4 import BeautifulSoup
import re

class WebCrawler:
    def __init__(self):
        pass

    def search_top_urls(self, query, max_results=5):
        """Search DuckDuckGo Lite HTML and extract top URLs."""
        try:
            url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            headers = {"User-Agent": "Mozilla/5.0"}

            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            urls = []

            # 1. Standard results: <a class="result__a">
            for a in soup.find_all("a", class_="result__a"):
                href = a.get("href")
                if href and href.startswith("http"):
                    urls.append(href)
                elif href and "uddg=" in href:
                    # decode DuckDuckGo redirect links
                    import urllib.parse
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                    if "uddg" in parsed:
                        urls.append(parsed["uddg"][0])

                if len(urls) >= max_results:
                    return urls

            # 2. Backup selector: <a class="result__url">
            for a in soup.find_all("a", class_="result__url"):
                href = a.get("href")
                if href and href.startswith("http"):
                    urls.append(href)
                if len(urls) >= max_results:
                    return urls

            # 3. Very fallback: any external link on results page
            # Filter out internal DDG links and common noise
            for a in soup.find_all("a"):
                href = a.get("href")
                if href and href.startswith("http") and "duckduckgo.com" not in href:
                    if href not in urls:
                        urls.append(href)
                if len(urls) >= max_results:
                    return urls

            return urls

        except Exception as e:
            print(f"[MultiSource] Search error: {e}")
            return []
        

    def crawl_url(self, url):
        """Fetch raw HTML and extract readable text."""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            resp = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator=" ", strip=True)
            return text

        except Exception as e:
            return f"[Error crawling {url}]"
