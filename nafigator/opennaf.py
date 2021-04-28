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
    naf = generate_naf(input)
    print(naf.header)
    # print(naf.raw)
    print(naf.formats)
    # print(naf.text)
    print(naf.terms)
    print(naf.version)
    # print(naf.entities)
    # print(naf.deps)


def generate_naf(input: str, params: dict = {}):
    """ """
    if "public" not in params.keys():
        params["public"] = dict()
    if "uri" not in params["public"].keys():
        params["public"]["uri"] = input
    return NafDocument(params)


if __name__ == "__main__":
    sys.exit(opennaf())
