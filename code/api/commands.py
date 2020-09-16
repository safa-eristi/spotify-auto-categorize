# -*- coding: utf-8 -*-

import click

from flask.cli import with_appcontext

from api import db


@click.command()
@with_appcontext
def initdb():
    print('Creating all resources.')
    db.create_all()


@click.command()
@with_appcontext
def dropdb():
    if input('Are you sure you want to drop all tables? (y/N)\n').lower() == 'y':
        print('Dropping tables...')
        db.drop_all()


@click.command()
@with_appcontext
def resetdb():
    if input('Are you sure you want to drop all tables? (y/N)\n').lower() == 'y':
        print('Reseting tables...')
        db.drop_all()
        db.create_all()
