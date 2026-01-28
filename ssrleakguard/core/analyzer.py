from ssrleakguard.detectors.ssr_detector import SSRDetector
from ssrleakguard.detectors.nextjs_parser import NextJSParser
from ssrleakguard.detectors.secret_scanner import SecretScanner
from ssrleakguard.utils.normalizer import normalize_ssr_data
from ssrleakguard.core.differ import diff_ssr_states
from ssrleakguard.core.context import AuthContext
from ssrleakguard.detectors.cache_detector import CacheDetector


class SSRAnalyzer:
    def __init__(self, client, verbose=False):
        self.client = client
        self.verbose = verbose
        self.ssr_detector = SSRDetector()
        self.nextjs_parser = NextJSParser()
        self.secret_scanner = SecretScanner()

    def _log(self, msg):
        if self.verbose:
            print(f"[DEBUG] {msg}")

    def analyze(self, url: str):
        response = self.client.get(url)
        html = response.text

        ssr_info = self.ssr_detector.detect_ssr(html)

        results = {
            "url": url,
            "ssr_detected": ssr_info["is_ssr"],
            "framework": ssr_info["framework"],
            "metadata": ssr_info,
            "findings": [],
            "cache_analysis": None,
        }

        if not ssr_info["is_ssr"]:
            return results

        next_data = self.nextjs_parser.extract_next_data(html)
        if next_data:
            page_props = self.nextjs_parser.extract_page_props(next_data)
            if page_props:
                paths = self.nextjs_parser.extract_all_data_paths(page_props)
                results["findings"].extend(
                    self.secret_scanner.scan_data_structure(paths)
                )

        results["findings"].extend(
            self.secret_scanner.scan_content(html, context="HTML body")
        )

        # ✅ Phase 3: cache analysis
        results["cache_analysis"] = CacheDetector.analyze(
            response, results["findings"]
        )

        return results

    # ✅ PHASE 2 ENTRY POINT
    def analyze_with_contexts(self, url: str, contexts: list[AuthContext]):
        ssr_states = {}

        for ctx in contexts:
            self._log(f"Fetching context: {ctx.name}")
            client = self.client.clone_with_cookies(ctx.cookies)

            response = client.get(url)
            html = response.text

            next_data = self.nextjs_parser.extract_next_data(html)
            if not next_data:
                continue

            normalized = normalize_ssr_data(next_data)
            ssr_states[ctx.name] = normalized

        authorization_findings = diff_ssr_states(ssr_states)

        return {
            "url": url,
            "contexts": list(ssr_states.keys()),
            "authorization_findings": authorization_findings,
        }