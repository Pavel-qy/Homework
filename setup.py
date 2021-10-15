import setuptools
import rss_reader


with open("README.md", "r") as readme:
    long_description = readme.read()

requirements = [
    "argparse",
    "requests",
    "bs4",
    "lxml",
]

setuptools.setup(
    name="rss_reader",
    version=rss_reader.__version__,
    author="Pavel Stankevich",
    author_email="pavel.qy@gmail.com",
    description="Pure Python command-line RSS reader.",
    long_description=long_description,
    packages=["rss_reader"],
    install_requires=requirements,
    python_requires=">=3.9",
    entry_points={
        "console_scripts": ["rss_reader = rss_reader.rss_reader:main"]
    }
)
