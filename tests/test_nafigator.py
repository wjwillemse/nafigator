#!/usr/bin/env python

"""Tests for `stanza2naf` package."""


import unittest
from click.testing import CliRunner

from stanza2naf import stanza2naf
from stanza2naf import cli


class TestStanza2naf(unittest.TestCase):
    """Tests for `stanza2naf` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'stanza2naf.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
