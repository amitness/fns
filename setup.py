from setuptools import setup, find_packages
from fns import __VERSION__

setup(
    name='fns',
    version=__VERSION__,
    license='MIT',
    description='Reusable functions for use in ML projects',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    author='Amit Chaudhary',
    author_email='meamitkc@gmail.com',
    url='https://github.com/amitness/fns',
    install_requires=['numpy', 'more_itertools'],
    packages=find_packages(),
)
