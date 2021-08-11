import os
import sys

import click

from neomodel_constraints.extractor import NeomodelExtractor
from neomodel_constraints.constraint import Neo4jConstraintTypeMapper
from neomodel_constraints.connection import Neo4jConnection
from neomodel_constraints.fetcher import FetcherAbstract, get_constraints_fetcher
from neomodel_constraints.manager import ConstraintManager


def get_fetcher(connection: Neo4jConnection, type_mapper: Neo4jConstraintTypeMapper) -> FetcherAbstract:
    version = connection.version()
    fetcher = get_constraints_fetcher(version)(connection, type_mapper)
    return fetcher


@click.group()
def main(): ...


@main.command()
@click.argument('path')
@click.option('--cypher-create-all', is_flag=True)
def extract(path, cypher_create_all):
    type_mapper = Neo4jConstraintTypeMapper()

    sys.path.insert(0, os.getcwd())
    extractor = NeomodelExtractor(path.lstrip('.'), type_mapper)
    constraints = extractor.extract()
    sys.path = sys.path[1:]

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
        fetcher = get_fetcher(connection, type_mapper)
        constraints = fetcher.fetch()
    if cypher_drop_all:
        click.echo(';\n'.join(constraints.get_drop_commands())+';')
    else:
        click.echo('\n'.join(list(map(str, constraints))))


@main.command()
@click.argument('path')
@click.argument('neo4j_uri')
@click.option('--username', required=True)
@click.option('--password', required=True, prompt=True, hide_input=True)
@click.option('--db', default=None)
@click.option('--dry-run', is_flag=True)
def update(path, neo4j_uri, username, password, db, dry_run):
    sys.path.insert(0, os.getcwd())

    type_mapper = Neo4jConstraintTypeMapper()
    extractor = NeomodelExtractor(path.lstrip('.'), type_mapper)

    with Neo4jConnection(neo4j_uri, username, password, db=db) as connection:
        fetcher = get_fetcher(connection, type_mapper)
        manager = ConstraintManager(extractor, [fetcher])

        update_commands = manager.get_update_commands()
        if not update_commands:
            click.echo('Already up-to-date')
        elif dry_run:
            click.echo(';\n'.join(update_commands)+';')
        else:
            for cmd in update_commands:
                click.echo('executing: ' + cmd)
                try:
                    connection.execute(cmd+';')
                    click.echo('    success')
                except Exception as e:
                    click.echo('    error: ' + str(e))

    sys.path = sys.path[1:]


main.add_command(fetch, 'fetch')
main.add_command(extract, 'extract')


if __name__ == '__main__':
    main()
