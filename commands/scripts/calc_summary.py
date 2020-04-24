import click
import os
import subprocess as sp

# from commands.base import cli
from commands.opts.option_classes import OptionEatAll

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    '-i',
    '--input-files',
    cls=OptionEatAll,
    help='Specify input, same BED-format, file(s). Accepts wildcard "*"')
@click.pass_context
def calc_summary(ctx, input_files):
    '''Compose a report for input files, of BED format.\n
    Report for file:\n
    - # of features\n
    - Tot # non-overlapping bases covered by features\n
    - Longest feature in file'''
    results = []
    for file in input_files:
        result = sp.run([ctx.obj['bash_path'], 'calc_summary', file],
                        stdout=sp.PIPE).stdout.decode('utf-8').strip().split('\n')
        results.append(result)

    for file, result in zip(input_files, results):
        click.echo(
            f'Report for file: {file}\n'
            f'# of features: {result[0]}\n'
            f'Tot # non-overlapping bases covered by features: {result[1]}\n'
            f'Longest feature: {result[2]}\n'
        )
