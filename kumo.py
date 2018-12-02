import click
import os

from utils.constants import *

# Some random defaults for configuration options.
default_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
default_search_method = 'dfs'
default_max_depth = 5
default_max_pages = 10

# The entry point for our CLI.
@click.group()
def main():
    pass

# Sub-command for actually crawling the website.
@main.command(name='crawl')
@click.option('--a', default=default_agent, help=HELP_AGENT)
@click.option('--m', default=default_search_method, help=HELP_SEARCH_METHOD)
@click.option('--depth', default=default_max_depth, help=HELP_MAX_DEPTH)
@click.option('--pages', default=default_max_pages, help=HELP_MAX_PAGES)
@click.argument('url', type=click.STRING, metavar='<url>', required=True)
def crawl(a, m, depth, pages, url):
    print(url)
    pass

# Sub-command that displays information about the project.
@main.command(name='info')
def info():
    # Gets the width of the terminal.
    terminal_width = os.get_terminal_size().columns

    # Project information and metadata.
    title = 'kumo [クモ]'.center(terminal_width)[:-2]
    description = 'A configurable, efficient web crawler and form brute-forcer written in Python.\n'.center(terminal_width)
    version = 'version: 0.1'.center(terminal_width)
    authors = 'authors: Johnny So, Andy Liang, Stanley Lim, Mankirat Gulati'.center(terminal_width)
    github = 'github: http://github.com/devhid/kumo'.center(terminal_width)

    # Output to STDOUT with ANSI coloring.
    click.secho(title, fg='green')
    click.secho(description, fg='blue')
    click.secho(version, fg='yellow')
    click.secho(authors, fg='yellow')
    click.secho(github, fg='yellow')