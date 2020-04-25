import pytest
import click
import os

from click import ClickException
from click.testing import CliRunner
from commands.scripts.process_bed import check_format
from commands.base import cli as kia
# from commands.opts.option_classes import OptionEatAll


@pytest.fixture
def runner():
    runner = CliRunner()
    return runner


def test_feature_overlap(runner):
    results = runner.invoke(
        kia,
        'featureOverlap -i tests/process_bed/happy_file.bed tests/process_bed/happy_file.bed')

    assert results.exit_code == 0


def test_calc_summary(runner):
    results = runner.invoke(
        kia,
        'calcSummary -i tests/process_bed/happy_file.bed')

    assert results.exit_code == 0


def test_check_format():
    # Detect empty, missing column and faulty start end
    files = ['empty_bed.bed', 'sad_file_mc.bed', 'sad_file_se.bed']
    dir_n = 'tests/process_bed'

    for file in files:
        assert (check_format(f'{dir_n}/{file}') == False)
