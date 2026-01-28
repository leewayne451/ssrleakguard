import re
from typing import List, Dict, Tuple
from ssrleakguard.utils.patterns import SECRET_PATTERNS


class SecretScanner:
    """Scanner for detecting secrets and sensitive data in content"""

    def __init__(self):
        self.patterns = SECRET_PATTERNS

    def scan_content(self, content: str, context: str = "") -> List[Dict]:
        """
        Scan content for secrets using regex patterns

        Args:
            content: String content to scan
            context: Context information (e.g., "HTML body", "props.user")

        Returns:
            List of findings dictionaries
        """
        findings = []

        for pattern_name, pattern_info in self.patterns.items():
            regex = pattern_info["pattern"]
            matches = re.finditer(regex, content, re.IGNORECASE)

            for match in matches:
                # Extract matched secret
                secret = match.group(0)

                # Get surrounding context (50 chars before and after)
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                snippet = content[start:end]

                finding = {
                    "type": pattern_name,
                    "severity": pattern_info["severity"],
                    "secret": secret,
                    "description": pattern_info["description"],
                    "context": context,
                    "snippet": snippet.replace("\n", " ").strip(),
                    "position": match.start(),
                }

                # Validate if needed
                if "validator" in pattern_info:
                    if not pattern_info["validator"](secret):
                        continue

                findings.append(finding)

        return findings

    def scan_data_structure(
        self, data_paths: List[Tuple[str, any]]
    ) -> List[Dict]:
        """
        Scan structured data paths for secrets

        Args:
            data_paths: List of (path, value) tuples

        Returns:
            List of findings
        """
        findings = []

        for path, value in data_paths:
            if not isinstance(value, str):
                value = str(value)

            # Scan the value
            path_findings = self.scan_content(value, context=f"Path: {path}")

            # Add path-specific context
            for finding in path_findings:
                finding["data_path"] = path
                findings.append(finding)

        return findings