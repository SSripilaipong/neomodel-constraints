import click

from neomodel_constraints.extractor import NeomodelExtractor
from neomodel_constraints.constraint import Neo4jConstraintTypeMapper
from neomodel_constraints.connection import Neo4jConnection
from neomodel_constraints.fetcher import ConstraintsFetcher


@click.group()
def main(): ...


@main.command()
@click.argument('path')
@click.option('--cypher-create-all', is_flag=True)
def extract(path, cypher_create_all):
    type_mapper = Neo4jConstraintTypeMapper()

    extractor = NeomodelExtractor(path, type_mapper)
    constraints = extractor.extract()
    if cypher_create_all:
        click.echo(';\n'.join(constraints.get_create_commands())+';')
    else:
        click.echo('\n'.join(list(map(str, constraints))))


@main.command()
@click.argument('uri')
@click.option('--username', required=True)
@click.option('--password', required=True, prompt=True, hide_input=True)
@click.option('--db', default=None)
@click.option('--cypher-drop-all', is_flag=True)
def fetch(uri, username, password, db, cypher_drop_all):
    type_mapper = Neo4jConstraintTypeMapper()
    with Neo4jConnection(uri, username, password, db=db) as connection:
        fetcher = ConstraintsFetcher(connection, type_mapper)
        constraints = fetcher.fetch()
    if cypher_drop_all:
        click.echo(';\n'.join(constraints.get_drop_commands())+';')
    else:
        click.echo('\n'.join(list(map(str, constraints))))


main.add_command(fetch, 'fetch')
main.add_command(extract, 'extract')


if __name__ == '__main__':
    main()
