import click
import json
import jmespath

def handle_api_error(response):
    """Parse and display a JSON error response from the API."""
    try:
        error_data = response.json()
        status_code = error_data.get('statusCode', response.status_code)
        status_name = error_data.get('statusName', 'Unknown Error')
        message = error_data.get('message', 'No message provided.')
        request_id = error_data.get('requestId', 'N/A')

        click.echo(f"Error: {status_code} ({status_name})", err=True)
        click.echo(f"  Message: {message}", err=True)
        click.echo(f"  Request ID: {request_id}", err=True)
    except json.JSONDecodeError:
        click.echo(f"Error: {response.status_code} {response.reason}", err=True)
        click.echo(f"  Response: {response.text}", err=True)

def print_json_output(data, raw_json=False, query=None):
    """Prints JSON data, optionally unformatted or filtered by JMESPath."""
    if query:
        data = jmespath.search(query, data)

    if raw_json:
        click.echo(json.dumps(data))
    else:
        click.echo(json.dumps(data, indent=4))
