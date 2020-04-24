import click
import os

# Subcommands
from commands.scripts.process_bed import calc_summary as calcSummary, feature_overlap as featureOverlap
from commands.scripts.plot_coverage import plot_coverage as plotCoverage


dir_path = os.path.dirname(os.path.realpath(__file__))
bash_path = os.path.join(dir_path, 'scripts/bash_commands.sh')
# Ugly solution for current bas command issue
hard_path = '/home/travis/build/karlnyr/KI-assignment/commands/scripts/bash_commands.sh'


@click.group()
@click.option(
    '--debug',
    is_flag=True,
    help='Run in test mode, will not create files')
@click.pass_context
def cli(ctx, debug):
    "ki-assignment"
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug
    if debug:
        ctx.obj['bash_path'] = hard_path
    else:
        ctx.obj['bash_path'] = bash_path


cli.add_command(calcSummary, name='calcSummary')
cli.add_command(featureOverlap, name='featureOverlap')
cli.add_command(plotCoverage, name='plotCoverage')
