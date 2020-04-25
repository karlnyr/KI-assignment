import click
import os

# Subcommands
from commands.scripts.process_bed import calc_summary as calcSummary, feature_overlap as featureOverlap
from commands.scripts.plot_coverage import plot_coverage as plotCoverage

cmds = {
    "calSum": {
        "calSum1": "groupBy -i <(sort -k1,1 -k2,2n -k3,3n %s) -c 1 -ops count | wc -l",
        "calSum2": "mergeBed -i <(sort -k1,1 -k2,2n %s) | awk -F '\t' '$2 ~ /^[0-9]+$/ && $3 ~ /^[0-9]+$/ {s+=$3-($2+1)} END {print s}'",
        "calSum3": "awk -F '\t' '$2 ~ /^[0-9]+$/ && $3 ~ /^[0-9]+$/ {print $4,$3-($2+1)}' %s | sort -k2,2n | tail -n 1"
    },
    "featOver": "intersectBed -wo -a $INPUT_FILE_1 -b $INPUT_FILE_2 | awk -v c=$CUTOFF -F '\t' '$NF > c {print $NF}' | wc -l"
}


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
    ctx.obj['CMDS'] = cmds


cli.add_command(calcSummary, name='calcSummary')
cli.add_command(featureOverlap, name='featureOverlap')
cli.add_command(plotCoverage, name='plotCoverage')
