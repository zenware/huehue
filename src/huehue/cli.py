import logging
from typing import Dict, Optional
from pathlib import Path
import sys

import click
import click_log

from huehue import __version__
from huehue.bridge import Bridge

from . import __version__


class CliContext:
    """
    Should I put the bridge in here?
    Should I put the API Client in here? What does that mean?
    Does that allow the urllib3 bits to spread nicely throughout my program?
    """
    def __init__(self) -> None:
        self.__api_client: Optional[HueAPIClient] = None
        self.bridge: Optional[Bridge] = None
        self.config = {}

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose:
            click.echo(f" config['{key}'] = {value}", file=sys.stderr)

    def __repr__(self):
        return f"<CliContext {self}>"


#pass_context = click.make_pass_decorator(CliContext)


def __verbosity_count_to_log_level(count: int) -> int:
    """Converts '-vvv' to logging log level.

    Args:
        count (int): A count of -v's provided on the CLI.

    Returns:
        int: log level for logging module
    """
    log_levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    verbosity_level = count if count <= 3 else len(log_levels) - 1
    if verbosity_level > 3:
        print("There are only 4 levels of verbosity.")
    return log_levels[verbosity_level]


@click.group(chain=True)
@click.option(
    "--config",
    nargs=2,
    multiple=True,
    metavar="Key/Value Pair",
    help="Overrides a config K/V Pair."
)
@click.option('-v', '--verbose', count=True, help='Set verbosity level.')
# TODO: Figure out why the hell this isn't working.
#@click.version_option(version=__version__)
@click.pass_context
def cli(ctx: click.Context, config, verbose: int) -> None:
    """This is the main command group for the click based CLI.

    Args:
        ctx (click.Context): Click context object.
        config ([type]): User adjustments to configuration for this run.
        verbose ([type]): User selected verbosity for this run.
    """
    logger = click_log.basic_config()
    logger.setLevel(__verbosity_count_to_log_level(verbose))

    context = CliContext()
    ctx.obj = context
    for key, value in config:
        ctx.obj.set_config(key, value)

@cli.command()
@click.pass_obj
def bridge(ctx: click.Context) -> None:
    """Does things with bridges"""
    ctx.bridge = Bridge()
    print(f"Bridge: <{ctx.bridge}>")



@cli.command('list')
@click.pass_obj
def show_list(ctx: click.Context) -> None:
    """Lists whatever deserves to be listed."""
    ctx.bridge.discover_bridges()
    print("List")