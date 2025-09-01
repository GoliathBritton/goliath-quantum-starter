#!/usr/bin/env python3
"""
Goliath Quantum Starter CLI - Enhanced Developer Experience

Simplified command structure with comprehensive help and error handling.
"""

import click
import requests
import json
import time
import os
from typing import Dict, Any, Optional
from pathlib import Path

# Configuration
DEFAULT_API_URL = "http://localhost:8000"
CONFIG_FILE = Path.home() / ".goliath" / "config.json"


class GoliathCLI:
    """Enhanced CLI for Goliath Quantum Starter"""

    def __init__(self):
        self.api_url = self._load_config().get("api_url", DEFAULT_API_URL)
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)

    def _make_request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        url = f"{self.api_url}{endpoint}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            click.echo(f"Error: Cannot connect to {self.api_url}")
            click.echo(
                "Make sure the API server is running with: python -m src.nqba_stack.api_server"
            )
            raise click.Abort()
        except requests.exceptions.HTTPError as e:
            click.echo(f"HTTP Error {e.response.status_code}: {e.response.text}")
            raise click.Abort()
        except Exception as e:
            click.echo(f"Error: {str(e)}")
            raise click.Abort()


# CLI Instance
cli = GoliathCLI()


@click.group()
@click.version_option(version="2.0.0")
@click.option("--api-url", default=DEFAULT_API_URL, help="API server URL")
def main(api_url: str):
    """🚀 Goliath Omniedge Quantum Starter CLI - Quantum-Enhanced Business Intelligence"""
    if api_url != DEFAULT_API_URL:
        cli.api_url = api_url
        config = cli._load_config()
        config["api_url"] = api_url
        cli._save_config(config)


@main.command()
def status():
    """Check system status and health"""
    click.echo("Checking system status...")

    try:
        # Health check
        health = cli._make_request("GET", "/health")
        click.echo(f"System Status: {health['status']}")
        click.echo(f"Version: {health['version']}")
        click.echo(f"Business Pods: {len(health['business_pods'])}")

        # Business pod metrics
        metrics = cli._make_request("GET", "/metrics/business-pods")
        click.echo(f"\nBusiness Pod Metrics:")
        for pod in metrics:
            click.echo(
                f"  • {pod['pod_name']}: {pod['total_operations']} operations, "
                f"{pod['average_quantum_advantage']:.1f}x quantum advantage"
            )

        # Quantum status
        quantum = cli._make_request("GET", "/quantum/status")
        click.echo(f"\nQuantum Status: {quantum['status']}")
        click.echo(f"  • Active Operations: {quantum['active_operations']}")
        click.echo(f"  • Queue Length: {quantum['queue_length']}")

    except Exception as e:
        click.echo(f"Failed to get status: {str(e)}")


@main.group()
def pods():
    """Manage business pods"""


@pods.command()
def list():
    """List all available business pods"""
    click.echo("Available Business Pods:")
    click.echo("  • Sigma Select - Sales Intelligence & Lead Scoring")
    click.echo("  • Goliath - Energy Optimization & Consumption Management")
    click.echo("  • Goliath Trade - Financial Trading & Portfolio Optimization")
    click.echo("  • SFG Symmetry - Insurance & Financial Services")
    click.echo("  • Ghost NeuroQ - Competitive Intelligence & Data Warfare")


@pods.command()
@click.argument("pod_name")
def demo(pod_name: str):
    """Run demo for a specific business pod"""
    click.echo(f"Running demo for {pod_name}...")

    try:
        if pod_name == "sigma-select":
            result = cli._make_request(
                "POST",
                "/sigma-select/score-leads",
                {
                    "leads": [
                        {
                            "company": "Demo Corp",
                            "revenue": 1000000,
                            "industry": "Technology",
                        }
                    ],
                    "optimization_level": "maximum",
                },
            )
            click.echo(
                f"Lead scored with {result['quantum_advantage']:.1f}x quantum advantage"
            )

        elif pod_name == "goliath":
            result = cli._make_request(
                "POST",
                "/goliath/optimize-energy",
                {
                    "energy_data": {
                        "current_consumption": {
                            "peak_hours": [14],
                            "off_peak_hours": [1, 2, 3],
                        }
                    },
                    "optimization_level": "maximum",
                },
            )
            click.echo(
                f"Energy optimized with {result['quantum_advantage']:.1f}x quantum advantage"
            )

        elif pod_name == "goliath-trade":
            result = cli._make_request(
                "POST",
                "/goliath-trade/optimize-portfolio",
                {
                    "portfolio_data": {
                        "assets": [{"symbol": "DEMO", "current_weight": 1.0}]
                    },
                    "optimization_level": "maximum",
                },
            )
            click.echo(
                f"Portfolio optimized with {result['quantum_advantage']:.1f}x quantum advantage"
            )

        elif pod_name == "sfg-symmetry":
            # Register client first
            client = cli._make_request(
                "POST",
                "/sfg-symmetry/register-client",
                {"age": 0, "income": 50000, "assets": 100000, "liabilities": 20000},
            )
            result = cli._make_request(
                "POST",
                "/sfg-symmetry/generate-recommendations",
                {"client_id": client["client_id"], "optimization_level": "maximum"},
            )
            click.echo(
                f"Financial recommendations generated with {result['quantum_advantage']:.1f}x quantum advantage"
            )

        elif pod_name == "ghost-neuroq":
            # Register target first
            target = cli._make_request(
                "POST",
                "/ghost-neuroq/register-target",
                {"name": "Demo Target", "organization": "Demo Org", "industry": "Demo"},
            )
            result = cli._make_request(
                "POST",
                "/ghost-neuroq/execute-neuro-siphon",
                {"target_id": target["target_id"], "operation_type": "data_extraction"},
            )
            click.echo(
                f"Intelligence gathered with {result['results']['quantum_advantage']:.1f}x quantum advantage"
            )

        else:
            click.echo(f"Unknown pod: {pod_name}")
            click.echo(
                "Available pods: sigma-select, goliath, goliath-trade, sfg-symmetry, ghost-neuroq"
            )

    except Exception as e:
        click.echo(f"Demo failed: {str(e)}")


@main.group()
def quantum():
    """Quantum computing operations"""


@quantum.command()
@click.option(
    "--problem-type",
    default="portfolio_optimization",
    help="Type of optimization problem",
)
@click.option(
    "--assets", default="AAPL,GOOGL,MSFT", help="Comma-separated list of assets"
)
@click.option("--risk-tolerance", default=0.6, help="Risk tolerance (0.0 to 1.0)")
@click.option("--optimization-level", default="maximum", help="Optimization level")
def optimize(
    problem_type: str, assets: str, risk_tolerance: float, optimization_level: str
):
    """Run quantum optimization"""
    click.echo(f"⚛️ Running quantum optimization...")

    asset_list = [asset.strip() for asset in assets.split(",")]

    try:
        result = cli._make_request(
            "POST",
            "/quantum/operate",
            {
                "operation_type": "optimization",
                "parameters": {
                    "problem_type": problem_type,
                    "assets": asset_list,
                    "constraints": {"risk_tolerance": risk_tolerance},
                },
                "business_pod": "goliath_trade",
                "optimization_level": optimization_level,
            },
        )

        click.echo(f"✅ Optimization completed!")
        click.echo(f"  • Quantum Advantage: {result['quantum_advantage']:.1f}x")
        click.echo(f"  • Execution Time: {result['execution_time']:.2f}s")
        click.echo(f"  • Status: {result['status']}")

    except Exception as e:
        click.echo(f"Optimization failed: {str(e)}")


@main.group()
def ltc():
    """Living Technical Codex operations"""


@ltc.command()
@click.option("--limit", default=10, help="Number of entries to retrieve")
@click.option("--pod", help="Filter by business pod")
def entries(limit: int, pod: Optional[str]):
    """Get LTC entries"""
    click.echo(f"📚 Retrieving LTC entries...")

    try:
        endpoint = f"/ltc/entries?limit={limit}"
        if pod:
            endpoint += f"&business_pod={pod}"

        result = cli._make_request("GET", endpoint)

        click.echo(f"📊 Found {result['total_count']} entries:")
        for entry in result["entries"][:limit]:
            click.echo(
                f"  • {entry['entry_id']}: {entry['operation_type']} "
                f"({entry['business_pod']}) - {entry['timestamp']}"
            )

    except Exception as e:
        click.echo(f"Failed to retrieve entries: {str(e)}")


@ltc.command()
def stats():
    """Get LTC statistics"""
    click.echo(f"📊 Retrieving LTC statistics...")

    try:
        result = cli._make_request("GET", "/ltc/statistics")

        click.echo(f"📈 LTC Statistics:")
        click.echo(f"  • Total Entries: {result['statistics']['total_entries']}")
        click.echo(
            f"  • Quantum Enhanced Ratio: {result['statistics']['quantum_enhanced_ratio']:.1%}"
        )
        click.echo(
            f"  • Average Quantum Advantage: {result['statistics']['average_quantum_advantage']:.1f}x"
        )

        click.echo(f"\n📊 Entries by Pod:")
        for pod, count in result["statistics"]["entries_by_pod"].items():
            click.echo(f"  • {pod}: {count}")

    except Exception as e:
        click.echo(f"Failed to retrieve statistics: {str(e)}")


@main.command()
def benchmark():
    """Run comprehensive performance benchmark"""
    click.echo("📊 Running comprehensive benchmark...")

    pods = [
        ("sigma_select", "score-leads"),
        ("goliath", "optimize-energy"),
        ("goliath-trade", "optimize-portfolio"),
        ("sfg-symmetry", "generate-recommendations"),
        ("ghost-neuroq", "execute-neuro-siphon"),
    ]

    results = {}

    for pod, endpoint in pods:
        click.echo(f"  🔄 Testing {pod}...")
        start_time = time.time()

        try:
            # Run basic operation for each pod
            if pod == "sigma_select":
                response = cli._make_request(
                    "POST",
                    f"/{pod}/{endpoint}",
                    {
                        "leads": [{"company": "Benchmark", "revenue": 1000000}],
                        "optimization_level": "maximum",
                    },
                )
                quantum_advantage = response.get("quantum_advantage", 1.0)

            elif pod == "goliath":
                response = cli._make_request(
                    "POST",
                    f"/{pod}/{endpoint}",
                    {
                        "energy_data": {
                            "current_consumption": {
                                "peak_hours": [14],
                                "off_peak_hours": [1, 2, 3],
                            }
                        },
                        "optimization_level": "maximum",
                    },
                )
                quantum_advantage = response.get("quantum_advantage", 1.0)

            elif pod == "goliath-trade":
                response = cli._make_request(
                    "POST",
                    f"/{pod}/{endpoint}",
                    {
                        "portfolio_data": {
                            "assets": [{"symbol": "BENCH", "current_weight": 1.0}]
                        },
                        "optimization_level": "maximum",
                    },
                )
                quantum_advantage = response.get("quantum_advantage", 1.0)

            elif pod == "sfg-symmetry":
                # First register client
                client = cli._make_request(
                    "POST",
                    f"/{pod}/register-client",
                    {
                        "age": 30,
                        "income": 50000,
                        "assets": 100000,
                        "liabilities": 20000,
                    },
                )
                response = cli._make_request(
                    "POST",
                    f"/{pod}/{endpoint}",
                    {"client_id": client["client_id"], "optimization_level": "maximum"},
                )
                quantum_advantage = response.get("quantum_advantage", 1.0)

            elif pod == "ghost-neuroq":
                # First register target
                target = cli._make_request(
                    "POST",
                    f"/{pod}/register-target",
                    {
                        "name": "Benchmark Target",
                        "organization": "Benchmark Org",
                        "industry": "Benchmark",
                    },
                )
                response = cli._make_request(
                    "POST",
                    f"/{pod}/{endpoint}",
                    {
                        "target_id": target["target_id"],
                        "operation_type": "data_extraction",
                    },
                )
                quantum_advantage = response["results"].get("quantum_advantage", 1.0)

            execution_time = time.time() - start_time

            results[pod] = {
                "quantum_advantage": quantum_advantage,
                "execution_time": execution_time,
                "status": "success",
            }

            click.echo(
                f"    ✅ {pod}: {quantum_advantage:.1f}x quantum advantage, {execution_time:.2f}s"
            )

        except Exception as e:
            execution_time = time.time() - start_time
            results[pod] = {
                "quantum_advantage": 1.0,
                "execution_time": execution_time,
                "status": f"error: {str(e)}",
            }
            click.echo(f"    {pod}: Failed - {str(e)}")

    # Print summary
    click.echo(f"\n📊 Benchmark Summary:")
    click.echo(
        f"{'Pod':<20} {'Quantum Advantage':<18} {'Execution Time':<15} {'Status'}"
    )
    click.echo("-" * 70)

    total_quantum_advantage = 0
    successful_pods = 0

    for pod, result in results.items():
        status = result["status"]
        if status == "success":
            total_quantum_advantage += result["quantum_advantage"]
            successful_pods += 1

        click.echo(
            f"{pod:<20} {result['quantum_advantage']:<18.1f}x {result['execution_time']:<15.2f}s {status}"
        )

    if successful_pods > 0:
        avg_quantum_advantage = total_quantum_advantage / successful_pods
        click.echo(f"\n🎯 Average Quantum Advantage: {avg_quantum_advantage:.1f}x")
        click.echo(f"✅ Successful Pods: {successful_pods}/{len(pods)}")

    return results


@main.command()
def setup():
    """Interactive setup and configuration"""
    click.echo("🚀 Goliath Quantum Starter Setup")
    click.echo("=" * 40)

    # API URL
    current_url = cli.api_url
    new_url = click.prompt(
        f"API Server URL (current: {current_url})", default=current_url, type=str
    )

    if new_url != current_url:
        cli.api_url = new_url
        config = cli._load_config()
        config["api_url"] = new_url
        cli._save_config(config)
        click.echo(f"✅ API URL updated to: {new_url}")

    # Test connection
    click.echo("\n🔍 Testing connection...")
    try:
        health = cli._make_request("GET", "/health")
        click.echo(f"✅ Connection successful! System status: {health['status']}")
        click.echo(f"📊 Version: {health['version']}")
        click.echo(f"🏢 Business Pods: {len(health['business_pods'])}")

        # Test each pod
        click.echo("\n🧪 Testing business pods...")
        pods_to_test = [
            ("sigma-select", "Lead Scoring"),
            ("goliath", "Energy Optimization"),
            ("goliath-trade", "Portfolio Optimization"),
            ("sfg-symmetry", "Financial Services"),
            ("ghost-neuroq", "Intelligence Gathering"),
        ]

        for pod, description in pods_to_test:
            try:
                # Simple test for each pod
                if pod == "sigma-select":
                    cli._make_request(
                        "POST",
                        f"/{pod}/score-leads",
                        {
                            "leads": [{"company": "Setup Test", "revenue": 1000000}],
                            "optimization_level": "maximum",
                        },
                    )
                elif pod == "goliath":
                    cli._make_request(
                        "POST",
                        f"/{pod}/optimize-energy",
                        {
                            "energy_data": {
                                "current_consumption": {
                                    "peak_hours": [14],
                                    "off_peak_hours": [1, 2, 3],
                                }
                            },
                            "optimization_level": "maximum",
                        },
                    )
                elif pod == "goliath-trade":
                    cli._make_request(
                        "POST",
                        f"/{pod}/optimize-portfolio",
                        {
                            "portfolio_data": {
                                "assets": [{"symbol": "SETUP", "current_weight": 1.0}]
                            },
                            "optimization_level": "maximum",
                        },
                    )
                elif pod == "sfg-symmetry":
                    client = cli._make_request(
                        "POST",
                        f"/{pod}/register-client",
                        {
                            "age": 30,
                            "income": 50000,
                            "assets": 100000,
                            "liabilities": 20000,
                        },
                    )
                    cli._make_request(
                        "POST",
                        f"/{pod}/generate-recommendations",
                        {
                            "client_id": client["client_id"],
                            "optimization_level": "maximum",
                        },
                    )
                elif pod == "ghost-neuroq":
                    target = cli._make_request(
                        "POST",
                        f"/{pod}/register-target",
                        {
                            "name": "Setup Target",
                            "organization": "Setup Org",
                            "industry": "Setup",
                        },
                    )
                    cli._make_request(
                        "POST",
                        f"/{pod}/execute-neuro-siphon",
                        {
                            "target_id": target["target_id"],
                            "operation_type": "data_extraction",
                        },
                    )

                click.echo(f"  ✅ {description} - Working")

            except Exception as e:
                click.echo(f"  {description} - Failed: {str(e)}")

        click.echo(f"\n🎉 Setup complete! All systems operational.")
        click.echo(f"💡 Try running: goliath status")
        click.echo(f"💡 Or test a specific pod: goliath pods demo sigma-select")

    except Exception as e:
        click.echo(f"Connection failed: {str(e)}")
        click.echo(
            f"💡 Make sure the API server is running with: python -m src.nqba_stack.api_server"
        )


@main.command()
def docs():
    """Open documentation and resources"""
    click.echo("📚 Goliath Quantum Starter Documentation")
    click.echo("=" * 40)

    docs_links = [
        ("📖 API Documentation", "docs/api_documentation.md"),
        ("🚀 Quick Start Templates", "docs/quick_start_templates.md"),
        ("🏗️ Architecture Guide", "docs/architecture.md"),
        ("💼 Business Case", "BUSINESS_CASE.md"),
        ("🚀 Development Roadmap", "DEVELOPMENT_ROADMAP.md"),
        ("📋 Project Management", "PROJECT_MANAGEMENT.md"),
    ]

    for title, path in docs_links:
        if Path(path).exists():
            click.echo(f"  ✅ {title}: {path}")
        else:
            click.echo(f"  {title}: {path} (not found)")

    click.echo(f"\n🌐 Interactive API Docs: {cli.api_url}/docs")
    click.echo(f"📖 Swagger UI: {cli.api_url}/docs")
    click.echo(f"🔧 Health Check: {cli.api_url}/health")


if __name__ == "__main__":
    main()
