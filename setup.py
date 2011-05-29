from setuptools import setup, find_packages

setup(
    name="civic-site",
    packages=find_packages(),
    install_requires=[
        'Flask',
        'sparql-client',
        'Products.ZSPARQLMethod',
        'flup',
    ],
    entry_points={'console_scripts': ['civic-site = civic_site:main']},
)
