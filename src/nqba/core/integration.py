import asyncio
import logging
from typing import Dict, Any, List

from .ingestion import DataIngestor
from .analysis import AdvancedAnalyzer
from .presentation import SolutionPresenter
from mcp import MCPClient\nfrom .intelligence import qdllm

logger = logging.getLogger(__name__)

class SolutionIntegrator:
    """
    Orchestrates the full NQBA solution pipeline:
    - Data ingestion
    - Advanced analysis and deciphering
    - Solution presentation and visualization
    """

    def __init__(
        self,
        ingestor: DataIngestor,
        analyzer: AdvancedAnalyzer,
        presenter: SolutionPresenter
    ):
        self.ingestor = ingestor
        self.analyzer = analyzer
        self.presenter = presenter

    async def integrate_solution(
        self,
        data_sources: List[str],
        analysis_params: Dict[str, Any] = None,
        presentation_format: str = "both"  # "pdf", "dashboard", or "both"
    ) -> Dict[str, Any]:
        """
        Run the complete integration pipeline.

        Args:
            data_sources: List of data source paths/URLs
            analysis_params: Parameters for analysis
            presentation_format: Output format

        Returns:
            Dict with presentation outputs (PDF path, dashboard script path)
        """
        try:
            # Step 1: Ingest data
            logger.info("Starting data ingestion...")
            ingested_data = await self.ingestor.ingest_data(data_sources)
            logger.info("Data ingestion completed")

            # Step 2: Analyze data
            logger.info("Starting advanced analysis...")
            analysis_results = await self.analyzer.analyze_data(
                ingested_data,
                params=analysis_params or {}
            )
            logger.info("Analysis completed")

            # Step 3: Present solution
            logger.info("Generating presentation...")
            presentation_outputs = self.presenter.present_solution(
                analysis_results,
                output_format=presentation_format
            )
            logger.info("Presentation generated")

            return presentation_outputs

        except Exception as e:
            logger.error(f"Integration failed: {str(e)}")
            raise

    def integrate_via_mcp(self, solutions, target_system):\n        mcp_client = MCPClient()\n        mcp_client.push_solution(target_system['mcp_endpoint'], solutions)  # Secure push\n        # Monitor outcomes with MCP callbacks\n        roi = qdllm.reason(mcp_client.get_feedback(), context='roi_calc')\n        return {'integrated': True, 'roi': roi}