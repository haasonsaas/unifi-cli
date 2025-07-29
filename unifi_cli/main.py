import click
from .config import pass_config

@click.group()
@pass_config
def cli(config):
    """A CLI tool to interact with the UniFi Network API."""
    pass

from .sites import sites
from .devices import devices
from .clients import clients
from .hotspot import hotspot
from .app import info

cli.add_command(sites)
cli.add_command(devices)
cli.add_command(clients)
cli.add_command(hotspot)
cli.add_command(info)

if __name__ == '__main__':
    cli()
