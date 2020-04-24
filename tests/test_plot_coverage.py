import pytest
import click

from commands.scripts.plot_coverage import plot_coverage
from click import ClickException
from click.testing import CliRunner


@pytest.fixture
def runner():
    runner = CliRunner()
    return runner


def test_dryrun_plot_coverage(runner):
    results = runner.invoke(
        plot_coverage,
        '-i tests/plot_coverage/happy_file.cov --dryrun')

    assert 'Successfully ran plot_coverage!' in results.output
    assert results.exit_code == 0


def test_wrong_header(runner):
    results = runner.invoke(
        plot_coverage,
        '-i tests/plot_coverage/sad_file.cov --dryrun',
        catch_exceptions=True)

    assert results.exit_code == 1
    assert isinstance(results.exception, ValueError)


def test_option_variables(runner):
    bad_configs = {'path': 'phony/path/', 'bins': 'string'}
    good_configs = {'path': 'tests/plot_coverage/happy_file.cov', 'bins': 100}

    bad_path = runner.invoke(
        plot_coverage,
        f"-i {bad_configs['path']} --bins {good_configs['bins']} --dryrun")

    # UsageErrors, dye to bad option, returns exit code 2
    assert bad_path.exit_code == 2

    bad_bins = runner.invoke(
        plot_coverage,
        f"-i {good_configs['path']} --bins {bad_configs['bins']} --dryrun")

    # UsageErrors, due to bad option, returns exit code 2
    assert bad_bins.exit_code == 2
