"""Setup script for dispatch-core library."""

from setuptools import find_packages, setup

setup(
    name="dispatch_core",  # Use underscores for Python module name
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.12",
    install_requires=[
        "pydantic>=2.12.0",
        "attrs>=22.2.0",
    ],
)
