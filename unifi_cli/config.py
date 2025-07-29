import os
import click
import json
from pathlib import Path

class Config:
    def __init__(self):
        self.url = os.environ.get('UNIFI_URL')
        self.api_key = os.environ.get('UNIFI_API_KEY')

        config_file = Path.home() / '.unifi_cli.json'
        if config_file.exists():
            with open(config_file) as f:
                config_data = json.load(f)
            if not self.url:
                self.url = config_data.get('url')
            if not self.api_key:
                self.api_key = config_data.get('api_key')

        if not self.url or not self.api_key:
            raise click.UsageError(
                'UniFi URL and API key must be configured. \n'
                'Set UNIFI_URL and UNIFI_API_KEY environment variables, or create a .unifi_cli.json file in your home directory with "url" and "api_key" keys.'
            )

pass_config = click.make_pass_decorator(Config, ensure=True)
