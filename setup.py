from setuptools import setup

reqs = [line.strip() for line in open('requirements.txt')]

def readme():
    with open('README.md') as f:
        return f.read()

kwargs = {
    'name': 'co-locate',
    'author': 'OHW 2019 Team Co-Locators!!!',
    'author_email': 'ohw@ohw.org',
    'url': 'https://github.com/oceanhackweek/ohw19-project-co_locators',
    'description': 'A utility for aggregating co-located ERDDAP datasets in space and time and \
        doing some cool stuff',
    'long_description': 'readme()',
    'entry_points': {
        'console_scripts': [
            'erddap-co-locate=colocate.run:main',
        ]
    },
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS'
    ],
    'packages': ['colocate'],
    'package_data': {

    },
    'version': '0.1.0',
}

kwargs['install_requires'] = reqs

setup(**kwargs)
