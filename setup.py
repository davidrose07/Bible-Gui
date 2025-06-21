from setuptools import setup, find_packages

def load_requirements(filename):
    with open(filename, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
setup(
    name="bible-gui",
    version="1.0",
    description="Read the Bible in a Gui Interface",
    author="David Rose",
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements('requirements.txt'),
    entry_points={"console_scripts": ["bible-gui=src.main:main"]},
    license="MIT",
)