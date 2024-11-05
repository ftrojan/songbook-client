import click
import songbook


@click.command()
def sync():
    songbook.sync()
