# -*- coding: utf-8 -*-

import click

from flask.cli import with_appcontext


@click.command()
@with_appcontext
def start():
    print('Starting..')

