from setuptools import setup, find_packages

setup(name='gwa_package',
    version='0.1',
    description='Package to support People Analytics data science projects',
    # Author
    author='Kevin Metherell',
    author_email='kevindickens@gmail.com',

    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'os',
        'datetime'
    ],
    zip_safe=False)
