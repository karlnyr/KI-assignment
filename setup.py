from setuptools import setup


setup(
    name='ki-assignment',
    version='1.0',
    py_modules=[
            'plot_coverage',
            'feature_overlap',
            'calc_summary',
    ],
    install_requires=[
        'Click',
        'seaborn',
        'pandas',
        ],
    entry_points='''
            [console_scripts]
            plot_coverage=plot_coverage:plot_coverage
            feature_overlap=feature_overlap:feature_overlap
            calc_summary=calc_summary:calc_summary
        ''',
)
