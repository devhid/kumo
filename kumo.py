import click
import os

# Some random defaults for configuration options.
default_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
default_search_method = 'dfs'
default_max_depth = 5
default_max_pages = 10

# Help messages for all the configuration options.
help_agent = 'A custom user-agent for use with each GET/POST request.'
help_search_method = 'The search traversal method for crawling: bfs|dfs.'
help_max_depth = 'The maximum depth of pages to crawl.'
help_max_pages = 'The maximum total number of crawled pages.'

# The entry point for our CLI.
@click.command()
@click.option('--a', default=default_agent, help=help_agent)
@click.option('--m', default=default_search_method, help=help_search_method)
@click.option('--d', default=default_max_depth, help=help_max_depth)
@click.option('--n', default=default_max_pages, help=help_max_pages)
def main(a, m, d, n):
    terminal_width = os.get_terminal_size().columns

    click.secho('kumo [クモ]'.center(terminal_width)[:-2], fg='green')
    click.secho('A configurable, efficient web crawler and form brute-forcer written in Python.\n'.center(terminal_width), fg='blue')
    click.secho('version: 0.1'.center(terminal_width), fg='yellow')
    click.secho('authors: Johnny So, Andy Liang, Stanley Lim, Mankirat Gulati'.center(terminal_width), fg='yellow')
    click.secho('github: http://github.com/devhid/kumo'.center(terminal_width), fg='yellow')