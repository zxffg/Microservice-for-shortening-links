import requests
from urllib.parse import urlparse

def is_real_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return False
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code < 400

    except Exception:
        return False
    
print(is_real_url("https://www.youtubЕ.com/"))
