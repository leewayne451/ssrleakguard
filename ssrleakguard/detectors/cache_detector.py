from typing import Dict


class CacheDetector:
    """
    Detects cache-unsafe SSR responses.
    """

    @staticmethod
    def analyze(response, ssr_findings: list) -> Dict:
        headers = {k.lower(): v for k, v in response.headers.items()}

        cache_control = headers.get("cache-control", "")
        vary = headers.get("vary", "")

        issues = []

        # Heuristic 1: SSR + sensitive data should not be publicly cached
        if ssr_findings:
            if "public" in cache_control or "max-age" in cache_control:
                issues.append(
                    {
                        "issue": "Personalized SSR response appears cacheable",
                        "evidence": f"Cache-Control: {cache_control}",
                        "severity": "high",
                    }
                )

        # Heuristic 2: Missing Vary: Cookie
        if ssr_findings and "cookie" not in vary.lower():
            issues.append(
                {
                    "issue": "Missing Vary: Cookie on personalized SSR response",
                    "evidence": f"Vary: {vary or '(not set)'}",
                    "severity": "high",
                }
            )

        return {
            "cache_issues": issues,
            "cache_control": cache_control,
            "vary": vary,
        }