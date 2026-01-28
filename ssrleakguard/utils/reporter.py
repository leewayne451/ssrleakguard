from colorama import Fore, Style


class Reporter:
    SEVERITY_COLORS = {
        "critical": Fore.RED,
        "high": Fore.MAGENTA,
        "medium": Fore.YELLOW,
        "low": Fore.BLUE,
    }

    from colorama import Fore, Style


    def print_console_report(self, results):
        print(f"\n{Fore.CYAN}{'='*60}")
        print("ANALYSIS RESULTS")
        print(f"{'='*60}{Style.RESET_ALL}\n")

        print(f"{Fore.WHITE}Target URL:{Style.RESET_ALL} {results['url']}")
        print(
            f"{Fore.WHITE}SSR Detected:{Style.RESET_ALL} "
            f"{'Yes' if results['ssr_detected'] else 'No'}"
        )

        if results.get("framework"):
            print(
                f"{Fore.WHITE}Framework:{Style.RESET_ALL} "
                f"{results['framework']}"
            )

        metadata = results.get("metadata", {})
        if metadata:
            print(f"\n{Fore.CYAN}Metadata:{Style.RESET_ALL}")
            for key, value in metadata.items():
                print(f"  - {key}: {value}")

        findings = results.get("findings", [])
        print(
            f"\n{Fore.CYAN}Findings: {len(findings)}"
            f"{Style.RESET_ALL}\n"
        )

        if not findings:
            print(f"{Fore.GREEN}[✓] No security issues detected")

        else:
            # Group findings by severity
            grouped = {}
            for f in findings:
                sev = f.get("severity", "medium")
                grouped.setdefault(sev, []).append(f)

            for severity in ["critical", "high", "medium", "low"]:
                if severity not in grouped:
                    continue

                color = self.SEVERITY_COLORS.get(severity, Fore.WHITE)
                group = grouped[severity]

                print(
                    f"{color}[{severity.upper()}] "
                    f"{len(group)} finding(s){Style.RESET_ALL}"
                )

                for idx, f in enumerate(group, 1):
                    print(f"\n  {idx}. {f.get('description', f['type'])}")
                    print(f"     Type: {f['type']}")
                    print(f"     Context: {f['context']}")

                    if "data_path" in f:
                        print(f"     Data Path: {f['data_path']}")

                    secret = f.get("secret", "")
                    if secret:
                        if len(secret) > 60:
                            secret = secret[:57] + "..."
                        print(f"     Secret: {secret}")

                    snippet = f.get("snippet")
                    if snippet:
                        if len(snippet) > 100:
                            snippet = snippet[:97] + "..."
                        print(f"     Snippet: ...{snippet}...")

                print()

        # ✅ Phase 3 — Cache safety analysis
        cache = results.get("cache_analysis")
        if cache:
            issues = cache.get("cache_issues", [])

            print(f"\n{Fore.CYAN}CACHE SAFETY ANALYSIS{Style.RESET_ALL}")

            if not issues:
                print(f"{Fore.GREEN}[✓] No cache-related SSR issues detected")
            else:
                for idx, issue in enumerate(issues, 1):
                    print(
                        f"\n{Fore.RED}{idx}. {issue['issue']}"
                        f"{Style.RESET_ALL}"
                    )
                    print(f"   Severity: {issue['severity']}")
                    print(f"   Evidence: {issue['evidence']}")

        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}[!] Found {len(findings)} potential "
            f"security issue(s){Style.RESET_ALL}"
        )
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    # ✅ NEW PHASE 2 REPORT
    def print_authorization_report(self, results):
        print("\n=== AUTHORIZATION ANALYSIS ===")
        print(f"Target URL: {results['url']}")
        print(f"Contexts tested: {', '.join(results['contexts'])}")

        findings = results["authorization_findings"]
        if not findings:
            print(f"{Fore.GREEN}[✓] No authorization inconsistencies detected{Style.RESET_ALL}")
            return

        print(f"\n{Fore.YELLOW}[!] Authorization Inconsistencies Found{Style.RESET_ALL}\n")

        for idx, f in enumerate(findings, 1):
            print(f"{idx}. Baseline: {f['baseline']} → Other: {f['other']}")
            print("   Diff:")
            for k, v in f["diff"].items():
                print(f"     - {k}: {v}")


    def print_cache_report(self, cache_analysis):
        issues = cache_analysis.get("cache_issues", [])

        print("\n=== CACHE SAFETY ANALYSIS ===")

        if not issues:
            print("[✓] No cache-related SSR issues detected")
            return

        for idx, issue in enumerate(issues, 1):
            print(f"\n{idx}. {issue['issue']}")
            print(f"   Severity: {issue['severity']}")
            print(f"   Evidence: {issue['evidence']}")