import setuptools

setuptools.setup(
    name="midi-orca",
    version="0.0.1",
    author="",
    author_email="georges.lebellier@sony.com",
    description="Package for converting midi files into orca sequencers.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)