# coding: utf-8

"""Main module."""

from datetime import datetime
import sys
import click
import logging
import os

from .nafdocument import NafDocument

@click.command()
@click.option('--input', default="data/example.naf", prompt="input file", help='The input file')

def opennaf(input: str):
    """
    """
    naf = generate_naf(input)
    print(naf.entities_layer)

def generate_naf(input: str, 
                 params: dict = {}):
    """
    """
    if 'public' not in params.keys():
        params['public'] = dict()
    if 'uri' not in params['public'].keys():
        params['public']['uri'] = input
    return NafDocument(params)


if __name__ == '__main__':
    sys.exit(opennaf())
