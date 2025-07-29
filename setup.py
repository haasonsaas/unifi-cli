from setuptools import setup, find_packages

setup(
    name='unifi-cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'jmespath',
    ],
    entry_points={
        'console_scripts': [
            'unifi=unifi_cli.main:cli',
        ],
    },
)
