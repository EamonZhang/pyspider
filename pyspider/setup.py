from setuptools import setup, find_packages

setup(
    name='pyspider',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = pyspider.settings']},
)