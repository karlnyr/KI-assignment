from setuptools import setup


setup(
    name='ki-assignment',
    version='1.0',
    py_modules=[
            'plot_coverage',
    ],
    install_requires=[
        'Click',
        'seaborn',
        'pandas',
        'subprocess'
    ],
    entry_points='''
            [console_scripts]
            plot_coverage=plot_coverage:plot_coverage
        ''',
)
