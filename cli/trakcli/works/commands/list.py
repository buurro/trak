from datetime import datetime
from typing import Annotated

import typer
from rich import print as rprint
from rich.table import Table

from trakcli.projects.database import get_project_from_config, get_projects_from_config
from trakcli.works.database import get_project_works_from_config

ALL_PROJECTS = "all"


def print_project_works(works, project_id):
    """Print a table of works by project."""
    works_table = Table(title=f"Works for project {project_id}")

    works_table.add_column("Id", no_wrap=True)
    works_table.add_column("Name", no_wrap=True)
    works_table.add_column("Description")
    works_table.add_column("Time")
    works_table.add_column("Rate")
    works_table.add_column("From")
    works_table.add_column("To")

    if works is not None and len(works):
        for w in works:
            time = w.get("time", "Missin time!")
            rate = w.get("rate", "0")

            from_date = w.get("from_date", None)
            if from_date is not None:
                try:
                    from_date = datetime.fromisoformat(from_date).strftime("%Y-%m-%d")
                except ValueError:
                    rprint(
                        f"[red]Error in {w['id']}'s from_date of {project_id} project.[/red]"
                    )

            to_date = w.get("to_date", None)
            if to_date is not None:
                try:
                    to_date = datetime.fromisoformat(to_date).strftime("%Y-%m-%d")
                except ValueError:
                    rprint(
                        f"[red]Error in {w['id']}'s to_date of {project_id} project.[/red]"
                    )

            works_table.add_row(
                w.get("id", "Missing id!"),
                w.get("name", "Missing name!"),
                w.get("description", ""),
                f"{time}",
                f"{rate}",
                from_date,
                to_date,
            )

        rprint("")
        rprint(works_table)

        return


def list_works(
    project_id: Annotated[str, typer.Argument()] = ALL_PROJECTS,
):
    """List the works in a project or all of them."""

    if project_id != ALL_PROJECTS:
        details = get_project_from_config(project_id)

        # Check if project esists
        if details:
            works = get_project_works_from_config(project_id)
            print_project_works(works, project_id)

            return
    else:
        # Show all current projects
        projects = get_projects_from_config()

        for project in projects:
            works = get_project_works_from_config(project)

            if works is not None:
                print_project_works(works, project)

        return
