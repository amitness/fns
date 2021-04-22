from setuptools import setup, find_packages

setup(
    name='fns',
    version='0.4.92',
    license='MIT',
    description='Reusable functions for use in ML projects',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    author='Amit Chaudhary',
    author_email='meamitkc@gmail.com',
    url='https://github.com/amitness/fns',
    install_requires=['numpy'],
    packages=find_packages(),
)
