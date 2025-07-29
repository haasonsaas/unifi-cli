import click
import requests
import json
from .config import pass_config
from .util import handle_api_error

@click.group()
def clients():
    """Commands for interacting with UniFi clients."""
    pass

@clients.command('list')
@click.option('--site-id', required=True, help='The ID of the site to list clients for.')
@click.option('--filter', help='Filter the results.')
@pass_config
def list_clients(config, site_id, filter):
    """List all connected clients for a site."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    params = {}
    if filter:
        params['filter'] = filter

    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/clients", headers=headers, params=params, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        click.echo(json.dumps(data, indent=4))
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@clients.command('get')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--client-id', required=True, help='The ID of the client.')
@pass_config
def get_client(config, site_id, client_id):
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
        click.echo(json.dumps(data, indent=4))
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
