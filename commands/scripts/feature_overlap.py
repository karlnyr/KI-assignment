import click

import subprocess as sp

# from commands.base import cli
from commands.opts.option_classes import OptionEatAll
from itertools import combinations


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
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
    combinations'''
    results = []
    for p in combinations(input_files, 2):
        result = sp.run(['scripts/bash_commands.sh', 'feature_overlap', p[0], p[1], str(cutoff)],
                        stdout=sp.PIPE).stdout.decode('utf-8').strip()
        results.append(result)
    for comp, result in zip(combinations(input_files, 2), results):
        click.echo(
            f'Searching overlapping features in: {comp[0]}, {comp[1]}\n'
            f'# overlapping features (min overlap={cutoff}): {result}\n')
