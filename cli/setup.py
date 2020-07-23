from setuptools import setup


setup(
    name="ShrinkImageCli",
    version="0.1",
    scripts=["shrink_image.py"],
    install_requires=["Pillow"],
    entry_points={"console_scripts": ["shrinki = shrink_image:main"]},
)
