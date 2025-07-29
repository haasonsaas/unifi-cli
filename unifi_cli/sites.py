import click
import requests
import json
from .config import pass_config
from .util import handle_api_error, print_json_output

@click.group()
def sites():
    """Commands for interacting with UniFi sites."""
    pass

@sites.command('list')
@click.option('--filter', help='Filter the results.')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def list_sites(config, filter, json, query):
    """List all sites."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    params = {}
    if filter:
        params['filter'] = filter

    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites", headers=headers, params=params, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)
