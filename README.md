# KI-assignment
Assignments for job application at KI.

Tested on Ubuntu xenial distribution.

For easiest install, create virtual environment (conda, venv etc) for python 3.6
```shell
# Example install
$ conda create -n kia python=3.6
$ conda activate kia

# Retrieve application
$ git clone https://github.com/karlnyr/KI-assignment.git
$ cd KI-assignment
$ pip install .
$ kia
Usage: kia [OPTIONS] COMMAND [ARGS]...

  ki-assignment

Options:
  --debug  Run in test mode, will not create files
  --help   Show this message and exit.

Commands:
  calcSummary     Compose a report for input files, of BED format.
  featureOverlap  Calculates the number of overlapping sequences in BED...
  plotCoverage    Plots both normalized and non-normalized coverage data...
```

Kia include three different commands, and are easily accessed like so:

```shell
$ kia plotCoverage
Usage: kia plotCoverage [OPTIONS]

  Plots both normalized and non-normalized coverage data gathered from
  sambamba depth. Red line in output indicates 100X coverage.

Options:
  -i, --input-file PATH  Input coverage file from the software sambamba depth
                         (https://lomereiter.github.io/sambamba/)

  -o, --out-path PATH    Specify out directory path, default = current
                         directory.

  -p, --prefix TEXT      Specify prefix on output, default = file_name
  --bins INTEGER         Specify size of bins for histogram, default=50 NOTE:
                         Increasing         number drastically will increase
                         computation time

  --dryrun               Will test functionality of plot_coverage, will not
                         save a figure in the end

  -h, --help             Show this message and exit.
```
