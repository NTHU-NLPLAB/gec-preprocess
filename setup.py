from setuptools import setup


# with open("README.md", "r") as fh:
#     long_description = fh.read()


setup(
    name="gecpt",
    version="0.0.1",
    author="JJC",
    author_email="jjc@nlplab.cc",
    description="A toolkit for preprocessing corpus for grammatical error correction.",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/NTHU-NLPLAB/gec-preprocess",
    packages=["gecpt", "gecpt.format", "gecpt.parse"],
    install_requires=['beautifulsoup4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
    extras_require={
        'parse':  ["spacy"],
    },
    # zip_safe=False,
    python_requires='>=3.6',
)
