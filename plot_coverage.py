import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import click


# TO DO:
# Make file parser into a function
# Make plotting into a function
# Create a class for the parsed data, plot function on top of that.
# Extras
# Include read file from zip format
# Check that regions hit are unique.

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS, no_args_is_help=True)
@click.option(
    '-i',
    '--input-file',
    type=click.Path(exists=True),
    help='Input coverage file from the software sambamba depth (https://lomereiter.github.io/sambamba/)'
)
@click.option('-o',
              '--out-path',
              default=os.getcwd(),
              help='Specify out directory path, default = current directory.')
def plot_coverage(input_file, out_path):
    '''Plots both normalized and non-normalized coverage data gathered from
    sambamba depth. Red line in output indicates 100X coverage.'''
    coverage_data = CovData(input_file, out_path)
    coverage_data.cov_file_parser()
    coverage_data.plot()


class CovData:
    '''Class to hold coverage data extracted'''

    def __init__(self, input_file, out_path):
        '''Initialize coverage data object'''
        self.input_file = input_file
        self.out_path = out_path
        self.entry_counter = int()
        self.cov_counter = float()
        self.avg_cov = float()
        self.cov_idx = int()
        self.cov_data = []
        self.avg_cov_data = []
        self.df = pd.DataFrame(dtype=float)
        self.n_df = pd.DataFrame(dtype=float)

    def cov_file_parser(self):
        '''Parse coverage data, return pandas of regular and normalized data'''
        with open(self.input_file, 'r') as fh:
            for line in fh:
                tmp_line = line.split('\t')
                # Implement test for file format:
                # Check if meanCoverage is present
                # Add try for possible faulty values in meanCoverage column
                if '#' in line:
                    self.cov_idx = tmp_line.index('meanCoverage')
                elif self.cov_idx:
                    self.cov_data.append(float(tmp_line[self.cov_idx]))
                #     self.df.append({'Coverage': float(tmp_line[self.cov_idx])}, ignore_index=True)
                    self.entry_counter += 1
                    self.cov_counter += float(tmp_line[self.cov_idx])
            # Calculating average coverage
            self.avg_cov = self.cov_counter / self.entry_counter
            self.avg_cov_data = [number / self.avg_cov for number in self.cov_data]
        # Setting list as panda for searborn compability
        self.df = pd.DataFrame(self.cov_data, columns=['Coverage'])
        self.cov_data = ''  # Free space
        self.n_df = pd.DataFrame(self.avg_cov_data, columns=['Normalized Coverage'])
        self.avg_cov_data = ''  # Free space

    def plot(self):
        '''Plot coverage data, red line indicates 100X coverage'''
        fig_dims = (12, 7)
        fig, ax = plt.subplots(ncols=2, figsize=fig_dims)
        ax[0].set(ylabel='Frequency')
        ax[1].set(ylabel='Frequency')
        ax[0].axvline(100, color='r')
        ax[1].axvline(100 / self.avg_cov, color='r')
        sns.distplot(
            self.df['Coverage'],
            ax=ax[0],
            hist=True,
            kde=False,
            bins=int(280 / 5)
        )
        sns.distplot(
            self.n_df['Normalized Coverage'],
            ax=ax[1],
            hist=True,
            kde=False,
            bins=int(280 / 5)
        )
        fig.savefig(f'{self.out_path}/coverage.png')


if __name__ == '__main__':
    plot_coverage()
