import click

import subprocess as sp

from option_classes import OptionEatAll
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
def feature_overlap(cutoff, input_files):
    results = []
    for p in combinations(input_files, 2):
        result = sp.run(['./bash_commands.sh', 'feature_overlap', p[0], p[1], str(cutoff)],
                        stdout=sp.PIPE).stdout.decode('utf-8').strip().split('\n')
        results.append(result)
    for item in results:
        print(item)
