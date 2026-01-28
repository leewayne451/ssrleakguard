import requests
from typing import Dict, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPClient:
    """HTTP client with retry logic and session management"""

    def __init__(
        self,
        cookies: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
    ):
        self.session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Set default headers
        self.session.headers.update(
            {
                "User-Agent": (
                    "SSRLeakGuard/0.1.0 "
                    "(Security Testing Tool)"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,*/*;q=0.8"
                ),
                "Accept-Language": "en-US,en;q=0.9",
            }
        )

        # Apply custom headers and cookies
        if headers:
            self.session.headers.update(headers)
        if cookies:
            self.session.cookies.update(cookies)

        self.timeout = timeout

    def get(self, url: str) -> requests.Response:
        """
        Perform GET request

        Args:
            url: Target URL

        Returns:
            Response object

        Raises:
            requests.RequestException: If request fails
        """
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response
    
    def clone_with_cookies(self, cookies: Dict[str, str]):
        client = HTTPClient(
            cookies=cookies,
            headers=dict(self.session.headers),
            timeout=self.timeout,
        )
        return client

    def close(self):
        """Close the session"""
        self.session.close()