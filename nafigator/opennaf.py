# coding: utf-8

"""Main module."""

import sys
import click
from .nafdocument import NafDocument


@click.command()
@click.option(
    "--input", default="data/example.naf", prompt="input file", help="The input file"
)
def opennaf(input: str):
    """ """
    naf = NafDocument().open(input)
    print(naf.header)
    # print(naf.raw)
    print(naf.formats)
    # print(naf.text)
    print(naf.terms)
    print(naf.version)
    # print(naf.entities)
    # print(naf.deps)


if __name__ == "__main__":
    sys.exit(opennaf())
