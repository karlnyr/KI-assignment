import click
import os

# import subprocess as sp
from subprocess import run, PIPE


from commands.opts.option_classes import OptionEatAll
from itertools import combinations


@click.command(no_args_is_help=True)
@click.option(
    '-i',
    '--input-files',
    cls=OptionEatAll,
    help='Specify input, same BED-format, file(s). Accepts wildcard "*"')
@click.pass_context
def calc_summary(ctx, input_files):
    '''Compose a report for input files, of BED format.

    Report for file: # of features, Tot # non-overlapping bases covered by
    features, Longest feature in file.

    Input files are expected to be formated such as:
    chromosome​ start  end​    name​, and have more than 1 entry'''
    for file in input_files:
        try:
            with open(file, 'r'):
                pass
        except FileNotFoundError as e:
            click.echo(f'{e}')
            raise
        try:
            for file in input_files:
                assert check_format(file)
        except AssertionError as e:
            click.echo(f'\n{file} is badly formatted\n')
            raise

    results = []
    for file in input_files:
        result = run(
            [ctx.obj['bash_path'], 'calc_summary', file],
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True).stdout.strip().split('\n')
        results.append(result)

    for file, result in zip(input_files, results):
        click.echo(
            f'Report for file: {file}\n'
            f'# of features: {result[0]}\n'
            f'Tot # non-overlapping bases covered by features: {result[1]}\n'
            f'Longest feature: {result[2]}'
        )


@click.command(no_args_is_help=True)
@click.option(
    '-c',
    '--cutoff',
    type=click.INT,
    default=1,
    help='Set the minimum number overlap between features, default = 0')
@click.option(
    '-i',
    '--input-files',
    cls=OptionEatAll,
    help='Specify input, same BED-format, file(s). Accepts wildcard "*"')
@click.pass_context
def feature_overlap(ctx, cutoff, input_files):
    '''Calculates the number of overlapping sequences in BED files. Accepts
    more than two files, will calculate overlaps between all possible
    combinations. Input files are expected to be formated such as:
    chromosome\tstart\tend​\tname​, and have more than 1 entry'''
    for file in input_files:
        try:
            with open(file, 'r'):
                pass
        except FileNotFoundError as e:
            click.echo(f'{e}')

    try:
        assert len(input_files) > 1
    except AssertionError as e:
        e.args += ('\nNot enough files handed\n')
        # click.echo('\nNot enough files handed\n')
        raise

    try:
        for file in input_files:
            assert check_format(file)
    except AssertionError as e:
        e.args += (f'\n{file} is badly formatted\n')
        raise

    results = []
    for p in combinations(input_files, 2):
        result = run(
            [ctx.obj['bash_path'], 'feature_overlap', p[0], p[1], str(cutoff)],
            stdout=PIPE,
            stderr=PIPE,
            universal_newlines=True)
        results.append(result.stdout)

    for comp, result in zip(combinations(input_files, 2), results):
        click.echo(
            f'Searching overlapping features in: {comp[0]}, {comp[1]}\n'
            f'# overlapping features (min overlap={cutoff}): {result}')


def check_format(file):
    '''check if input file is remotely correct format. Bedtools sends error for
    faulty formatted files, but will allow for missing data required here'''
    try:
        with open(file, 'r') as fh:
            lines = next(fh)
            pass
    except StopIteration:
        return False
    try:
        lines = []
        with open(file, 'r') as fh:
            lines.append(next(fh).strip().split('\t'))
            lines.append(next(fh).strip().split('\t'))
        length = [len(x) == 4 for x in lines]
        # If one is header, this is okay
        assert any(length)
        # The second one must be true
        assert (length[1])
        # Start and end are integers
        assert int(lines[1][1])
        assert int(lines[1][2])
    except AssertionError as e:
        print(e)
        return False
    return True
