import click
import requests
import json
from .config import pass_config
from .util import handle_api_error, print_json_output

@click.group()
def clients():
    """Commands for interacting with UniFi clients."""
    pass

@clients.command('list')
@click.option('--site-id', required=True, help='The ID of the site to list clients for.')
@click.option('--filter', help='Filter the results.')
@click.option('--offset', type=int, default=0, help='Offset for pagination.')
@click.option('--limit', type=int, default=25, help='Limit for pagination (max 200).')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def list_clients(config, site_id, filter, offset, limit, json, query):
    """List all connected clients for a site."""
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
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/clients", headers=headers, params=params, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@clients.command('get')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--client-id', required=True, help='The ID of the client.')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def get_client(config, site_id, client_id, json, query):
    """Get detailed information about a specific client."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/clients/{client_id}", headers=headers, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@clients.command('authorize-guest')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--client-id', required=True, help='The ID of the client to authorize.')
@click.option('--time-limit', type=int, help='How long (in minutes) the guest will be authorized.')
@click.option('--data-usage-limit', type=int, help='Data usage limit in megabytes.')
@click.option('--rx-rate-limit', type=int, help='Download rate limit in kilobits per second.')
@click.option('--tx-rate-limit', type=int, help='Upload rate limit in kilobits per second.')
@pass_config
def authorize_guest(config, site_id, client_id, time_limit, data_usage_limit, rx_rate_limit, tx_rate_limit):
    """Authorize a specific client as a guest."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    data = {
        'action': 'AUTHORIZE_GUEST_ACCESS'
    }
    if time_limit is not None:
        data['timeLimitMinutes'] = time_limit
    if data_usage_limit is not None:
        data['dataUsageLimitMBytes'] = data_usage_limit
    if rx_rate_limit is not None:
        data['rxRateLimitKbps'] = rx_rate_limit
    if tx_rate_limit is not None:
        data['txRateLimitKbps'] = tx_rate_limit

    try:
        response = requests.post(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/clients/{client_id}/actions", headers=headers, json=data, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        click.echo(f"Client {client_id} guest authorization initiated.")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@clients.command('block')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--mac-address', required=True, help='The MAC address of the client to block.')
@click.confirmation_option(prompt='Are you sure you want to block this client?')
@pass_config
def block_client(config, site_id, mac_address):
    """Block a specific client by MAC address."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    data = {
        'cmd': 'block-sta',
        'mac': mac_address.lower()
    }
    try:
        response = requests.post(f"{config.url}/api/s/{site_id}/cmd/stamgr", headers=headers, json=data, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        click.echo(f"Client {mac_address} blocked.")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@clients.command('unblock')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--mac-address', required=True, help='The MAC address of the client to unblock.')
@click.confirmation_option(prompt='Are you sure you want to unblock this client?')
@pass_config
def unblock_client(config, site_id, mac_address):
    """Unblock a specific client by MAC address."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    data = {
        'cmd': 'unblock-sta',
        'mac': mac_address.lower()
    }
    try:
        response = requests.post(f"{config.url}/api/s/{site_id}/cmd/stamgr", headers=headers, json=data, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        click.echo(f"Client {mac_address} unblocked.")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)