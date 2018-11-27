import click
import imagenet_utils as imnet

@click.group()
def cli():
    pass

@click.command()
@click.argument('term')
@click.option('-n', '--number', type=int)
def search(term, number):
    results = imnet.search(term)
    if number and len(results) > number:
        results = results[:number]
    for result in results:
        click.echo(f"{result.wnid}: {result.words}")

@click.command()
@click.argument('wnid')
@click.option('-o', '--output-folder')
@click.option('-s', '--search', default=False, is_flag=True)
def download(wnid, output_folder=None, search=False):

    if search:
        result = imnet.search(wnid)
        wnid = result[0].wnid
        click.echo(f"Search found wnid={wnid}")

    if not output_folder:
        destination = wnid

    click.echo("downloading")
    click.echo(wnid)
    imnet.download(wnid, destination)

cli.add_command(search)
cli.add_command(download)
