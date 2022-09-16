#!/usr/bin/env python
from setuptools import setup


with open("README.md", "r") as readme_file:
    readme = readme_file.read()


requirements = ["cfn-guard-rs>=0.1.2", "colorama>=0.4.1", "Jinja2==2.11.3", "markupsafe==2.0.1", ]

setup(
    name="resource-schema-guard-rail",
    version="0.0.1",
    author="Anton Mokhovikov",
    author_email="ammokhov@amazon.com",
    description="Schema Guard Rail",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ammokhov/resource-schema-guard-rail/",
    packages=["rpdk.guard_rail"],
    package_dir={'':'src'},
    install_requires=requirements,
    python_requires=">=3.7",
    
    entry_points={
        "console_scripts": ["guard-rail-cli = guard_rail:main", "guard-rail = guard_rail:main"]
    },
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)