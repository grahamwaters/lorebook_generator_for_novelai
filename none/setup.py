#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click>=7.0",
]

test_requirements = []

setup(
    author="Graham G. Waters",
    author_email="graham.waters.business@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="This repo is designed to help all of us as authors using NovelAI. It pulls from Wikipedia articles to automatically generate lorebooks for real places or years and pretty much anything you could find on Wikipedia using python's wikipedia library. The repo contains two different versions: a basic one that generates based on a CSV file, 'characters.csv' and a more advanced version that implements multiple keywords for a more tailored search.",
    entry_points={
        "console_scripts": [
            "none=none.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="none",
    name="none",
    packages=find_packages(include=["none", "none.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/grahamwaters/none",
    version="0.1.0",
    zip_safe=False,
)
