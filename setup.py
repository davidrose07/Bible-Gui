from setuptools import setup, find_packages

setup(
    name="bible-gui",
    version="1.0",
    description="Read the Bible in a Gui Interface",
    author="David Rose",
    author_email="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["bible-gui=src.main:main"]},
    install_requires=[],
    license="",
)