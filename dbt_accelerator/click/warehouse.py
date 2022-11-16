import logging

import rich_click as click

from dbt_accelerator.click.log_decorators import wrap_action
from dbt_accelerator.companion.warehouse_companion import WarehouseCompanion

logger = logging.getLogger(__name__)


CLI_WAREHOUSE_COMMAND_GROUPS = [
    {
        "name": "Advanced usage",
        "commands": ["setup_user_database", "clean_user_database"],
    }
]


@click.command(help="Set up warehouse database for a new Yoda user")
@wrap_action("Set up warehouse database for a new user")
def setup_user_database() -> None:
    """Set up warehouse database for a new user"""
    warehouse = WarehouseCompanion()
    warehouse.setup_user_db()


@click.command(help="Clear user's database (drop all tables and delete related storage objects)")
@wrap_action("Clear user's database")
def clean_user_database():
    """Clear user's database (drop all tables and delete related storage objects)"""
    # if EnvironmentConfig().is_production():
    #     logger.info("Cleaning user's database called in production environment -> Aborting.")
    #     return
    warehouse = WarehouseCompanion()
    warehouse.clean_user_database()


@click.group(help="Commands for warehouse management")
def warehouse():
    """Commands for warehouse management"""


warehouse.add_command(setup_user_database)
warehouse.add_command(clean_user_database)
