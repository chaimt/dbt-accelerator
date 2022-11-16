import logging

import rich_click as click

logger = logging.getLogger(__name__)

CLI_CICD_COMMAND_GROUP = [
    {
        "name": "CI CD",
        "commands": ["enrich_catalog"],
    },
]


@click.group(help="Commands to use during CI CD flows")
def cicd():
    pass
