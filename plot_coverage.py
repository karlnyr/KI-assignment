import os
import math
import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import click

# Extras
# Include read file from zip format


class CovData:
    '''Class to hold coverage data extracted'''

    def __init__(self, input_file, out_path, bins):
        '''Initialize coverage data object'''
        self.input_file = input_file
        self.out_path = out_path
        self.df = ''
        self.n_df = ''
        self.avg_cov = float()
        self.bins = bins
        self.columns = ['meanCoverage']

    def cov_file_parser(self):
        '''Parse coverage data, return pandas of regular and normalized data'''
        try:
            self.df = pd.read_csv(
                self.input_file,
                delimiter='\t',
                header=0,
                usecols=self.columns
            )
        except ValueError as e:
            sys.exit(e)

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
        fig.savefig(f'{self.out_path}/coverage.png')


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    '-i',
    '--input-file',
    type=click.File(mode='r'),
    help='Input coverage file from the software sambamba depth \
                (https://lomereiter.github.io/sambamba/)')
@click.option(
    '-o',
    '--out-path',
    default=os.getcwd(),
    type=click.Path(exists=True),
    help='Specify out directory path, default = current directory.')
@click.option(
    '-bins',
    type=click.INT,
    default=50,
    help='Specify size of bins for histogram, default=50\n NOTE: Increasing \
        number drastically will increase computation time')
def plot_coverage(input_file, out_path, bins):
    '''Plots both normalized and non-normalized coverage data gathered from
    sambamba depth. Red line in output indicates 100X coverage.'''
    coverage_data = CovData(input_file, out_path, bins)
    coverage_data.cov_file_parser()
    coverage_data.plot()
