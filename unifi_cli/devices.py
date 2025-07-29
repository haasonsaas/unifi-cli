import click
import requests
import json
from .config import pass_config
from .util import handle_api_error, print_json_output

@click.group()
def devices():
    """Commands for interacting with UniFi devices."""
    pass

@devices.command('list')
@click.option('--site-id', required=True, help='The ID of the site to list devices for.')
@click.option('--filter', help='Filter the results.')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def list_devices(config, site_id, filter, json, query):
    """List all devices for a site."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    params = {}
    if filter:
        params['filter'] = filter

    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/devices", headers=headers, params=params, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@devices.command('get')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--device-id', required=True, help='The ID of the device.')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def get_device(config, site_id, device_id, json, query):
    """Get detailed information about a specific device."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/devices/{device_id}", headers=headers, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@devices.command('restart')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--device-id', required=True, help='The ID of the device to restart.')
@pass_config
def restart_device(config, site_id, device_id):
    """Restart a specific device."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    data = {
        'action': 'RESTART'
    }
    try:
        response = requests.post(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/devices/{device_id}/actions", headers=headers, json=data, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        click.echo(f"Device {device_id} restart initiated.")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@devices.command('power-cycle-port')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--device-id', required=True, help='The ID of the device.')
@click.option('--port-idx', required=True, type=int, help='The index of the port to power cycle.')
@pass_config
def power_cycle_port(config, site_id, device_id, port_idx):
    """Power cycle a specific port on a device."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    data = {
        'action': 'POWER_CYCLE'
    }
    try:
        response = requests.post(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/devices/{device_id}/interfaces/ports/{port_idx}/actions", headers=headers, json=data, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        click.echo(f"Port {port_idx} on device {device_id} power cycle initiated.")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)

@devices.command('get-latest-statistics')
@click.option('--site-id', required=True, help='The ID of the site.')
@click.option('--device-id', required=True, help='The ID of the device.')
@click.option('--json', is_flag=True, help='Output raw JSON.')
@click.option('--query', help='JMESPath query to apply to the JSON output.')
@pass_config
def get_latest_statistics(config, site_id, device_id, json, query):
    """Retrieve the latest real-time statistics of a specific adopted device."""
    headers = {
        'X-API-KEY': config.api_key,
        'Accept': 'application/json'
    }
    try:
        response = requests.get(f"{config.url}/proxy/network/integration/v1/sites/{site_id}/devices/{device_id}/statistics/latest", headers=headers, verify=False)
        if not response.ok:
            handle_api_error(response)
            return
        data = response.json()
        print_json_output(data, raw_json=json, query=query)
    except requests.exceptions.RequestException as e:
        click.echo(f"Error: {e}", err=True)
