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

import argparse

def main():
    parser = argparse.ArgumentParser(description="FLYFOX AI Quantum Computing Platform Installer")
    parser.add_argument("--web3-init", action="store_true", help="Initialize Web3 components")
    parser.add_argument("--web3-mcp", action="store_true", help="Set up Web3 MCP integrations")
    args = parser.parse_args()

    print_banner()
    
    if not check_python_version():
        sys.exit(1)
        
    if not check_system_requirements():
        sys.exit(1)
        
    if not install_dependencies():
        sys.exit(1)
        
    create_directories()
    setup_configuration()
    
    if args.web3_init:
        print("Initializing Web3 components...")
        web3_dir = Path("web3/hardhat")
        if web3_dir.exists():
            os.chdir(web3_dir)
            try:
                subprocess.run(["npm", "install"], check=True)
                print("Installed Hardhat dependencies")
                subprocess.run(["npx", "hardhat", "compile"], check=True)
                print("Compiled smart contracts")
                # Add more Web3 init steps if needed
            except subprocess.CalledProcessError as e:
                print(f"Web3 initialization failed: {e}")
            finally:
                os.chdir("../..")
        else:
            print("Web3 directory not found")
    if args.web3_mcp:
        print("Setting up Web3 MCP integrations...")
        web3_dir = Path("web3/hardhat")
        if web3_dir.exists():
            os.chdir(web3_dir)
            try:
                subprocess.run(["npm", "install"], check=True)
                subprocess.run(["npx", "hardhat", "compile"], check=True)
                node_process = subprocess.Popen(["npx", "hardhat", "node"])
                print("Started Hardhat local node")
                import time
                time.sleep(5)
                subprocess.run(["npx", "hardhat", "run", "scripts/deploy.js", "--network", "localhost"], check=True)
                print("Deployed contracts for MCP")
            except Exception as e:
                print(f"Web3 MCP setup failed: {e}")
            finally:
                os.chdir("../..")
        else:
            print("Web3 directory not found")
    
    run_tests()
    create_examples()
    
    print("\nInstallation completed successfully!")
    print("To get started:")
    print("1. Copy .env.template to .env and fill in your API keys")
    print("2. Run: python src/main.py")
    print("3. For quantum demos: python examples/quantum_demo.py")
    print("4. For agent demos: python examples/agent_demo.py")
    print("\nFor Web3 features, use --web3-init flag")

if __name__ == "__main__":
    main()    for message in messages:
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
