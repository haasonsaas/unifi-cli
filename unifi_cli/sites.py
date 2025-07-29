import click
import requests
import json
from .config import pass_config
from .util import handle_api_error

@click.group()
def sites():
    """Commands for interacting with UniFi sites."""
    pass

@sites.command('list')
@click.option('--filter', help='Filter the results.')
@pass_config
def list_sites(config, filter):
    """List all sites."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    params = {}
    if filter:
        params['filter'] = filter

    try:
        # The -k flag in the curl example corresponds to verify=False in requests
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites", headers=headers, params=params, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        click.echo(json.dumps(data, indent=4))
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)
