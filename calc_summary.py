import click

import subprocess as sp

from option_classes import OptionEatAll


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    '-i',
    '--input-files',
    cls=OptionEatAll,
    help='Specify input, same BED-format, file(s). Accepts wildcard "*"')
def calc_summary(input_files):
    '''Input files of similar BED format, will allow for multiple files'''
    results = []
    for file in input_files:
        result = sp.run(['./bash_commands.sh', 'calc_summary', file],
                        stdout=sp.PIPE).stdout.decode('utf-8').strip().split('\n')
        results.append(result)

    for file, result in zip(input_files, results):
        print(
            f'Report for file: {file}\n'
            f'# of features: {result[0]}\n'
            f'Tot # non-overlapping bases covered by features: {result[1]}\n'
            f'Longest feature: {result[2]}\n'
        )
