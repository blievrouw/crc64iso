import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crc64iso",
    version="0.0.2",
    author="Bert Lievrouw",
    author_email="bert.lievrouw@gmail.com",
    description="CRC-64 checksum generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='checksum digest crc crc-64 cyclic redundancy check data integrity',
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
