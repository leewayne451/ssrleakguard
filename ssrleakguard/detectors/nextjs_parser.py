import json
from bs4 import BeautifulSoup
from typing import Dict, Optional


class NextJSParser:
    """Parser for Next.js specific SSR data"""

    @staticmethod
    def extract_next_data(html: str) -> Optional[Dict]:
        """
        Extract and parse __NEXT_DATA__ from Next.js page

        Args:
            html: HTML content

        Returns:
            Parsed JSON data or None if not found
        """
        soup = BeautifulSoup(html, "lxml")

        # Find the __NEXT_DATA__ script tag
        next_data_script = soup.find(
            "script", {"id": "__NEXT_DATA__", "type": "application/json"}
        )

        if not next_data_script:
            return None

        try:
            data = json.loads(next_data_script.string)
            return data
        except (json.JSONDecodeError, AttributeError):
            return None

    @staticmethod
    def extract_page_props(next_data: Dict) -> Optional[Dict]:
        """
        Extract page props from __NEXT_DATA__

        Args:
            next_data: Parsed __NEXT_DATA__ object

        Returns:
            Page props dictionary or None
        """
        try:
            return next_data.get("props", {}).get("pageProps", {})
        except (AttributeError, TypeError):
            return None

    @staticmethod
    def extract_all_data_paths(data: Dict, prefix: str = "") -> list:
        """
        Recursively extract all data paths from nested dictionary

        Args:
            data: Dictionary to traverse
            prefix: Current path prefix

        Returns:
            List of (path, value) tuples
        """
        results = []

        if isinstance(data, dict):
            for key, value in data.items():
                current_path = f"{prefix}.{key}" if prefix else key

                if isinstance(value, (dict, list)):
                    results.extend(
                        NextJSParser.extract_all_data_paths(
                            value, current_path
                        )
                    )
                else:
                    results.append((current_path, value))

        elif isinstance(data, list):
            for idx, value in enumerate(data):
                current_path = f"{prefix}[{idx}]"

                if isinstance(value, (dict, list)):
                    results.extend(
                        NextJSParser.extract_all_data_paths(
                            value, current_path
                        )
                    )
                else:
                    results.append((current_path, value))

        return results