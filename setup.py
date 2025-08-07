import sys
from setuptools import setup, find_packages

def read_requirements(file_path):
    """Read requirements from a file and return a list of packages."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]
    
setup(
    name="anime recommender",
    version="0.1.0",
    author="Lokesh Kummari",
    packages=find_packages(),
    install_requires=read_requirements('requirements.txt'),
)