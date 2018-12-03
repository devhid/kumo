import click
import os

from utils.constants import *
from crawler.crawler import Crawler
from configs import configs

# Some random defaults for configuration options.
default_config = configs.DEFAULT_CONFIGS
default_agent = default_config['user_agent']
default_search_method = default_config['traversal']
default_max_depth = default_config['max_depth']
default_max_pages = default_config['max_total']

# The entry point for our CLI.
@click.group()
def main():
    pass

# Sub-command for actually crawling the website.
@main.command(name='crawl')
# @click.option('--a', default=default_agent, help=HELP_AGENT)
# @click.option('--m', default=default_search_method, help=HELP_SEARCH_METHOD)
# @click.option('--depth', default=default_max_depth, help=HELP_MAX_DEPTH)
# @click.option('--pages', default=default_max_pages, help=HELP_MAX_PAGES)
@click.argument('url', type=click.STRING, metavar='<url>', required=True)
@click.argument('cfgs', type=click.STRING, metavar='<cfgs>', required=True)
def crawl(url, cfgs):
    click.secho("Crawler will begin on '{url}' with below settings:\n".format(url=url), fg='green')
    config = configs.load_config_section(config_section=cfgs)
    if config is None:
        print(f"Invalid config {cfgs}")
    else:
        for val in config:
            print("%s : %s" % (val,config[val]))
    click.echo()
    crawler = Crawler()
    crawler.crawl(url, config['traversal'], config['user_agent'], int(config['max_depth']), int(config['max_total']))

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
