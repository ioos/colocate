from setuptools import setup

reqs = [line.strip() for line in open('requirements.txt')]

def readme():
    with open('README.md') as f:
        return f.read()

kwargs = {
    'name': 'colocate',
    'author': 'OHW 2019 Team Co-Locators!!!',
    'author_email': 'noreply@co-locators-ohw19.org',
    'url': 'https://github.com/ioos/colocate',
    'description': 'A utility for aggregating co-located ERDDAP datasets in space and time. Originally developed during OceanHackWeek 2019 and migrated to U.S. IOOS for maintenance and further development.',
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
