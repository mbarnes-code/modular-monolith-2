#!/usr/bin/env python3

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()
                    and not line.startswith("#")]

setup(
    name="maltrail-service",
    version="0.1.0",
    author="Maltrail Development Team",
    description="Malicious traffic detection system integrated into the modular monolith platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stamparm/maltrail",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "maltrail-server=maltrail.server:main",
            "maltrail-sensor=maltrail.sensor:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.conf", "*.service", "html/**/*", "misc/**/*"],
    },
)
