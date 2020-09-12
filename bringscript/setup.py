from setuptools import setup, find_packages


setup(
    name="bringscript",
    version="0.1.0",
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=["Jinja2"],
    package_data={"bringscript": ["templates/*/*.jinja"]},
    entry_points={"console_scripts": ["bringscript = bringscript.main:main"]},
)
