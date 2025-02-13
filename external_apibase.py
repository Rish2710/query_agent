import requests

EXTERNAL_API_URL = "https://openlibrary.org/search.json"

def fetch_external_reports(query):
    """Fetch reports from an external API."""
    response = requests.get(EXTERNAL_API_URL, params={"q": query})
    return response.json().get("reports", [])
