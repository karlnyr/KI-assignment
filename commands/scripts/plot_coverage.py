import os
import click

import subprocess as sp
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as lines


class CovData:
    '''Class to hold coverage data extracted'''

    def __init__(self, input_file, out_path, bins, prefix, dryrun):
        '''Initialize coverage data object'''
        self.input_file = input_file
        if prefix == '':
            self.prefix = sp.run(
                ['basename', input_file],
                stdout=sp.PIPE).stdout.decode('utf-8').strip()
        else:
            self.prefix = prefix
        self.out_path = out_path
        self.df = ''
        self.n_df = ''
        self.avg_cov = float()
        self.bins = bins
        self.columns = ['meanCoverage']
        self.dryrun = dryrun

    def cov_file_parser(self):
        '''Parse coverage data, set pandas of regular and normalized data'''
        try:
            self.df = pd.read_csv(
                self.input_file,
                delimiter='\t',
                header=0,
                usecols=self.columns
            )
        except ValueError as ve:
            raise ValueError(ve)
       # For clarity, creating a normalized data frame for plotting
        self.avg_cov = self.df[self.columns[0]].sum() / self.df.shape[0]
        self.n_df = pd.DataFrame(self.df[self.columns[0]].divide(self.avg_cov), columns=['meanCoverage'])

    def plot(self):
        '''Plot coverage data, red line indicates 100X coverage'''
        fig_dims = (12, 7)
        label = '100X coverage'
        fig, ax = plt.subplots(ncols=2, figsize=fig_dims)
        ax[0].axvline(100, color='r', label=label)
        ax[1].axvline(100 / self.avg_cov, color='r', label=label)
        for axs in ax:
            axs.set(ylabel='Frequency')
            handles, _ = axs.get_legend_handles_labels()
            axs.legend(handles=handles)
        sns.distplot(
            self.df['meanCoverage'],
            ax=ax[0],
            hist=True,
            kde=False,
            bins=self.bins
        )
        sns.distplot(
            self.n_df['meanCoverage'],
            ax=ax[1],
            hist=True,
            kde=False,
            bins=self.bins
        )
        ax[0].set_xlabel('Coverage')
        ax[1].set_xlabel('Normalized Coverage')
        if not self.dryrun:
            fig.savefig(f'{self.out_path}/{self.prefix}_coverage.png')


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    '-i',
    '--input-file',
    type=click.Path(exists=True),  # Using path instead of File due to codecs skipping byte
    help='Input coverage file from the software sambamba depth \
                (https://lomereiter.github.io/sambamba/)')
@click.option(
    '-o',
    '--out-path',
    default=os.getcwd(),
    type=click.Path(exists=True),
    help='Specify out directory path, default = current directory.')
@click.option(
    '-p',
    '--prefix',
    default='',
    type=click.STRING,
    help='Specify prefix on output, default = file_name')
@click.option(
    '--bins',
    type=click.INT,
    default=50,
    help='Specify size of bins for histogram, default=50\n NOTE: Increasing \
        number drastically will increase computation time')
@click.option(
    '--dryrun',
    is_flag=True,
    help='Will test functionality of plot_coverage, will not save a figure in the end')
@click.pass_context
def plot_coverage(ctx, input_file, out_path, bins, prefix, dryrun):
    '''Plots both normalized and non-normalized coverage data gathered from
    sambamba depth. Red line in output indicates 100X coverage.'''
    coverage_data = CovData(input_file, out_path, bins, prefix, dryrun)
    coverage_data.cov_file_parser()
    coverage_data.plot()
    if coverage_data.dryrun:
        print('Successfully ran plot_coverage!')
