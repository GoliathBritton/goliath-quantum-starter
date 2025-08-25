#!/usr/bin/env python3
"""
FLYFOX AI Quantum Computing Platform - Command Line Interface

This module provides a comprehensive CLI for interacting with the quantum computing platform,
including quantum operations, agent interactions, and system management.
"""

import asyncio
import click
import sys
import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import yaml

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from goliath.quantum import GoliathQuantum
from agents.chatbot import create_chatbot
from agents.voice_agent import create_voice_agent
from agents.digital_human import create_digital_human
from utils.config import get_config, config
from utils.logger import get_logger, setup_logging

logger = get_logger(__name__)

@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--log-file', help='Log file path')
def cli(config_file: Optional[str], verbose: bool, log_file: Optional[str]):
    """FLYFOX AI Quantum Computing Platform CLI"""
    # Setup logging
    if verbose:
        config.logging.level = "DEBUG"
    if log_file:
        config.logging.file_path = log_file
    
    setup_logging(config.logging.__dict__)
    
    # Load custom config if provided
    if config_file:
        try:
            config.save_to_file(config_file)
            logger.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logger.error(f"Failed to load configuration from {config_file}: {e}")
    
    logger.info("FLYFOX AI Quantum Computing Platform CLI initialized")

@cli.group()
def quantum():
    """Quantum computing operations"""
    pass

@quantum.command()
@click.option('--qubits', '-q', default=4, help='Number of qubits')
@click.option('--backend', '-b', default='qiskit', help='Quantum backend')
@click.option('--optimization', '-o', default=2, help='Optimization level')
def demo(qubits: int, backend: str, optimization: int):
    """Run quantum computing demonstration"""
    asyncio.run(_run_quantum_demo(qubits, backend, optimization))

@quantum.command()
@click.argument('matrix_file')
@click.option('--algorithm', '-a', default='qaoa', help='Optimization algorithm')
@click.option('--iterations', '-i', default=100, help='Number of iterations')
def optimize(matrix_file: str, algorithm: str, iterations: int):
    """Run quantum optimization on QUBO matrix"""
    asyncio.run(_run_optimization(matrix_file, algorithm, iterations))

@quantum.command()
@click.option('--circuit', '-c', help='Circuit specification file')
@click.option('--qubits', '-q', default=2, help='Number of qubits')
def circuit(circuit: Optional[str], qubits: int):
    """Execute quantum circuit"""
    asyncio.run(_execute_circuit(circuit, qubits))

@cli.group()
def agents():
    """AI agent interactions"""
    pass

@agents.command()
@click.option('--message', '-m', help='Message to send to chatbot')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive chat session')
def chatbot(message: Optional[str], interactive: bool):
    """Interact with quantum-enhanced chatbot"""
    asyncio.run(_chatbot_interaction(message, interactive))

@agents.command()
@click.option('--duration', '-d', default=5.0, help='Recording duration in seconds')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive voice session')
def voice(duration: float, interactive: bool):
    """Interact with voice agent"""
    asyncio.run(_voice_interaction(duration, interactive))

@agents.command()
@click.option('--message', '-m', help='Message to send to digital human')
@click.option('--interactive', '-i', is_flag=True, help='Start interactive session')
def digital_human(message: Optional[str], interactive: bool):
    """Interact with digital human agent"""
    asyncio.run(_digital_human_interaction(message, interactive))

@cli.group()
def system():
    """System management and configuration"""
    pass

@system.command()
def status():
    """Show system status"""
    _show_system_status()

@system.command()
@click.option('--format', '-f', default='yaml', help='Output format (yaml/json)')
@click.option('--output', '-o', help='Output file path')
def config_show(format: str, output: Optional[str]):
    """Show current configuration"""
    _show_configuration(format, output)

@system.command()
@click.argument('key')
@click.argument('value')
def config_set(key: str, value: str):
    """Set configuration value"""
    _set_configuration(key, value)

@system.command()
@click.argument('config_file')
def config_load(config_file: str):
    """Load configuration from file"""
    _load_configuration(config_file)

@cli.command()
def version():
    """Show version information"""
    click.echo("FLYFOX AI Quantum Computing Platform v0.1.0")
    click.echo("© 2025 FLYFOX AI. All rights reserved.")

# Quantum operations implementation
async def _run_quantum_demo(qubits: int, backend: str, optimization: int):
    """Run quantum demonstration"""
    try:
        click.echo(f"🔬 Running quantum demonstration with {qubits} qubits on {backend} backend...")
        
        client = GoliathQuantum(
            use_simulator=True,
            apollo_mode=True,
            enable_dynex=False
        )
        
        # Create simple quantum circuit
        circuit_spec = {
            "qubits": qubits,
            "gates": [
                {"type": "h", "target": i} for i in range(qubits)
            ] + [
                {"type": "cx", "control": i, "target": (i + 1) % qubits} 
                for i in range(qubits - 1)
            ],
            "measurements": list(range(qubits))
        }
        
        result = await client.execute_quantum_circuit(circuit_spec, optimization_level=optimization)
        
        if result.success:
            click.echo("✅ Quantum demonstration completed successfully!")
            click.echo(f"   Execution time: {result.execution_time:.3f}s")
            click.echo(f"   Backend: {result.result_data.get('backend', 'N/A')}")
            click.echo(f"   Qubits: {result.result_data.get('qubits', 'N/A')}")
        else:
            click.echo(f"❌ Quantum demonstration failed: {result.error_message}")
            
    except Exception as e:
        logger.exception(f"Quantum demo failed: {e}")
        click.echo(f"❌ Error running quantum demonstration: {e}")

async def _run_optimization(matrix_file: str, algorithm: str, iterations: int):
    """Run quantum optimization"""
    try:
        click.echo(f"⚡ Running {algorithm.upper()} optimization...")
        
        # Load QUBO matrix
        if not os.path.exists(matrix_file):
            click.echo(f"❌ Matrix file not found: {matrix_file}")
            return
        
        with open(matrix_file, 'r') as f:
            if matrix_file.endswith('.json'):
                matrix_data = json.load(f)
            elif matrix_file.endswith('.yaml') or matrix_file.endswith('.yml'):
                matrix_data = yaml.safe_load(f)
            else:
                click.echo("❌ Unsupported file format. Use JSON or YAML.")
                return
        
        client = GoliathQuantum(
            use_simulator=True,
            apollo_mode=True,
            enable_dynex=False
        )
        
        # Run optimization
        result = await client.optimize_qubo(matrix_data, algorithm=algorithm, iterations=iterations)
        
        if result.success:
            click.echo("✅ Optimization completed successfully!")
            click.echo(f"   Solution: {result.solution}")
            click.echo(f"   Objective value: {result.objective_value}")
            click.echo(f"   Execution time: {result.execution_time:.3f}s")
        else:
            click.echo(f"❌ Optimization failed: {result.error_message}")
            
    except Exception as e:
        logger.exception(f"Optimization failed: {e}")
        click.echo(f"❌ Error running optimization: {e}")

async def _execute_circuit(circuit_file: Optional[str], qubits: int):
    """Execute quantum circuit"""
    try:
        if circuit_file:
            click.echo(f"🔬 Executing quantum circuit from {circuit_file}...")
            with open(circuit_file, 'r') as f:
                circuit_spec = json.load(f)
        else:
            click.echo(f"🔬 Executing default {qubits}-qubit circuit...")
            # Create default circuit
            circuit_spec = {
                "qubits": qubits,
                "gates": [
                    {"type": "h", "target": 0},
                    {"type": "cx", "control": 0, "target": 1}
                ] + [
                    {"type": "h", "target": i} for i in range(2, qubits)
                ],
                "measurements": list(range(qubits))
            }
        
        client = GoliathQuantum(
            use_simulator=True,
            apollo_mode=True,
            enable_dynex=False
        )
        
        result = await client.execute_quantum_circuit(circuit_spec)
        
        if result.success:
            click.echo("✅ Circuit executed successfully!")
            click.echo(f"   Execution time: {result.execution_time:.3f}s")
            click.echo(f"   Backend: {result.result_data.get('backend', 'N/A')}")
        else:
            click.echo(f"❌ Circuit execution failed: {result.error_message}")
            
    except Exception as e:
        logger.exception(f"Circuit execution failed: {e}")
        click.echo(f"❌ Error executing circuit: {e}")

# Agent interactions implementation
async def _chatbot_interaction(message: Optional[str], interactive: bool):
    """Interact with chatbot"""
    try:
        chatbot = create_chatbot()
        
        if interactive:
            click.echo("🤖 Starting interactive chat session with quantum chatbot...")
            click.echo("Type 'quit' or 'exit' to end the session.")
            
            while True:
                try:
                    user_input = click.prompt("You", prompt_suffix=": ")
                    if user_input.lower() in ['quit', 'exit', 'bye']:
                        break
                    
                    response = await chatbot.process_message(user_input)
                    click.echo(f"🤖 {response.content}")
                    
                    if response.suggestions:
                        click.echo("💡 Suggestions:")
                        for suggestion in response.suggestions:
                            click.echo(f"   • {suggestion}")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    click.echo(f"❌ Error: {e}")
            
            click.echo("👋 Chat session ended.")
        else:
            if not message:
                message = click.prompt("Enter your message")
            
            response = await chatbot.process_message(message)
            click.echo(f"🤖 {response.content}")
            
    except Exception as e:
        logger.exception(f"Chatbot interaction failed: {e}")
        click.echo(f"❌ Error: {e}")

async def _voice_interaction(duration: float, interactive: bool):
    """Interact with voice agent"""
    try:
        voice_agent = create_voice_agent()
        
        if not voice_agent.is_available():
            click.echo("❌ Voice processing not available. Install required dependencies.")
            return
        
        if interactive:
            click.echo("🎤 Starting interactive voice session...")
            click.echo("Press Ctrl+C to end the session.")
            
            while True:
                try:
                    click.echo(f"🎤 Recording {duration} seconds of audio...")
                    audio_data, audio_format = voice_agent.record_audio(duration)
                    
                    click.echo("🔄 Processing voice command...")
                    response = await voice_agent.process_voice_command(audio_data, audio_format)
                    
                    click.echo(f"🎤 {response.text}")
                    
                    if response.audio_file:
                        click.echo("🔊 Playing audio response...")
                        voice_agent.play_audio(response.audio_file)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    click.echo(f"❌ Error: {e}")
            
            click.echo("👋 Voice session ended.")
        else:
            click.echo(f"🎤 Recording {duration} seconds of audio...")
            audio_data, audio_format = voice_agent.record_audio(duration)
            
            click.echo("🔄 Processing voice command...")
            response = await voice_agent.process_voice_command(audio_data, audio_format)
            
            click.echo(f"🎤 {response.text}")
            
    except Exception as e:
        logger.exception(f"Voice interaction failed: {e}")
        click.echo(f"❌ Error: {e}")

async def _digital_human_interaction(message: Optional[str], interactive: bool):
    """Interact with digital human"""
    try:
        digital_human = create_digital_human()
        
        if interactive:
            click.echo("👤 Starting interactive session with digital human...")
            click.echo("Type 'quit' or 'exit' to end the session.")
            
            while True:
                try:
                    user_input = click.prompt("You", prompt_suffix=": ")
                    if user_input.lower() in ['quit', 'exit', 'bye']:
                        break
                    
                    response = await digital_human.interact(user_input)
                    click.echo(f"👤 {response.content}")
                    
                    if response.follow_up_questions:
                        click.echo("💭 Follow-up questions:")
                        for question in response.follow_up_questions:
                            click.echo(f"   • {question}")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    click.echo(f"❌ Error: {e}")
            
            click.echo("👋 Digital human session ended.")
        else:
            if not message:
                message = click.prompt("Enter your message")
            
            response = await digital_human.interact(message)
            click.echo(f"👤 {response.content}")
            
    except Exception as e:
        logger.exception(f"Digital human interaction failed: {e}")
        click.echo(f"❌ Error: {e}")

# System management implementation
def _show_system_status():
    """Show system status"""
    click.echo("🔍 FLYFOX AI Quantum Computing Platform - System Status")
    click.echo("=" * 60)
    
    # Configuration status
    click.echo("📋 Configuration:")
    click.echo(f"   Quantum Backend: {config.quantum.backend}")
    click.echo(f"   Max Qubits: {config.quantum.max_qubits}")
    click.echo(f"   Optimization Level: {config.quantum.optimization_level}")
    click.echo(f"   Apollo Mode: {'Enabled' if config.quantum.enable_apollo_mode else 'Disabled'}")
    click.echo(f"   Dynex Integration: {'Enabled' if config.dynex.api_key else 'Disabled'}")
    
    # Agent status
    click.echo("\n🤖 Agents:")
    click.echo(f"   Chatbot: {'Enabled' if config.agent.enable_chatbot else 'Disabled'}")
    click.echo(f"   Voice Agent: {'Enabled' if config.agent.enable_voice else 'Disabled'}")
    click.echo(f"   Digital Human: {'Enabled' if config.agent.enable_digital_human else 'Disabled'}")
    
    # Logging status
    click.echo("\n📝 Logging:")
    click.echo(f"   Level: {config.logging.level}")
    click.echo(f"   Console: {'Enabled' if config.logging.enable_console else 'Disabled'}")
    click.echo(f"   File: {config.logging.file_path or 'Not configured'}")
    
    click.echo("\n✅ System is ready!")

def _show_configuration(format: str, output: Optional[str]):
    """Show current configuration"""
    config_dict = {
        'quantum': config.quantum.__dict__,
        'dynex': config.dynex.__dict__,
        'nqba': config.nqba.__dict__,
        'agent': config.agent.__dict__,
        'logging': config.logging.__dict__,
    }
    
    if format == 'json':
        config_str = json.dumps(config_dict, indent=2)
    else:
        config_str = yaml.dump(config_dict, default_flow_style=False, indent=2)
    
    if output:
        with open(output, 'w') as f:
            f.write(config_str)
        click.echo(f"Configuration saved to {output}")
    else:
        click.echo(config_str)

def _set_configuration(key: str, value: str):
    """Set configuration value"""
    try:
        config.set(key, value)
        click.echo(f"✅ Configuration updated: {key} = {value}")
    except Exception as e:
        click.echo(f"❌ Failed to update configuration: {e}")

def _load_configuration(config_file: str):
    """Load configuration from file"""
    try:
        config.save_to_file(config_file)
        click.echo(f"✅ Configuration loaded from {config_file}")
    except Exception as e:
        click.echo(f"❌ Failed to load configuration: {e}")

if __name__ == '__main__':
    cli()
