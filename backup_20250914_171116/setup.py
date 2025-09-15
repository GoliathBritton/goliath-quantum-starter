#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Setup Script

This script sets up the FLYFOX AI Quantum Computing Platform with all necessary
components, dependencies, and configurations.
"""

from setuptools import setup, find_packages
import os
import sys
from pathlib import Path

# Read the README file
def read_readme():
    """Read README file"""
    readme_path = Path(__file__).parent / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "FLYFOX AI Quantum Computing Platform"

# Read requirements
def read_requirements():
    """Read requirements from requirements.txt"""
    requirements_path = Path(__file__).parent / "requirements.txt"
    if requirements_path.exists():
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

# Package information
PACKAGE_NAME = "flyfox-quantum-platform"
PACKAGE_VERSION = "0.1.0"
PACKAGE_DESCRIPTION = "FLYFOX AI Quantum Computing Platform - Advanced quantum computing with AI agents"
PACKAGE_AUTHOR = "FLYFOX AI"
PACKAGE_AUTHOR_EMAIL = "contact@flyfox.ai"
PACKAGE_URL = "https://github.com/FLYFOX-AI/flyfox-quantum-platform"
PACKAGE_LICENSE = "MIT"

# Package classifiers
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: System :: Distributed Computing",
]

# Package keywords
KEYWORDS = [
    "quantum computing",
    "artificial intelligence",
    "machine learning",
    "optimization",
    "quantum algorithms",
    "quantum machine learning",
    "quantum optimization",
    "AI agents",
    "chatbot",
    "voice processing",
    "digital human",
    "FLYFOX AI",
    "Dynex",
    "NQBA",
]

# Setup configuration
setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description=PACKAGE_DESCRIPTION,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author=PACKAGE_AUTHOR,
    author_email=PACKAGE_AUTHOR_EMAIL,
    url=PACKAGE_URL,
    license=PACKAGE_LICENSE,
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.0",
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "voice": [
            "speech-recognition>=3.10.0",
            "pyttsx3>=2.90",
            "pyaudio>=0.2.11",
        ],
        "full": [
            "qiskit[all]>=0.44.0",
            "torch>=2.0.0",
            "transformers>=4.30.0",
            "openai>=1.0.0",
            "anthropic>=0.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "flyfox-quantum=cli:cli",
            "flyfox-demo=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.json", "*.md", "*.txt"],
    },
    zip_safe=False,
    project_urls={
        "Bug Reports": f"{PACKAGE_URL}/issues",
        "Source": PACKAGE_URL,
        "Documentation": f"{PACKAGE_URL}/docs",
        "Changelog": f"{PACKAGE_URL}/blob/main/CHANGELOG.md",
    },
)

if __name__ == "__main__":
    # Additional setup steps
    print("FLYFOX AI Quantum Computing Platform Setup")
    print("=" * 50)
    
    # Create necessary directories
    directories = [
        "logs",
        "config",
        "data",
        "models",
        "temp",
        "docs",
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create default configuration if it doesn't exist
    config_file = Path("config/config.yaml")
    if not config_file.exists():
        default_config = """# FLYFOX AI Quantum Computing Platform Configuration
# Default configuration file

quantum:
  max_qubits: 32
  backend: "qiskit"
  optimization_level: 2
  enable_apollo_mode: true
  enable_hybrid: true

dynex:
  api_key: ""
  network: "mainnet"
  enable_pouw: true
  green_credits: true
  submission_interval: 300

nqba:
  execution_mode: "simulator"
  max_parallel_jobs: 4
  timeout: 300
  enable_optimization: true
  cache_results: true

agent:
  enable_voice: false
  enable_chatbot: true
  enable_digital_human: false
  language_model: "gpt-3.5-turbo"
  max_tokens: 1000

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file_path: null
  enable_console: true
"""
        with open(config_file, "w") as f:
            f.write(default_config)
        print(f"Created default configuration: {config_file}")
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -e .")
    print("2. Configure your API keys in config/config.yaml")
    print("3. Run the demo: python main.py")
    print("4. Use the CLI: flyfox-quantum --help")
