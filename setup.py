"""Setup notetools"""
import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="notetools",
    version="0.0.2",
    author="johntd54",
    author_email="trungduc1992@gmail.com",
    description="Notebook utility functions",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/johntd54/notetools",
    packages=setuptools.find_packages(
        exclude=["tests.*", "tests", "*.tests", "*.tests.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    license='GNU General Public License (GPL)',
    keywords="notetools deep learning inquire artificial intelligence",
    install_requires=[
        'IPython',
        'PyDrive',
    ],
    python_requires=">=3.5"
)
