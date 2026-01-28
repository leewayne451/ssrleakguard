from colorama import Fore, Style


class Reporter:
    SEVERITY_COLORS = {
        "critical": Fore.RED,
        "high": Fore.MAGENTA,
        "medium": Fore.YELLOW,
        "low": Fore.BLUE,
    }

    def print_console_report(self, results):
        """Phase 1: SSR Data Exposure Report"""
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
            print(f"{Fore.GREEN}[✓] No security issues detected{Style.RESET_ALL}")

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

        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}[!] Found {len(findings)} potential "
            f"security issue(s){Style.RESET_ALL}"
        )
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

    def print_authorization_report(self, results):
        """Phase 2: Authorization Inconsistency Report"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print("AUTHORIZATION ANALYSIS")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"Target URL: {results['url']}")
        print(f"Contexts tested: {', '.join(results['contexts'])}\n")

        findings = results["authorization_findings"]
        if not findings:
            print(f"{Fore.GREEN}[✓] No authorization inconsistencies detected{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Authorization Inconsistencies Found{Style.RESET_ALL}\n")

            for idx, f in enumerate(findings, 1):
                print(f"{idx}. Baseline: {f['baseline']} → Other: {f['other']}")
                print("   Diff:")
                for k, v in f["diff"].items():
                    print(f"     - {k}: {v}")

        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")