#!/usr/bin/env python3
"""
Setup script for Goliath Quantum
Neuromorphic Quantum Base Architecture for advanced AI systems
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Goliath Quantum - Neuromorphic Quantum Base Architecture"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="goliath-quantum",
    version="0.1.0",
    author="Goliath Britton",
    author_email="goliath@goliathquantum.com",
    description="Neuromorphic Quantum Base Architecture for advanced AI systems",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/GoliathBritton/goliath-quantum-starter",
    project_urls={
        "Bug Reports": "https://github.com/GoliathBritton/goliath-quantum-starter/issues",
        "Source": "https://github.com/GoliathBritton/goliath-quantum-starter",
        "Documentation": "https://github.com/GoliathBritton/goliath-quantum-starter/docs",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "voice": [
            "speechrecognition>=3.10.0",
            "pyaudio>=0.2.11",
        ],
        "web": [
            "fastapi>=0.100.0",
            "uvicorn>=0.22.0",
        ],
        "database": [
            "sqlalchemy>=2.0.0",
            "alembic>=1.11.0",
        ],
        "queue": [
            "redis>=4.5.0",
            "celery>=5.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "goliath-quantum=goliath_quantum.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "goliath_quantum": [
            "config/*.json",
            "config/*.yaml",
            "config/*.yml",
        ],
    },
    keywords=[
        "quantum",
        "computing",
        "ai",
        "artificial-intelligence",
        "machine-learning",
        "neuromorphic",
        "dynex",
        "blockchain",
        "cryptography",
    ],
    zip_safe=False,
)
