import click
import requests
import json
from .config import pass_config
from .util import handle_api_error, print_json_output

@click.group()
def hotspot():
    """Commands for interacting with UniFi Hotspot."""
    pass

@hotspot.group()
def vouchers():
    """Commands for managing Hotspot vouchers."""
    pass

@vouchers.command('list')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--filter', help='Filter the results.')
@click.option('--offset', type=int, default=0, help='Offset for pagination.')
@click.option('--limit', type=int, default=100, help='Limit for pagination (max 1000).')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def list_vouchers(config, site_id, filter, offset, limit, json, query):
    """List all Hotspot vouchers for a site."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    params = {
        'offset': offset,
        'limit': limit
    }
    if filter:
        params['filter'] = filter

    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/hotspot/vouchers", headers=headers, params=params, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@vouchers.command('generate')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--count', default=1, help='Number of vouchers to generate.')
@click.option('--name', required=True, help='Voucher note.')
@click.option('--time-limit', required=True, type=int, help='Voucher time limit in minutes.')
@pass_config
def generate_vouchers(config, site_id, count, name, time_limit):
    """Generate Hotspot vouchers."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    data = {
        'count': count,
        'name': name,
        'timeLimitMinutes': time_limit
    }
    try:
        response = requests.post(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/hotspot/vouchers", headers=headers, json=data, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        click.echo(json.dumps(data, indent=4))
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@vouchers.command('delete')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--voucher-id', required=True, help='The ID of the voucher to delete.')
@pass_config
def delete_voucher(config, site_id, voucher_id):
    """Delete a specific Hotspot voucher."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    try:
        response = requests.delete(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/hotspot/vouchers/{voucher_id}", headers=headers, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        click.echo(json.dumps(data, indent=4))
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@vouchers.command('get')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--voucher-id', required=True, help='The ID of the voucher.')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def get_voucher(config, site_id, voucher_id, json, query):
    """Retrieve details of a specific Hotspot voucher."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/hotspot/vouchers/{voucher_id}", headers=headers, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)
