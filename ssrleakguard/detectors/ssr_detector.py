from bs4 import BeautifulSoup
from typing import Dict, Optional


class SSRDetector:
    """Detects if a page uses Server-Side Rendering"""

    @staticmethod
    def detect_ssr(html: str) -> Dict[str, any]:
        """
        Detect SSR framework and patterns

        Args:
            html: HTML content to analyze

        Returns:
            Dictionary with detection results:
            {
                'is_ssr': bool,
                'framework': str or None,
                'confidence': str,
                'indicators': list
            }
        """
        soup = BeautifulSoup(html, "lxml")
        indicators = []

        # Check for Next.js specific markers
        nextjs_detected = False

        # Look for __NEXT_DATA__ script
        next_data_script = soup.find(
            "script", {"id": "__NEXT_DATA__", "type": "application/json"}
        )
        if next_data_script:
            indicators.append("__NEXT_DATA__ script found")
            nextjs_detected = True

        # Look for Next.js build ID meta tag
        next_build_id = soup.find("meta", {"name": "next-head-count"})
        if next_build_id:
            indicators.append("Next.js meta tags found")
            nextjs_detected = True

        # Check for Next.js script tags
        next_scripts = soup.find_all("script", src=True)
        for script in next_scripts:
            src = script.get("src", "")
            if "_next/static/" in src or "/_next/" in src:
                indicators.append(f"Next.js script: {src}")
                nextjs_detected = True
                break

        # Check for meaningful initial HTML (sign of SSR)
        body = soup.find("body")
        if body:
            text_content = body.get_text(strip=True)
            if len(text_content) > 200:  # Arbitrary threshold
                indicators.append("Meaningful initial HTML content")

        if nextjs_detected:
            confidence = "high" if len(indicators) >= 2 else "medium"
            return {
                "is_ssr": True,
                "framework": "Next.js",
                "confidence": confidence,
                "indicators": indicators,
            }

        # If meaningful content but no framework detected
        if len(indicators) > 0:
            return {
                "is_ssr": True,
                "framework": "Unknown",
                "confidence": "low",
                "indicators": indicators,
            }

        return {
            "is_ssr": False,
            "framework": None,
            "confidence": "low",
            "indicators": ["No SSR indicators found"],
        }