import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore")


def fetch_sitemap_urls(sitemap_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # Fetch the sitemap.xml content
        response = requests.get(sitemap_url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the sitemap: {e}")
        return None


def parse_sitemap_urls(sitemap_content):
    if sitemap_content is None:
        return []

    # Parse the XML content with BeautifulSoup
    soup = BeautifulSoup(sitemap_content, 'lxml')

    # Find all 'loc' tags which contain the URLs
    url_tags = soup.find_all('loc')

    # Extract the URLs from the 'loc' tags
    sitemap_urls = [url_tag for url_tag in url_tags]
    urls = []

    for sitemap_url in sitemap_urls:
        url = sitemap_url.text.strip()
        if url.endswith('.xml'):
            urls += parse_sitemap_urls(fetch_sitemap_urls(url))
        else:
            urls.append(url)

    return urls

website_url = input("The Url: ")
sitemap_url = urljoin(website_url, 'sitemap.xml')
sitemap_content = fetch_sitemap_urls(sitemap_url)
urls = parse_sitemap_urls(sitemap_content)
for url in urls:
    print(url)
