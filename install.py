#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Installation Script

This script installs and configures the FLYFOX AI Quantum Computing Platform
with all necessary dependencies and setup steps.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import shutil
import json
import yaml

def print_banner():
    """Print installation banner"""
    print("FLYFOX AI Quantum Computing Platform")
    print("=" * 50)
    print("Advanced quantum computing with AI agents")
    print("Installing and configuring the platform...")
    print()

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print(f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is compatible")
    return True

def check_system_requirements():
    """Check system requirements"""
    print("Checking system requirements...")
    
    # Check available memory (at least 4GB recommended)
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        if memory_gb < 4:
            print(f"WARNING: Low memory detected ({memory_gb:.1f}GB)")
            print("   At least 4GB RAM is recommended for optimal performance")
        else:
            print(f"Memory: {memory_gb:.1f}GB available")
    except ImportError:
        print("Could not check memory (psutil not available)")
    
    # Check disk space (at least 2GB free)
    try:
        disk_usage = shutil.disk_usage('.')
        free_gb = disk_usage.free / (1024**3)
        if free_gb < 2:
            print(f"ERROR: Insufficient disk space: {free_gb:.1f}GB free")
            print("   At least 2GB free space is required")
            sys.exit(1)
        else:
            print(f"Disk space: {free_gb:.1f}GB free")
    except Exception as e:
        print(f"Could not check disk space: {e}")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    
    try:
        # Upgrade pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        print("Upgraded pip")
        
        # Install core dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("Installed core dependencies")
        
        # Install development dependencies
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"], 
                      check=True)
        print("Installed development dependencies")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        print(f"   Error output: {e.stderr.decode() if e.stderr else 'No error output'}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    
    directories = [
        "logs",
        "config",
        "data",
        "models",
        "temp",
        "docs",
        "tests",
        "examples",
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created: {directory}")
    
    return True

def setup_configuration():
    """Setup configuration files"""
    print("Setting up configuration...")
    
    # Create default config if it doesn't exist
    config_file = Path("config/config.yaml")
    if not config_file.exists():
        default_config = {
            "quantum": {
                "max_qubits": 32,
                "backend": "qiskit",
                "optimization_level": 2,
                "enable_apollo_mode": True,
                "enable_hybrid": True
            },
            "dynex": {
                "api_key": "",
                "network": "mainnet",
                "enable_pouw": True,
                "green_credits": True,
                "submission_interval": 300
            },
            "nqba": {
                "execution_mode": "simulator",
                "max_parallel_jobs": 4,
                "timeout": 300,
                "enable_optimization": True,
                "cache_results": True
            },
            "agent": {
                "enable_voice": False,
                "enable_chatbot": True,
                "enable_digital_human": False,
                "language_model": "gpt-3.5-turbo",
                "max_tokens": 1000
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file_path": "logs/flyfox_quantum.log",
                "enable_console": True
            }
        }
        
        with open(config_file, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False, indent=2)
        print(f"Created: {config_file}")
    
    # Create environment template
    env_template = Path(".env.template")
    if not env_template.exists():
        env_content = """# FLYFOX AI Quantum Computing Platform Environment Variables
# Copy this file to .env and fill in your API keys

# Quantum Computing
QUANTUM_MAX_QUBITS=32
QUANTUM_BACKEND=qiskit
QUANTUM_OPTIMIZATION_LEVEL=2

# Dynex Integration
DYNEX_API_KEY=your_dynex_api_key_here
DYNEX_NETWORK=mainnet

# AI Services
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/flyfox_quantum.log

# Development
DEBUG=False
ENVIRONMENT=production
"""
        with open(env_template, 'w') as f:
            f.write(env_content)
        print(f"Created: {env_template}")
    
    return True

def run_tests():
    """Run basic tests to verify installation"""
    print("Running installation tests...")
    
    try:
        # Run basic tests
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("All tests passed")
            return True
        else:
            print("Some tests failed, but installation may still work")
            print(f"   Test output: {result.stdout}")
            return True  # Don't fail installation for test failures
            
    except Exception as e:
        print(f"Could not run tests: {e}")
        return True

def create_examples():
    """Create example files"""
    print("Creating examples...")
    
    # Create basic quantum example
    quantum_example = Path("examples/quantum_demo.py")
    if not quantum_example.exists():
        example_code = '''#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Basic Quantum Demo
"""

import asyncio
from goliath.quantum import GoliathQuantum

async def main():
    """Run basic quantum demonstration"""
    print("FLYFOX AI Quantum Computing Demo")
    print("=" * 40)
    
    # Initialize quantum client
    client = GoliathQuantum(
        use_simulator=True,
        apollo_mode=True,
        enable_dynex=False
    )
    
    # Create simple quantum circuit
    circuit_spec = {
        "qubits": 2,
        "gates": [
            {"type": "h", "target": 0},
            {"type": "cx", "control": 0, "target": 1}
        ],
        "measurements": [0, 1]
    }
    
    print("Executing quantum circuit...")
    result = await client.execute_quantum_circuit(circuit_spec)
    
    if result.success:
        print("Quantum circuit executed successfully!")
        print(f"   Execution time: {result.execution_time:.3f}s")
        print(f"   Backend: {result.result_data.get('backend', 'N/A')}")
    else:
        print(f"Quantum circuit failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
'''
        quantum_example.parent.mkdir(exist_ok=True)
        with open(quantum_example, 'w') as f:
            f.write(example_code)
        print(f"Created: {quantum_example}")
    
    # Create agent example
    agent_example = Path("examples/agent_demo.py")
    if not agent_example.exists():
        example_code = '''#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Agent Demo
"""

import asyncio
from agents.chatbot import create_chatbot

async def main():
    """Run agent demonstration"""
    print("FLYFOX AI Agent Demo")
    print("=" * 30)
    
    # Create chatbot
    chatbot = create_chatbot()
    
    # Test interaction
    messages = [
        "Hello!",
        "Tell me about quantum computing",
        "How can I use quantum optimization?",
        "Goodbye!"
    ]
    
    for message in messages:
        print(f"\\nYou: {message}")
        response = await chatbot.process_message(message)
        print(f"Bot: {response.content}")
        
        if response.suggestions:
            print("Suggestions:")
            for suggestion in response.suggestions:
                print(f"   • {suggestion}")

if __name__ == "__main__":
    asyncio.run(main())
'''
        with open(agent_example, 'w') as f:
            f.write(example_code)
        print(f"Created: {agent_example}")
    
    return True

def print_completion_message():
    """Print installation completion message"""
    print()
    print("FLYFOX AI Quantum Computing Platform Installation Complete!")
    print("=" * 60)
    print()
    print("Next Steps:")
    print("1. Configure your API keys:")
    print("   • Copy .env.template to .env")
    print("   • Add your API keys (OpenAI, Anthropic, Dynex)")
    print()
    print("2. Test the installation:")
    print("   • Run: python examples/quantum_demo.py")
    print("   • Run: python examples/agent_demo.py")
    print("   • Run: flyfox-quantum --help")
    print()
    print("3. Start developing:")
    print("   • Check the documentation in docs/")
    print("   • Run tests: pytest tests/")
    print("   • Use the CLI: flyfox-quantum")
    print()
    print("Useful Commands:")
    print("   • CLI help: flyfox-quantum --help")
    print("   • System status: flyfox-quantum system status")
    print("   • Quantum demo: flyfox-quantum quantum demo")
    print("   • Agent chat: flyfox-quantum agents chatbot --interactive")
    print()
    print("Documentation:")
    print("   • GitHub: https://github.com/FLYFOX-AI/flyfox-quantum-platform")
    print("   • Website: https://flyfox.ai")
    print()
    print("Happy quantum computing!")

def main():
    """Main installation function"""
    print_banner()
    
    # Check requirements
    if not check_python_version():
        return False
    
    if not check_system_requirements():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Setup platform
    if not create_directories():
        return False
    
    if not setup_configuration():
        return False
    
    if not create_examples():
        return False
    
    # Test installation
    run_tests()
    
    # Print completion message
    print_completion_message()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nInstallation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nInstallation failed: {e}")
        sys.exit(1)
