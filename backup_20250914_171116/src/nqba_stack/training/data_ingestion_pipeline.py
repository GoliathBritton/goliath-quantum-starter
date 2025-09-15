"""Data Ingestion Pipeline for NQBA Platform Training Data

This module provides comprehensive data ingestion capabilities for training
the platform's AI/ML models with diverse, high-quality datasets.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from pathlib import Path
import json
import hashlib
import aiohttp
import pandas as pd
import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from ..core.ltc_logger import LTCLogger
from ..core.quantum_adapter import QuantumAdapter
from ..database.models import TrainingDataset, DataSource, DataQualityMetrics
from ..security.encryption import QuantumEncryption

logger = LTCLogger("DataIngestionPipeline")


class DataSourceType(Enum):
    """Types of data sources for training"""
    
    FINANCIAL_MARKET = "financial_market"
    SCIENTIFIC_LITERATURE = "scientific_literature"
    ECONOMIC_INDICATORS = "economic_indicators"
    CORPORATE_DATA = "corporate_data"
    ALTERNATIVE_DATA = "alternative_data"
    REAL_TIME_FEEDS = "real_time_feeds"
    BENCHMARK_DATASETS = "benchmark_datasets"
    PROPRIETARY_DATA = "proprietary_data"


class DataFormat(Enum):
    """Supported data formats"""
    
    JSON = "json"
    CSV = "csv"
    PARQUET = "parquet"
    AVRO = "avro"
    XML = "xml"
    TEXT = "text"
    BINARY = "binary"
    STREAM = "stream"


class DataQuality(Enum):
    """Data quality levels"""
    
    EXCELLENT = "excellent"  # 95%+ quality score
    GOOD = "good"           # 85-94% quality score
    FAIR = "fair"           # 70-84% quality score
    POOR = "poor"           # <70% quality score


@dataclass
class DataSourceConfig:
    """Configuration for a data source"""
    
    source_id: str
    source_type: DataSourceType
    name: str
    description: str
    endpoint_url: str
    api_key: Optional[str] = None
    format: DataFormat = DataFormat.JSON
    update_frequency: str = "daily"  # cron expression or interval
    quality_threshold: float = 0.85
    encryption_required: bool = True
    compliance_tags: List[str] = field(default_factory=list)
    custom_headers: Dict[str, str] = field(default_factory=dict)
    rate_limit: Optional[int] = None  # requests per minute
    timeout: int = 30  # seconds
    retry_attempts: int = 3
    batch_size: int = 1000
    enabled: bool = True


@dataclass
class DataIngestionResult:
    """Result of data ingestion operation"""
    
    source_id: str
    success: bool
    records_processed: int
    records_valid: int
    records_invalid: int
    quality_score: float
    processing_time: float
    data_size_mb: float
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DataValidationRule:
    """Data validation rule definition"""
    
    rule_id: str
    field_name: str
    rule_type: str  # required, type, range, pattern, custom
    parameters: Dict[str, Any]
    severity: str = "error"  # error, warning, info
    description: str = ""


class DataIngestionPipeline:
    """Comprehensive data ingestion pipeline for training data"""
    
    def __init__(
        self,
        db_session: AsyncSession,
        redis_client: Redis,
        quantum_adapter: QuantumAdapter,
        ltc_logger: LTCLogger,
        encryption: QuantumEncryption,
        storage_path: Path = Path("/data/training")
    ):
        self.db_session = db_session
        self.redis_client = redis_client
        self.quantum_adapter = quantum_adapter
        self.ltc_logger = ltc_logger
        self.encryption = encryption
        self.storage_path = storage_path
        
        # Data source configurations
        self.data_sources: Dict[str, DataSourceConfig] = {}
        
        # Validation rules
        self.validation_rules: Dict[str, List[DataValidationRule]] = {}
        
        # Quality metrics
        self.quality_metrics: Dict[str, float] = {}
        
        # Processing statistics
        self.stats = {
            "total_ingested": 0,
            "total_processed": 0,
            "total_errors": 0,
            "average_quality": 0.0,
            "last_update": None
        }
        
        # Initialize built-in data sources
        self._initialize_data_sources()
        
        logger.info("Data Ingestion Pipeline initialized")
    
    def _initialize_data_sources(self):
        """Initialize built-in data source configurations"""
        
        # Financial Market Data Sources
        self.add_data_source(DataSourceConfig(
            source_id="alpha_vantage",
            source_type=DataSourceType.FINANCIAL_MARKET,
            name="Alpha Vantage Market Data",
            description="Real-time and historical stock market data",
            endpoint_url="https://www.alphavantage.co/query",
            format=DataFormat.JSON,
            update_frequency="0 */4 * * *",  # Every 4 hours
            quality_threshold=0.95,
            rate_limit=5,  # 5 requests per minute
            compliance_tags=["financial", "public"]
        ))
        
        self.add_data_source(DataSourceConfig(
            source_id="fred_economic",
            source_type=DataSourceType.ECONOMIC_INDICATORS,
            name="FRED Economic Data",
            description="Federal Reserve Economic Data",
            endpoint_url="https://api.stlouisfed.org/fred",
            format=DataFormat.JSON,
            update_frequency="0 6 * * *",  # Daily at 6 AM
            quality_threshold=0.98,
            rate_limit=120,  # 120 requests per minute
            compliance_tags=["economic", "government", "public"]
        ))
        
        # Scientific Literature
        self.add_data_source(DataSourceConfig(
            source_id="arxiv_papers",
            source_type=DataSourceType.SCIENTIFIC_LITERATURE,
            name="arXiv Scientific Papers",
            description="Scientific papers from arXiv repository",
            endpoint_url="http://export.arxiv.org/api/query",
            format=DataFormat.XML,
            update_frequency="0 2 * * *",  # Daily at 2 AM
            quality_threshold=0.90,
            rate_limit=3,  # 3 requests per second
            compliance_tags=["academic", "public"]
        ))
        
        # Cryptocurrency Data
        self.add_data_source(DataSourceConfig(
            source_id="coingecko",
            source_type=DataSourceType.ALTERNATIVE_DATA,
            name="CoinGecko Crypto Data",
            description="Cryptocurrency market data and metrics",
            endpoint_url="https://api.coingecko.com/api/v3",
            format=DataFormat.JSON,
            update_frequency="*/15 * * * *",  # Every 15 minutes
            quality_threshold=0.92,
            rate_limit=50,  # 50 requests per minute
            compliance_tags=["crypto", "public"]
        ))
        
        # Real-time News Sentiment
        self.add_data_source(DataSourceConfig(
            source_id="news_sentiment",
            source_type=DataSourceType.ALTERNATIVE_DATA,
            name="Financial News Sentiment",
            description="Real-time financial news sentiment analysis",
            endpoint_url="https://newsapi.org/v2",
            format=DataFormat.JSON,
            update_frequency="*/30 * * * *",  # Every 30 minutes
            quality_threshold=0.85,
            rate_limit=1000,  # 1000 requests per day
            compliance_tags=["news", "sentiment", "public"]
        ))
    
    def add_data_source(self, config: DataSourceConfig):
        """Add a new data source configuration"""
        self.data_sources[config.source_id] = config
        logger.info(f"Added data source: {config.name} ({config.source_id})")
    
    def add_validation_rule(self, source_id: str, rule: DataValidationRule):
        """Add validation rule for a data source"""
        if source_id not in self.validation_rules:
            self.validation_rules[source_id] = []
        self.validation_rules[source_id].append(rule)
        logger.info(f"Added validation rule {rule.rule_id} for {source_id}")
    
    async def ingest_data(
        self,
        source_id: str,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> DataIngestionResult:
        """Ingest data from a specific source"""
        
        if source_id not in self.data_sources:
            raise ValueError(f"Unknown data source: {source_id}")
        
        config = self.data_sources[source_id]
        
        if not config.enabled:
            logger.warning(f"Data source {source_id} is disabled")
            return DataIngestionResult(
                source_id=source_id,
                success=False,
                records_processed=0,
                records_valid=0,
                records_invalid=0,
                quality_score=0.0,
                processing_time=0.0,
                data_size_mb=0.0,
                error_message="Data source is disabled"
            )
        
        start_time = datetime.now()
        
        try:
            # Fetch data from source
            raw_data = await self._fetch_data(config, custom_params)
            
            # Validate data quality
            validation_result = await self._validate_data(source_id, raw_data)
            
            # Process and transform data
            processed_data = await self._process_data(config, raw_data)
            
            # Store data
            storage_result = await self._store_data(config, processed_data)
            
            # Update metrics
            await self._update_metrics(source_id, validation_result, storage_result)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = DataIngestionResult(
                source_id=source_id,
                success=True,
                records_processed=len(processed_data) if processed_data else 0,
                records_valid=validation_result.get("valid_records", 0),
                records_invalid=validation_result.get("invalid_records", 0),
                quality_score=validation_result.get("quality_score", 0.0),
                processing_time=processing_time,
                data_size_mb=storage_result.get("size_mb", 0.0),
                metadata={
                    "source_config": config.source_id,
                    "validation_details": validation_result,
                    "storage_details": storage_result
                }
            )
            
            logger.info(
                f"Successfully ingested data from {source_id}: "
                f"{result.records_processed} records, "
                f"quality score: {result.quality_score:.2f}"
            )
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            
            logger.error(f"Data ingestion failed for {source_id}: {e}")
            
            return DataIngestionResult(
                source_id=source_id,
                success=False,
                records_processed=0,
                records_valid=0,
                records_invalid=0,
                quality_score=0.0,
                processing_time=processing_time,
                data_size_mb=0.0,
                error_message=str(e)
            )
    
    async def _fetch_data(
        self,
        config: DataSourceConfig,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Fetch data from external source"""
        
        headers = {
            "User-Agent": "NQBA-Platform/1.0",
            **config.custom_headers
        }
        
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"
        
        params = custom_params or {}
        
        timeout = aiohttp.ClientTimeout(total=config.timeout)
        
        async with aiohttp.ClientSession(timeout=timeout) as session:
            for attempt in range(config.retry_attempts):
                try:
                    async with session.get(
                        config.endpoint_url,
                        headers=headers,
                        params=params
                    ) as response:
                        response.raise_for_status()
                        
                        if config.format == DataFormat.JSON:
                            return await response.json()
                        elif config.format == DataFormat.TEXT:
                            return await response.text()
                        elif config.format == DataFormat.XML:
                            return await response.text()
                        else:
                            return await response.read()
                            
                except Exception as e:
                    if attempt == config.retry_attempts - 1:
                        raise
                    
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(
                        f"Fetch attempt {attempt + 1} failed for {config.source_id}, "
                        f"retrying in {wait_time}s: {e}"
                    )
                    await asyncio.sleep(wait_time)
    
    async def _validate_data(self, source_id: str, data: Any) -> Dict[str, Any]:
        """Validate data quality and compliance"""
        
        validation_result = {
            "valid_records": 0,
            "invalid_records": 0,
            "quality_score": 0.0,
            "validation_errors": [],
            "validation_warnings": []
        }
        
        if not data:
            validation_result["validation_errors"].append("No data received")
            return validation_result
        
        # Apply validation rules if configured
        if source_id in self.validation_rules:
            rules = self.validation_rules[source_id]
            
            for rule in rules:
                try:
                    rule_result = await self._apply_validation_rule(data, rule)
                    
                    if rule_result["passed"]:
                        validation_result["valid_records"] += rule_result.get("count", 1)
                    else:
                        validation_result["invalid_records"] += rule_result.get("count", 1)
                        
                        if rule.severity == "error":
                            validation_result["validation_errors"].append(
                                f"Rule {rule.rule_id}: {rule_result['message']}"
                            )
                        else:
                            validation_result["validation_warnings"].append(
                                f"Rule {rule.rule_id}: {rule_result['message']}"
                            )
                            
                except Exception as e:
                    validation_result["validation_errors"].append(
                        f"Validation rule {rule.rule_id} failed: {e}"
                    )
        
        # Calculate quality score
        total_records = validation_result["valid_records"] + validation_result["invalid_records"]
        if total_records > 0:
            validation_result["quality_score"] = validation_result["valid_records"] / total_records
        
        return validation_result
    
    async def _apply_validation_rule(self, data: Any, rule: DataValidationRule) -> Dict[str, Any]:
        """Apply a single validation rule"""
        
        if rule.rule_type == "required":
            if isinstance(data, dict):
                field_exists = rule.field_name in data and data[rule.field_name] is not None
                return {
                    "passed": field_exists,
                    "message": f"Required field {rule.field_name} {'found' if field_exists else 'missing'}",
                    "count": 1
                }
        
        elif rule.rule_type == "type":
            if isinstance(data, dict) and rule.field_name in data:
                expected_type = rule.parameters.get("type")
                actual_value = data[rule.field_name]
                type_match = isinstance(actual_value, expected_type)
                return {
                    "passed": type_match,
                    "message": f"Field {rule.field_name} type validation {'passed' if type_match else 'failed'}",
                    "count": 1
                }
        
        elif rule.rule_type == "range":
            if isinstance(data, dict) and rule.field_name in data:
                value = data[rule.field_name]
                min_val = rule.parameters.get("min")
                max_val = rule.parameters.get("max")
                
                in_range = True
                if min_val is not None and value < min_val:
                    in_range = False
                if max_val is not None and value > max_val:
                    in_range = False
                
                return {
                    "passed": in_range,
                    "message": f"Field {rule.field_name} range validation {'passed' if in_range else 'failed'}",
                    "count": 1
                }
        
        # Default: rule passed
        return {"passed": True, "message": "Rule applied successfully", "count": 1}
    
    async def _process_data(self, config: DataSourceConfig, raw_data: Any) -> List[Dict[str, Any]]:
        """Process and transform raw data"""
        
        if not raw_data:
            return []
        
        processed_data = []
        
        try:
            if config.format == DataFormat.JSON:
                if isinstance(raw_data, list):
                    processed_data = raw_data
                elif isinstance(raw_data, dict):
                    # Extract data array if nested
                    if "data" in raw_data:
                        processed_data = raw_data["data"]
                    elif "results" in raw_data:
                        processed_data = raw_data["results"]
                    else:
                        processed_data = [raw_data]
            
            elif config.format == DataFormat.CSV:
                # Convert CSV to list of dictionaries
                if isinstance(raw_data, str):
                    import io
                    df = pd.read_csv(io.StringIO(raw_data))
                    processed_data = df.to_dict("records")
            
            elif config.format == DataFormat.XML:
                # Basic XML processing (can be enhanced)
                import xml.etree.ElementTree as ET
                if isinstance(raw_data, str):
                    root = ET.fromstring(raw_data)
                    processed_data = [{"xml_content": raw_data}]
            
            # Add metadata to each record
            for record in processed_data:
                if isinstance(record, dict):
                    record["_metadata"] = {
                        "source_id": config.source_id,
                        "ingestion_timestamp": datetime.now().isoformat(),
                        "data_hash": hashlib.md5(
                            json.dumps(record, sort_keys=True).encode()
                        ).hexdigest()
                    }
            
            logger.info(f"Processed {len(processed_data)} records from {config.source_id}")
            
        except Exception as e:
            logger.error(f"Data processing failed for {config.source_id}: {e}")
            raise
        
        return processed_data
    
    async def _store_data(self, config: DataSourceConfig, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Store processed data"""
        
        if not data:
            return {"stored_records": 0, "size_mb": 0.0}
        
        # Create storage directory
        source_dir = self.storage_path / config.source_id
        source_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{config.source_id}_{timestamp}.json"
        file_path = source_dir / filename
        
        try:
            # Encrypt data if required
            if config.encryption_required:
                encrypted_data = await self.encryption.encrypt_data(json.dumps(data))
                with open(file_path.with_suffix(".enc"), "wb") as f:
                    f.write(encrypted_data)
            else:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2, default=str)
            
            # Calculate file size
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            
            # Store metadata in Redis
            metadata = {
                "source_id": config.source_id,
                "filename": filename,
                "record_count": len(data),
                "file_size_mb": file_size_mb,
                "encrypted": config.encryption_required,
                "timestamp": datetime.now().isoformat()
            }
            
            await self.redis_client.hset(
                f"training_data:{config.source_id}:{timestamp}",
                mapping=metadata
            )
            
            # Set expiration (30 days)
            await self.redis_client.expire(
                f"training_data:{config.source_id}:{timestamp}",
                30 * 24 * 3600
            )
            
            logger.info(
                f"Stored {len(data)} records from {config.source_id} "
                f"({file_size_mb:.2f} MB)"
            )
            
            return {
                "stored_records": len(data),
                "size_mb": file_size_mb,
                "file_path": str(file_path),
                "encrypted": config.encryption_required
            }
            
        except Exception as e:
            logger.error(f"Data storage failed for {config.source_id}: {e}")
            raise
    
    async def _update_metrics(self, source_id: str, validation_result: Dict, storage_result: Dict):
        """Update ingestion metrics"""
        
        self.stats["total_ingested"] += storage_result.get("stored_records", 0)
        self.stats["total_processed"] += validation_result.get("valid_records", 0)
        
        if validation_result.get("validation_errors"):
            self.stats["total_errors"] += len(validation_result["validation_errors"])
        
        # Update quality metrics
        quality_score = validation_result.get("quality_score", 0.0)
        self.quality_metrics[source_id] = quality_score
        
        # Calculate average quality
        if self.quality_metrics:
            self.stats["average_quality"] = sum(self.quality_metrics.values()) / len(self.quality_metrics)
        
        self.stats["last_update"] = datetime.now().isoformat()
        
        # Store metrics in Redis
        await self.redis_client.hset(
            "training_pipeline_stats",
            mapping={
                "total_ingested": self.stats["total_ingested"],
                "total_processed": self.stats["total_processed"],
                "total_errors": self.stats["total_errors"],
                "average_quality": self.stats["average_quality"],
                "last_update": self.stats["last_update"]
            }
        )
    
    async def ingest_all_sources(self) -> List[DataIngestionResult]:
        """Ingest data from all enabled sources"""
        
        results = []
        
        for source_id, config in self.data_sources.items():
            if config.enabled:
                try:
                    result = await self.ingest_data(source_id)
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to ingest from {source_id}: {e}")
                    results.append(DataIngestionResult(
                        source_id=source_id,
                        success=False,
                        records_processed=0,
                        records_valid=0,
                        records_invalid=0,
                        quality_score=0.0,
                        processing_time=0.0,
                        data_size_mb=0.0,
                        error_message=str(e)
                    ))
        
        logger.info(f"Completed ingestion from {len(results)} sources")
        return results
    
    async def get_ingestion_stats(self) -> Dict[str, Any]:
        """Get current ingestion statistics"""
        
        # Get latest stats from Redis
        redis_stats = await self.redis_client.hgetall("training_pipeline_stats")
        
        if redis_stats:
            return {
                "total_ingested": int(redis_stats.get("total_ingested", 0)),
                "total_processed": int(redis_stats.get("total_processed", 0)),
                "total_errors": int(redis_stats.get("total_errors", 0)),
                "average_quality": float(redis_stats.get("average_quality", 0.0)),
                "last_update": redis_stats.get("last_update"),
                "source_quality_metrics": self.quality_metrics,
                "active_sources": len([c for c in self.data_sources.values() if c.enabled]),
                "total_sources": len(self.data_sources)
            }
        
        return self.stats
    
    async def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old training data files"""
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleaned_files = 0
        
        for source_dir in self.storage_path.iterdir():
            if source_dir.is_dir():
                for file_path in source_dir.iterdir():
                    if file_path.is_file():
                        file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                        if file_time < cutoff_date:
                            file_path.unlink()
                            cleaned_files += 1
        
        logger.info(f"Cleaned up {cleaned_files} old training data files")
        return cleaned_files


# Example usage and testing
if __name__ == "__main__":
    async def test_pipeline():
        """Test the data ingestion pipeline"""
        
        # This would normally be injected
        from unittest.mock import AsyncMock
        
        pipeline = DataIngestionPipeline(
            db_session=AsyncMock(),
            redis_client=AsyncMock(),
            quantum_adapter=AsyncMock(),
            ltc_logger=logger,
            encryption=AsyncMock(),
            storage_path=Path("/tmp/test_training_data")
        )
        
        # Add validation rules
        pipeline.add_validation_rule(
            "alpha_vantage",
            DataValidationRule(
                rule_id="price_required",
                field_name="price",
                rule_type="required",
                parameters={},
                description="Price field is required"
            )
        )
        
        # Test ingestion (would need real API keys)
        # result = await pipeline.ingest_data("alpha_vantage")
        # print(f"Ingestion result: {result}")
        
        # Get stats
        stats = await pipeline.get_ingestion_stats()
        print(f"Pipeline stats: {stats}")
    
    # Run test
    # asyncio.run(test_pipeline())
    pass