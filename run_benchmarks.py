#!/usr/bin/env python3
"""
NQBA Stack Benchmark Runner

Simple CLI script to run benchmarks and generate comprehensive reports.
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nqba_stack.benchmarks import (
    BenchmarkRunner,
    BenchmarkConfig,
    get_all_problems,
    generate_all_reports,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    """Main benchmark execution function"""
    print("🚀 NQBA Stack Benchmark Runner")
    print("=" * 50)

    # Configuration
    config = BenchmarkConfig(
        problem_size=50,  # Start with moderate size
        iterations=5,  # 5 runs per problem
        timeout_seconds=120,  # 2 minute timeout
        output_dir="benchmark_results",
        save_detailed=True,
        compare_solutions=True,
    )

    print(f"Configuration:")
    print(f"  Problem Size: {config.problem_size}")
    print(f"  Iterations: {config.iterations}")
    print(f"  Timeout: {config.timeout_seconds}s")
    print(f"  Output Directory: {config.output_dir}")
    print()

    # Get all problems
    problems = get_all_problems()
    print(f"Problems to benchmark: {len(problems)}")
    for problem in problems:
        print(f"  - {problem.name}")
    print()

    # Create benchmark runner
    runner = BenchmarkRunner(config)

    try:
        print("Starting comprehensive benchmark...")
        print("This may take several minutes depending on problem complexity.")
        print()

        # Run benchmarks
        report = await runner.run_comprehensive_benchmark(problems)

        print("✅ Benchmark completed successfully!")
        print()

        # Display summary
        print("📊 BENCHMARK SUMMARY")
        print("-" * 30)
        print(f"Total Problems: {report.total_problems}")
        print(f"Quantum Success Rate: {report.summary['quantum_success_rate']:.1%}")
        print(f"Classical Success Rate: {report.summary['classical_success_rate']:.1%}")
        print(f"Overall Speedup: {report.summary['average_speedup']:.2f}x")
        print(
            f"Quality Improvement: {report.summary['quality_improvement_percent']:+.1f}%"
        )
        print()

        # Display quantum advantage assessment
        speedup = report.summary["average_speedup"]
        quality = report.summary["quality_improvement_percent"]

        print("🎯 QUANTUM ADVANTAGE ASSESSMENT")
        print("-" * 35)

        if speedup > 2.0:
            print("🚀 EXCEPTIONAL: Significant quantum speedup (>2x)")
        elif speedup > 1.5:
            print("⚡ STRONG: Moderate quantum speedup (1.5-2x)")
        elif speedup > 1.1:
            print("📈 MODEST: Slight quantum speedup (1.1-1.5x)")
        else:
            print("⚠️ LIMITED: Minimal quantum speedup (<1.1x)")

        if quality > 10:
            print("🎯 EXCEPTIONAL: Significantly better quality")
        elif quality > 5:
            print("📊 STRONG: Notable quality improvement")
        elif quality > 0:
            print("✅ POSITIVE: Slight quality improvement")
        else:
            print("🔍 NEUTRAL: Comparable quality")

        print()

        # Generate comprehensive reports
        print("📋 Generating comprehensive reports...")
        comprehensive_report = generate_all_reports(
            runner.results, config, "benchmark_reports"
        )

        print("✅ Reports generated successfully!")
        print()
        print("📁 Report files created:")
        print("  - benchmark_reports/executive_summary.txt")
        print("  - benchmark_reports/technical_report.txt")
        print("  - benchmark_reports/investor_one_pager.txt")
        print("  - benchmark_reports/benchmark_report.json")
        print("  - benchmark_reports/*.png (charts)")
        print()

        # Display top recommendations
        print("💡 TOP RECOMMENDATIONS")
        print("-" * 25)
        for i, rec in enumerate(comprehensive_report.recommendations[:3], 1):
            print(f"{i}. {rec}")
        print()

        print("🎉 Benchmark execution complete!")
        print("Review the generated reports for detailed analysis.")

    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        logging.error(f"Benchmark execution failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Benchmark interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
