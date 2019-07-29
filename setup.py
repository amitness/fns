from setuptools import setup, find_packages

setup(
    name='fns',
    version='0.0.4',
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
    install_requires=['numpy'],
    packages=find_packages(),
)
