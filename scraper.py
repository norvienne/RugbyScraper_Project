import requests

# ESPN blocks requests without proper headers so we pretend to be a browser
request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# fetches the html from a given url
# returns the html as a string or None if it fails
def fetch_espn_page(url):
    try:
        response = requests.get(url, headers=request_headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"error fetching page: {e}")
        return None


#  test
html = fetch_espn_page("https://www.espn.com/rugby")
if html:
    print("page fetched successfully")
    print(f"got {len(html)} characters of html")
else:
    print("failed to fetch page")
