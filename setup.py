"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Freenove_SmartCar',
    version='1.0.0',
    description='Freenove SmartCar',
    long_description=long_description,
    url='https://github.com/Freenove/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi',
    author='Freenove',
    author_email='sales@free=nove.com',
    license='GNU',
    zip_safe=False,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU License',

        'Programming Language :: Python :: 3',
    ],

    keywords='freenove raspberry pi robot car',
    packages=find_packages(exclude=['docs', 'tests*']),

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'smartcar=smartcar:main',
        ],
    },
)
