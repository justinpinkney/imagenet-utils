import click

@click.group()
def cli():
    pass

@click.command()
def search():
    click.echo("Searched")

cli.add_command(search)
