from colorama import Fore, Style


class Reporter:
    SEVERITY_COLORS = {
        "critical": Fore.RED,
        "high": Fore.MAGENTA,
        "medium": Fore.YELLOW,
        "low": Fore.BLUE,
    }
    
    # Remediation guidance for different vulnerability types
    REMEDIATIONS = {
        "email": "Filter email addresses from data before passing to getServerSideProps() or page props",
        "user_id": "Use opaque identifiers instead of internal user IDs in SSR output",
        "token": "Never include tokens in SSR output; store authentication tokens in httpOnly cookies",
        "api_key": "Move API keys to server-side environment variables and never expose in SSR props",
        "password": "Never send password hashes or related data to client-side rendering",
        "credit_card": "Remove all payment information from SSR data; fetch only when needed via secure API",
        "ssn": "Never include SSNs or other PII in SSR output",
        "internal_id": "Replace internal IDs with public-facing identifiers before serialization",
        "role": "Avoid exposing user roles in SSR props; validate permissions server-side only",
        "phone": "Filter phone numbers from SSR props unless explicitly needed for display",
        "address": "Only include address data when necessary; filter from bulk user data",
        "jwt": "Store JWT tokens in httpOnly cookies, never in SSR props or localStorage",
        "session": "Use httpOnly cookies for session management, not SSR-serialized data",
        "env": "Ensure environment variables are not leaked through SSR; use server-only code",
        "database": "Never expose database credentials; keep them in secure server-side configuration",
        "aws": "Move AWS credentials to server-side environment variables and never expose in SSR props",
        "secret": "Remove secrets from SSR output; use server-side environment variables",
        "authorization_inconsistency": "Add proper authorization checks in getServerSideProps() before fetching sensitive data",
        "cache_unsafe_personalization": "Add 'Cache-Control: private' or 'Vary: Cookie' header for user-specific pages",
        "default": "Review SSR data serialization logic and filter sensitive information before rendering"
    }
    
    def get_remediation(self, finding_type):
        """Get remediation guidance for a specific finding type"""
        finding_lower = finding_type.lower()
        
        # Try exact match first
        if finding_lower in self.REMEDIATIONS:
            return self.REMEDIATIONS[finding_lower]
        
        # Try partial match - check if any key is contained in the finding type
        for key, value in self.REMEDIATIONS.items():
            if key in finding_lower:
                return value
        
        # Return default if no match
        return self.REMEDIATIONS["default"]

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
                    
                    # Add remediation guidance
                    remediation = self.get_remediation(f['type'])
                    print(f"     {Fore.GREEN}Remediation:{Style.RESET_ALL} {remediation}")

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
                
                # Add remediation guidance for authorization issues
                remediation = self.get_remediation("authorization_inconsistency")
                print(f"   {Fore.GREEN}Remediation:{Style.RESET_ALL} {remediation}\n")

        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")