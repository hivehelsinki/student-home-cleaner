import os
import click

from helpers import get_students, get_homes, delete_homes

@click.command()
@click.option('--perform', is_flag=True, default=False)
def cli(perform):
    homes_list = get_homes()
    students_list = get_students()

    to_delete = list(set(homes_list) - set(students_list))

    print("Information:")
    print("\t- active students found: %d" % len(students_list))
    print("\t- homes image found: %d" % len(homes_list))
    print("\t- homes to delete: %s" % len(to_delete))
    print("\t- homes to delete: %s" % ', '.join(to_delete))

    if perform:
        if len(to_delete) > 0:
            delete_homes(to_delete)
    else:
        print("Run with the option --perform to delete those images")

    
if __name__ == "__main__":
    cli()