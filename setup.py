from setuptools import setup, find_packages

setup(
    name='pydep',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'rich',
        'semver',
    ],
    entry_points={
        'console_scripts': [
            'python-npm=src.cli:main',
        ],
    },
    # Metadata
    author='Sidi Chang',
    author_email='schang@blossomcapital.org',
    description='A Python NodeJS dependency manager inspired by NPM',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/schang03-boop/python-npm',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)