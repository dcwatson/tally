from setuptools import setup, find_packages
import tally

setup(
    name='tally',
    version=tally.__version__,
    description='A Django application (and daemon) for collecting, storing, and aggregating metrics.',
    author='Dan Watson',
    author_email='dcwatson@gmail.com',
    url='https://github.com/dcwatson/tally',
    license='BSD',
    packages=find_packages(exclude=[
        'tally.settings',
        'tally.tests',
    ]),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
