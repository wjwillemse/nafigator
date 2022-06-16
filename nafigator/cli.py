# -*- coding: utf-8 -*-

"""Cli module.

Console script for nafigator.

"""


import sys
import click
import os
import logging
from nafigator import parse2naf


@click.command()
@click.option(
    "--input", default="data/example.pdf", prompt="input file", help="The input file"
)
@click.option(
    "--output",
    default="data/example.naf.xml",
    prompt="output file",
    help="The output file",
)
@click.option(
    "--engine",
    default="stanza",
    prompt="NLP-package",
    help="The package to parse the text",
)
@click.option(
    "--language", default="en", prompt="language", help="The language of the input file"
)
@click.option(
    "--naf_version",
    default="v3.1",
    prompt="naf version",
    help="NAF version to convert to",
)
@click.option(
    "--dtd_validation",
    default=False,
    prompt="dtd validation",
    help="Validate the NAF dtd",
)
def main(
    input: str,
    output: str,
    engine: str,
    language: str,
    naf_version: str,
    dtd_validation: bool,
) -> int:
    """Command line interface function to generate and write NAF file

    Args:
        input: location of the document file to be converted
        output: location of the NAF file
        engine: name of the NLP processor
        language: language of the document file
        naf_version: naf version to be used
        dtd_validation: if True then the NAF file will be validated

    Returns:
        int: The return value. 0 for success

    """

    log_file: str = os.path.splitext(input)[0] + ".log"
    logging.basicConfig(filename=log_file, level=logging.INFO, filemode="w")
    tree = parse2naf.generate_naf(
        input=input,
        engine=engine,
        language=language,
        naf_version=naf_version,
        dtd_validation=dtd_validation,
    )
    if tree is not None:
        tree.write(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
