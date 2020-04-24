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
    print(results)
