from setuptools import setup, find_packages

setup(
    name="civic-site",
    packages=find_packages(),
    install_requires=['Flask'],
    entry_points={'console_scripts': ['civic-site = civic_site:main']},
)
