import click
from ssrleakguard.core.http_client import HTTPClient
from ssrleakguard.core.analyzer import SSRAnalyzer
from ssrleakguard.core.context import AuthContext
from ssrleakguard.utils.reporter import Reporter


@click.command()
@click.argument("url")
@click.option("--cookie", "-c", multiple=True)
@click.option("--context", multiple=True, help="name or name:key=value")
@click.option("--verbose", "-v", is_flag=True)
def main(url, cookie, context, verbose):
    cookies = {}
    for c in cookie:
        if "=" in c:
            k, v = c.split("=", 1)
            cookies[k] = v

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


if __name__ == "__main__":
    main()