"""Setup script for dispatch-database library."""

from setuptools import find_packages, setup

setup(
    name="dispatch_database",  # Use underscores for Python module name
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.12",
    install_requires=[
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0",
        "psycopg2-binary>=2.9.0",
        "sqlalchemy-utils>=0.41.0",
        "dispatch_core>=0.1.0",
    ],
)
