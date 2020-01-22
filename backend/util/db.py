## @package backend.util.db
#  @author Sebastian Steinmeyer
#  Handles the functionality for the database access
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

## Get the database.
#  @return the database object
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )
    return g.db

## Close the database.
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

## Initiates the database with the schema file.
def init_db():
    db = get_db()
    with current_app.open_resource('sql_scripts/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

## Defines the flask command for initializing the database.
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized and cleared the database.')

## Adds some sample data from the sample.sql file into the database.
def sample_db():
    db = get_db()
    with current_app.open_resource('sql_scripts/sample.sql') as f:
        db.executescript(f.read().decode('utf8'))

## Defines the flask command for adding sample data into the database.
@click.command('sample-db')
@with_appcontext
def sample_db_command():
    sample_db()
    click.echo('Inserted sample data into database.')

## Adds the commands and close context to the given app.
#  @param app the app to register the commands in
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(sample_db_command)