from plot_coverage import CovData, check_header

test_object = CovData('input_file','output_file')

def test_check_header():
    true_header = '# this string does contain meanCoverage'
    assert check_header(true_header) == True

## TO DO:
# Add tests on cov_file_parser, simply try to parse a dummy file which we know have the right format
# Add test on plot function, simply try to plot the output of the cov_file_parser function

