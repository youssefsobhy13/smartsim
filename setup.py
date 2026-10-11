"""Packaging for SmartSim (``python -m pip install -e .``)."""

from setuptools import find_packages, setup

setup(
    name="smartsim",
    version="1.0.0",
    description="Integrated educational simulation platform (BAS221, Sphinx University)",
    python_requires=">=3.9",
    packages=find_packages(include=["config*", "core*", "module*", "tests*"]),
    py_modules=["main"],
    install_requires=["numpy>=1.21.0", "scipy>=1.7.0", "matplotlib>=3.4.0"],
    extras_require={
        "full": ["plotly>=5.0.0", "pandas>=1.3.0", "simpy>=4.0.0"],
        "dev": ["pytest>=6.2.0"],
    },
    entry_points={"console_scripts": ["smartsim=main:main"]},
)
