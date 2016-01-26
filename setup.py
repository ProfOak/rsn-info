from setuptools import find_packages, setup

setup(
    name="rsn-info",
    version="1.0",
    description="Library to read SNES RSN/SPC files",
    install_requires=[
        "rarfile==4.0",
    ],
)
