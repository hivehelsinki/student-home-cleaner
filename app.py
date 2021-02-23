#!/usr/bin/env python3 -B

import os
import click

from tools.helpers import get_students, get_homes, delete_homes
from loguru import logger


logger.add("logs/logs.log", rotation="500 MB", retention="10 days", compression="zip") 


@click.command()
@click.option('--perform', is_flag=True, default=False)
def cli(perform):
    students_list = get_students()
    homes_list = get_homes()
    to_delete = list(set(homes_list) - set(students_list))

    print(f"Information:\n\t- active students found: {len(students_list)}")
    print(f"\t- homes image found: {len(homes_list)}")
    print(f"\t- homes to delete: {len(to_delete)}")
    print(f"\t- homes to delete: {', '.join(to_delete)}")

    if perform:
        delete_homes(to_delete)
    else:
        print("Run with the option --perform to delete those images")

    
if __name__ == "__main__":
    cli()