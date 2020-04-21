import os
import math

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import click


# TO DO:
# Replace arrays with numpy arrays, speeds up the creation of avg_cov_data
# Extras
# Include read file from zip format
# Check that regions hit are unique.

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


class CovData:
    '''Class to hold coverage data extracted'''

    def __init__(self, input_file, out_path, bins):
        '''Initialize coverage data object'''
        self.input_file = input_file
        self.out_path = out_path
        self.entry_counter = int()
        self.cov_counter = float()
        self.avg_cov = float()
        self.cov_idx = int()
        self.cov_data = [] # replace arrays with numpy arrays, speeds up the creation of avg_cov_data
        self.avg_cov_data = [] # replace arrays with numpy arrays, speeds up the creation of avg_cov_data
        self.df = pd.DataFrame(dtype=float)
        self.n_df = pd.DataFrame(dtype=float)
        self.bins = bins

    def cov_file_parser(self):
        '''Parse coverage data, return pandas of regular and normalized data'''
        for line in self.input_file:
            tmp_line = line.lower().split('\t')
            if '#' in line:
                check_header(line)
                self.cov_idx = tmp_line.index('meancoverage')
            elif self.cov_idx:
                try:
                    data = float(tmp_line[self.cov_idx])
                    self.cov_data.append(data)
                    self.entry_counter += 1
                    self.cov_counter += data
                except ValueError:
                    print(f'Row {self.entry_counter} contains string and not a number, omitting...')

        # Calculating average coverage
        self.avg_cov = self.cov_counter / self.entry_counter
        self.avg_cov_data = [number / self.avg_cov for number in self.cov_data]
        # Setting list as panda for searborn compability
        self.df = pd.DataFrame(self.cov_data, columns=['Coverage'])
        self.n_df = pd.DataFrame(self.avg_cov_data, columns=['Normalized Coverage'])

    def plot(self):
        '''Plot coverage data, red line indicates 100X coverage'''
        fig_dims = (12, 7)
        label = '100X coverage'
        fig, ax = plt.subplots(ncols=2, figsize=fig_dims)
        ax[0].set(ylabel='Frequency')
        ax[1].set(ylabel='Frequency')
        ax[0].axvline(100, color='r', label=label)
        ax[1].axvline(100 / self.avg_cov, color='r', label=label)
        handles_0, _0 = ax[0].get_legend_handles_labels()
        handles_1, _1 = ax[1].get_legend_handles_labels()
        ax[0].legend(handles=handles_0)
        ax[1].legend(handles=handles_1)
        sns.distplot(
            self.df['Coverage'],
            ax=ax[0],
            hist=True,
            kde=False,
            bins=self.bins
        )
        sns.distplot(
            self.n_df['Normalized Coverage'],
            ax=ax[1],
            hist=True,
            kde=False,
            bins=self.bins
        )
        fig.savefig(f'{self.out_path}/coverage.png')


def check_header(header):
    '''Checks header in sambamba output. Looks for "meanCoverage" in header'''
    assert 'meancoverage' in header.lower(), 'Could not find meanCoverage in \
            header, please check the file format'
    return True
