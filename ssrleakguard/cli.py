import click
import sys
from datetime import datetime
from pathlib import Path
from ssrleakguard.core.http_client import HTTPClient
from ssrleakguard.core.analyzer import SSRAnalyzer
from ssrleakguard.core.context import AuthContext
from ssrleakguard.utils.reporter import Reporter


class TeeOutput:
    """Write output to both terminal and file"""
    def __init__(self, *files):
        self.files = files
    
    def write(self, data):
        for f in self.files:
            f.write(data)
            f.flush()
    
    def flush(self):
        for f in self.files:
            f.flush()


@click.command()
@click.argument("url")
@click.option("--cookie", "-c", multiple=True)
@click.option("--context", multiple=True, help="name or name:key=value")
@click.option("--verbose", "-v", is_flag=True)
@click.option("--no-report", is_flag=True, help="Disable automatic report saving")
def main(url, cookie, context, verbose, no_report):
    # Setup report logging
    report_file = None
    original_stdout = sys.stdout
    
    if not no_report:
        # Create reports directory
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"ssrleakguard_report_{timestamp}.txt"
        
        # Open report file and redirect stdout
        report_file = open(report_path, 'w', encoding='utf-8')
        sys.stdout = TeeOutput(original_stdout, report_file)
        
        # Print report header
        command = ' '.join(sys.argv)
        print("=" * 70)
        print("SSRLeakGuard Security Scan Report")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Command: {command}")
        print("=" * 70)
        print()
    
    try:
        # Parse cookies
        cookies = {}
        for c in cookie:
            if "=" in c:
                k, v = c.split("=", 1)
                cookies[k] = v

        # Parse contexts
        contexts = []
        for ctx in context:
            if ":" not in ctx:
                contexts.append(AuthContext(name=ctx, cookies={}))
            else:
                name, cookie_part = ctx.split(":", 1)
                k, v = cookie_part.split("=", 1)
                contexts.append(AuthContext(name=name, cookies={k: v}))

        client = HTTPClient(cookies=cookies)
        analyzer = SSRAnalyzer(client, verbose=verbose)
        reporter = Reporter()

        # Phase 2 if contexts are provided
        if contexts:
            results = analyzer.analyze_with_contexts(url, contexts)
            reporter.print_authorization_report(results)
        else:
            # Phase 1
            results = analyzer.analyze(url)
            reporter.print_console_report(results)
    
    finally:
        # Restore stdout and close report file
        if not no_report and report_file:
            print()
            print("=" * 70)
            sys.stdout = original_stdout
            report_file.close()
            print(f"✓ Report saved to: {report_path}")
            print("=" * 70)


if __name__ == "__main__":
    main()