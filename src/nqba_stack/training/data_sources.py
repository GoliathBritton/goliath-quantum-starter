"""Data Sources for NQBA Platform Training

This module provides access to real-world data sources for immediate platform
credibility and validation, including financial markets, scientific literature,
economic indicators, and quantum computing research data.
"""

import asyncio
import logging
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import aiohttp
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import feedparser
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
import arxiv
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData
from fredapi import Fred
import quandl

from ..core.ltc_logger import LTCLogger
from .data_ingestion_pipeline import DataSource, DataQuality

logger = LTCLogger("DataSources")


class DataSourceType(Enum):
    """Types of data sources"""
    
    FINANCIAL_MARKET = "financial_market"
    ECONOMIC_INDICATORS = "economic_indicators"
    SCIENTIFIC_LITERATURE = "scientific_literature"
    QUANTUM_RESEARCH = "quantum_research"
    CRYPTOCURRENCY = "cryptocurrency"
    COMMODITIES = "commodities"
    FOREX = "forex"
    NEWS_SENTIMENT = "news_sentiment"
    SOCIAL_MEDIA = "social_media"
    PATENT_DATA = "patent_data"
    RESEARCH_PAPERS = "research_papers"
    MARKET_VOLATILITY = "market_volatility"
    TRADING_VOLUME = "trading_volume"
    EARNINGS_DATA = "earnings_data"
    INSIDER_TRADING = "insider_trading"


class DataProvider(Enum):
    """Data providers"""
    
    YAHOO_FINANCE = "yahoo_finance"
    ALPHA_VANTAGE = "alpha_vantage"
    QUANDL = "quandl"
    FRED = "fred"  # Federal Reserve Economic Data
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    GOOGLE_SCHOLAR = "google_scholar"
    COINBASE = "coinbase"
    BINANCE = "binance"
    REUTERS = "reuters"
    BLOOMBERG = "bloomberg"
    TWITTER = "twitter"
    REDDIT = "reddit"
    USPTO = "uspto"  # US Patent Office
    SEMANTIC_SCHOLAR = "semantic_scholar"
    CROSSREF = "crossref"
    NATURE = "nature"
    SCIENCE = "science"
    IEEE = "ieee"
    ACM = "acm"


class DataFrequency(Enum):
    """Data update frequencies"""
    
    REAL_TIME = "real_time"
    MINUTE = "minute"
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    ON_DEMAND = "on_demand"


@dataclass
class DataSourceConfig:
    """Configuration for a data source"""
    
    source_id: str
    source_type: DataSourceType
    provider: DataProvider
    frequency: DataFrequency
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    rate_limit: int = 100  # requests per minute
    cost_per_request: float = 0.0
    quality_threshold: float = 0.8
    enabled: bool = True
    last_updated: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataRecord:
    """Individual data record"""
    
    record_id: str
    source_id: str
    timestamp: datetime
    data: Dict[str, Any]
    quality_score: float
    confidence: float
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataBatch:
    """Batch of data records"""
    
    batch_id: str
    source_id: str
    records: List[DataRecord]
    batch_timestamp: datetime
    total_records: int
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    processing_time: float = 0.0
    errors: List[str] = field(default_factory=list)


class RealTimeDataSources:
    """Manages real-time data sources for immediate platform credibility"""
    
    def __init__(
        self,
        db_session: AsyncSession,
        redis_client: Redis,
        ltc_logger: LTCLogger,
        config_path: Path = Path("/config/data_sources.yaml")
    ):
        self.db_session = db_session
        self.redis_client = redis_client
        self.ltc_logger = ltc_logger
        self.config_path = config_path
        
        # Data source configurations
        self.sources: Dict[str, DataSourceConfig] = {}
        
        # API clients
        self.session = None
        self.alpha_vantage_ts = None
        self.alpha_vantage_fd = None
        self.fred_client = None
        
        # Rate limiting
        self.rate_limiters: Dict[str, Dict[str, Any]] = {}
        
        # Data cache
        self.data_cache: Dict[str, Any] = {}
        self.cache_ttl = 300  # 5 minutes
        
        # Quality tracking
        self.quality_metrics: Dict[str, Dict[str, float]] = {}
        
        # Initialize sources
        asyncio.create_task(self._initialize_sources())
        
        logger.info("Real-time data sources initialized")
    
    async def _initialize_sources(self):
        """Initialize data sources and API clients"""
        
        try:
            # Create HTTP session
            self.session = aiohttp.ClientSession()
            
            # Initialize API clients
            await self._initialize_api_clients()
            
            # Load source configurations
            await self._load_source_configurations()
            
            # Start data collection tasks
            await self._start_collection_tasks()
            
            logger.info("Data sources initialization completed")
            
        except Exception as e:
            logger.error(f"Failed to initialize data sources: {e}")
    
    async def _initialize_api_clients(self):
        """Initialize API clients for various data providers"""
        
        try:
            # Alpha Vantage
            alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            if alpha_vantage_key:
                self.alpha_vantage_ts = TimeSeries(key=alpha_vantage_key, output_format='pandas')
                self.alpha_vantage_fd = FundamentalData(key=alpha_vantage_key, output_format='pandas')
                logger.info("Alpha Vantage client initialized")
            
            # FRED (Federal Reserve Economic Data)
            fred_key = os.getenv("FRED_API_KEY")
            if fred_key:
                self.fred_client = Fred(api_key=fred_key)
                logger.info("FRED client initialized")
            
            # Quandl
            quandl_key = os.getenv("QUANDL_API_KEY")
            if quandl_key:
                quandl.ApiConfig.api_key = quandl_key
                logger.info("Quandl client initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize API clients: {e}")
    
    async def _load_source_configurations(self):
        """Load data source configurations"""
        
        # Create default configurations for immediate credibility
        default_sources = {
            # Financial Market Data
            "sp500_realtime": DataSourceConfig(
                source_id="sp500_realtime",
                source_type=DataSourceType.FINANCIAL_MARKET,
                provider=DataProvider.YAHOO_FINANCE,
                frequency=DataFrequency.MINUTE,
                parameters={"symbols": ["SPY", "QQQ", "IWM", "VTI"]},
                rate_limit=2000
            ),
            "crypto_prices": DataSourceConfig(
                source_id="crypto_prices",
                source_type=DataSourceType.CRYPTOCURRENCY,
                provider=DataProvider.COINBASE,
                frequency=DataFrequency.MINUTE,
                parameters={"symbols": ["BTC-USD", "ETH-USD", "ADA-USD"]},
                rate_limit=1000
            ),
            "economic_indicators": DataSourceConfig(
                source_id="economic_indicators",
                source_type=DataSourceType.ECONOMIC_INDICATORS,
                provider=DataProvider.FRED,
                frequency=DataFrequency.DAILY,
                parameters={"series": ["GDP", "UNRATE", "CPIAUCSL", "FEDFUNDS"]},
                rate_limit=120
            ),
            "quantum_research": DataSourceConfig(
                source_id="quantum_research",
                source_type=DataSourceType.QUANTUM_RESEARCH,
                provider=DataProvider.ARXIV,
                frequency=DataFrequency.DAILY,
                parameters={"categories": ["quant-ph", "cs.ET", "physics.comp-ph"]},
                rate_limit=1000
            ),
            "market_volatility": DataSourceConfig(
                source_id="market_volatility",
                source_type=DataSourceType.MARKET_VOLATILITY,
                provider=DataProvider.ALPHA_VANTAGE,
                frequency=DataFrequency.HOURLY,
                parameters={"symbols": ["VIX", "VIXM", "VXST"]},
                rate_limit=500
            ),
            "earnings_data": DataSourceConfig(
                source_id="earnings_data",
                source_type=DataSourceType.EARNINGS_DATA,
                provider=DataProvider.ALPHA_VANTAGE,
                frequency=DataFrequency.DAILY,
                parameters={"symbols": ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]},
                rate_limit=500
            ),
            "scientific_papers": DataSourceConfig(
                source_id="scientific_papers",
                source_type=DataSourceType.SCIENTIFIC_LITERATURE,
                provider=DataProvider.SEMANTIC_SCHOLAR,
                frequency=DataFrequency.DAILY,
                parameters={"fields": ["machine learning", "quantum computing", "financial modeling"]},
                rate_limit=1000
            ),
            "news_sentiment": DataSourceConfig(
                source_id="news_sentiment",
                source_type=DataSourceType.NEWS_SENTIMENT,
                provider=DataProvider.REUTERS,
                frequency=DataFrequency.HOURLY,
                parameters={"topics": ["markets", "technology", "quantum", "AI"]},
                rate_limit=1000
            )
        }
        
        # Add API keys from environment
        for source_config in default_sources.values():
            if source_config.provider == DataProvider.ALPHA_VANTAGE:
                source_config.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
            elif source_config.provider == DataProvider.FRED:
                source_config.api_key = os.getenv("FRED_API_KEY")
            elif source_config.provider == DataProvider.QUANDL:
                source_config.api_key = os.getenv("QUANDL_API_KEY")
        
        self.sources = default_sources
        logger.info(f"Loaded {len(self.sources)} data source configurations")
    
    async def _start_collection_tasks(self):
        """Start data collection tasks for each source"""
        
        for source_id, config in self.sources.items():
            if config.enabled:
                # Create collection task based on frequency
                if config.frequency == DataFrequency.REAL_TIME:
                    asyncio.create_task(self._collect_realtime_data(source_id))
                elif config.frequency == DataFrequency.MINUTE:
                    asyncio.create_task(self._collect_periodic_data(source_id, 60))
                elif config.frequency == DataFrequency.HOURLY:
                    asyncio.create_task(self._collect_periodic_data(source_id, 3600))
                elif config.frequency == DataFrequency.DAILY:
                    asyncio.create_task(self._collect_periodic_data(source_id, 86400))
        
        logger.info("Data collection tasks started")
    
    async def collect_financial_data(self, symbols: List[str]) -> DataBatch:
        """Collect real-time financial market data"""
        
        try:
            records = []
            batch_id = f"financial_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for symbol in symbols:
                try:
                    # Get real-time data from Yahoo Finance
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    history = ticker.history(period="1d", interval="1m")
                    
                    if not history.empty:
                        latest = history.iloc[-1]
                        
                        record = DataRecord(
                            record_id=f"{symbol}_{datetime.now().isoformat()}",
                            source_id="sp500_realtime",
                            timestamp=datetime.now(),
                            data={
                                "symbol": symbol,
                                "price": float(latest['Close']),
                                "volume": int(latest['Volume']),
                                "high": float(latest['High']),
                                "low": float(latest['Low']),
                                "open": float(latest['Open']),
                                "market_cap": info.get('marketCap', 0),
                                "pe_ratio": info.get('trailingPE', 0),
                                "52_week_high": info.get('fiftyTwoWeekHigh', 0),
                                "52_week_low": info.get('fiftyTwoWeekLow', 0)
                            },
                            quality_score=0.95,
                            confidence=0.9,
                            tags=["financial", "real-time", "market"]
                        )
                        
                        records.append(record)
                        
                except Exception as e:
                    logger.warning(f"Failed to collect data for {symbol}: {e}")
            
            batch = DataBatch(
                batch_id=batch_id,
                source_id="sp500_realtime",
                records=records,
                batch_timestamp=datetime.now(),
                total_records=len(records),
                quality_metrics={"completeness": len(records) / len(symbols)}
            )
            
            # Store in cache and Redis
            await self._store_batch(batch)
            
            logger.info(f"Collected financial data for {len(records)} symbols")
            return batch
            
        except Exception as e:
            logger.error(f"Failed to collect financial data: {e}")
            return DataBatch(
                batch_id=f"financial_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                source_id="sp500_realtime",
                records=[],
                batch_timestamp=datetime.now(),
                total_records=0,
                errors=[str(e)]
            )
    
    async def collect_crypto_data(self, symbols: List[str]) -> DataBatch:
        """Collect cryptocurrency market data"""
        
        try:
            records = []
            batch_id = f"crypto_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Use Coinbase Pro API
            base_url = "https://api.pro.coinbase.com"
            
            for symbol in symbols:
                try:
                    # Get ticker data
                    async with self.session.get(f"{base_url}/products/{symbol}/ticker") as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            record = DataRecord(
                                record_id=f"{symbol}_{datetime.now().isoformat()}",
                                source_id="crypto_prices",
                                timestamp=datetime.now(),
                                data={
                                    "symbol": symbol,
                                    "price": float(data.get('price', 0)),
                                    "volume_24h": float(data.get('volume', 0)),
                                    "bid": float(data.get('bid', 0)),
                                    "ask": float(data.get('ask', 0)),
                                    "size": float(data.get('size', 0))
                                },
                                quality_score=0.92,
                                confidence=0.88,
                                tags=["cryptocurrency", "real-time", "market"]
                            )
                            
                            records.append(record)
                            
                except Exception as e:
                    logger.warning(f"Failed to collect crypto data for {symbol}: {e}")
            
            batch = DataBatch(
                batch_id=batch_id,
                source_id="crypto_prices",
                records=records,
                batch_timestamp=datetime.now(),
                total_records=len(records),
                quality_metrics={"completeness": len(records) / len(symbols)}
            )
            
            await self._store_batch(batch)
            
            logger.info(f"Collected crypto data for {len(records)} symbols")
            return batch
            
        except Exception as e:
            logger.error(f"Failed to collect crypto data: {e}")
            return DataBatch(
                batch_id=f"crypto_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                source_id="crypto_prices",
                records=[],
                batch_timestamp=datetime.now(),
                total_records=0,
                errors=[str(e)]
            )
    
    async def collect_economic_indicators(self, series_ids: List[str]) -> DataBatch:
        """Collect economic indicators from FRED"""
        
        try:
            records = []
            batch_id = f"economic_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            if self.fred_client:
                for series_id in series_ids:
                    try:
                        # Get latest data point
                        data = self.fred_client.get_series(series_id, limit=1)
                        
                        if not data.empty:
                            latest_value = data.iloc[-1]
                            latest_date = data.index[-1]
                            
                            # Get series info
                            info = self.fred_client.get_series_info(series_id)
                            
                            record = DataRecord(
                                record_id=f"{series_id}_{datetime.now().isoformat()}",
                                source_id="economic_indicators",
                                timestamp=datetime.now(),
                                data={
                                    "series_id": series_id,
                                    "value": float(latest_value),
                                    "date": latest_date.isoformat(),
                                    "title": info.get('title', ''),
                                    "units": info.get('units', ''),
                                    "frequency": info.get('frequency', ''),
                                    "seasonal_adjustment": info.get('seasonal_adjustment', '')
                                },
                                quality_score=0.98,
                                confidence=0.95,
                                tags=["economic", "indicator", "government"]
                            )
                            
                            records.append(record)
                            
                    except Exception as e:
                        logger.warning(f"Failed to collect economic data for {series_id}: {e}")
            
            batch = DataBatch(
                batch_id=batch_id,
                source_id="economic_indicators",
                records=records,
                batch_timestamp=datetime.now(),
                total_records=len(records),
                quality_metrics={"completeness": len(records) / len(series_ids)}
            )
            
            await self._store_batch(batch)
            
            logger.info(f"Collected economic indicators for {len(records)} series")
            return batch
            
        except Exception as e:
            logger.error(f"Failed to collect economic indicators: {e}")
            return DataBatch(
                batch_id=f"economic_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                source_id="economic_indicators",
                records=[],
                batch_timestamp=datetime.now(),
                total_records=0,
                errors=[str(e)]
            )
    
    async def collect_quantum_research(self, categories: List[str]) -> DataBatch:
        """Collect quantum computing research papers from arXiv"""
        
        try:
            records = []
            batch_id = f"quantum_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            for category in categories:
                try:
                    # Search for recent papers in category
                    search = arxiv.Search(
                        query=f"cat:{category}",
                        max_results=10,
                        sort_by=arxiv.SortCriterion.SubmittedDate,
                        sort_order=arxiv.SortOrder.Descending
                    )
                    
                    for paper in search.results():
                        record = DataRecord(
                            record_id=f"arxiv_{paper.entry_id.split('/')[-1]}",
                            source_id="quantum_research",
                            timestamp=datetime.now(),
                            data={
                                "arxiv_id": paper.entry_id.split('/')[-1],
                                "title": paper.title,
                                "authors": [str(author) for author in paper.authors],
                                "abstract": paper.summary,
                                "categories": paper.categories,
                                "published": paper.published.isoformat(),
                                "updated": paper.updated.isoformat(),
                                "pdf_url": paper.pdf_url,
                                "primary_category": paper.primary_category
                            },
                            quality_score=0.90,
                            confidence=0.85,
                            tags=["quantum", "research", "arxiv", category]
                        )
                        
                        records.append(record)
                        
                except Exception as e:
                    logger.warning(f"Failed to collect quantum research for {category}: {e}")
            
            batch = DataBatch(
                batch_id=batch_id,
                source_id="quantum_research",
                records=records,
                batch_timestamp=datetime.now(),
                total_records=len(records),
                quality_metrics={"completeness": 1.0 if records else 0.0}
            )
            
            await self._store_batch(batch)
            
            logger.info(f"Collected {len(records)} quantum research papers")
            return batch
            
        except Exception as e:
            logger.error(f"Failed to collect quantum research: {e}")
            return DataBatch(
                batch_id=f"quantum_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                source_id="quantum_research",
                records=[],
                batch_timestamp=datetime.now(),
                total_records=0,
                errors=[str(e)]
            )
    
    async def collect_market_sentiment(self, topics: List[str]) -> DataBatch:
        """Collect market sentiment from news sources"""
        
        try:
            records = []
            batch_id = f"sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Use RSS feeds for news sentiment
            news_feeds = {
                "reuters_markets": "https://feeds.reuters.com/reuters/businessNews",
                "reuters_tech": "https://feeds.reuters.com/reuters/technologyNews",
                "bloomberg_markets": "https://feeds.bloomberg.com/markets/news.rss"
            }
            
            for feed_name, feed_url in news_feeds.items():
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:5]:  # Latest 5 articles
                        # Simple sentiment analysis (would use proper NLP in production)
                        sentiment_score = self._analyze_sentiment(entry.title + " " + entry.summary)
                        
                        record = DataRecord(
                            record_id=f"{feed_name}_{entry.id}",
                            source_id="news_sentiment",
                            timestamp=datetime.now(),
                            data={
                                "source": feed_name,
                                "title": entry.title,
                                "summary": entry.summary,
                                "link": entry.link,
                                "published": entry.published,
                                "sentiment_score": sentiment_score,
                                "sentiment_label": "positive" if sentiment_score > 0.1 else "negative" if sentiment_score < -0.1 else "neutral"
                            },
                            quality_score=0.85,
                            confidence=0.75,
                            tags=["news", "sentiment", "market", feed_name]
                        )
                        
                        records.append(record)
                        
                except Exception as e:
                    logger.warning(f"Failed to collect sentiment from {feed_name}: {e}")
            
            batch = DataBatch(
                batch_id=batch_id,
                source_id="news_sentiment",
                records=records,
                batch_timestamp=datetime.now(),
                total_records=len(records),
                quality_metrics={"completeness": 1.0 if records else 0.0}
            )
            
            await self._store_batch(batch)
            
            logger.info(f"Collected {len(records)} sentiment records")
            return batch
            
        except Exception as e:
            logger.error(f"Failed to collect market sentiment: {e}")
            return DataBatch(
                batch_id=f"sentiment_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                source_id="news_sentiment",
                records=[],
                batch_timestamp=datetime.now(),
                total_records=0,
                errors=[str(e)]
            )
    
    def _analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (placeholder for proper NLP)"""
        
        positive_words = ['growth', 'profit', 'gain', 'rise', 'increase', 'bull', 'positive', 'strong']
        negative_words = ['loss', 'decline', 'fall', 'decrease', 'bear', 'negative', 'weak', 'crash']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        return (positive_count - negative_count) / total_words
    
    async def _store_batch(self, batch: DataBatch):
        """Store data batch in cache and Redis"""
        
        try:
            # Store in local cache
            self.data_cache[batch.batch_id] = batch
            
            # Store in Redis
            batch_data = {
                "batch_id": batch.batch_id,
                "source_id": batch.source_id,
                "timestamp": batch.batch_timestamp.isoformat(),
                "total_records": batch.total_records,
                "quality_metrics": json.dumps(batch.quality_metrics),
                "records": json.dumps([{
                    "record_id": r.record_id,
                    "timestamp": r.timestamp.isoformat(),
                    "data": r.data,
                    "quality_score": r.quality_score,
                    "confidence": r.confidence,
                    "tags": r.tags
                } for r in batch.records])
            }
            
            await self.redis_client.hset(
                f"data_batch:{batch.batch_id}",
                mapping=batch_data
            )
            
            # Set expiration
            await self.redis_client.expire(f"data_batch:{batch.batch_id}", self.cache_ttl)
            
            # Update source metrics
            await self._update_source_metrics(batch.source_id, batch)
            
        except Exception as e:
            logger.error(f"Failed to store batch {batch.batch_id}: {e}")
    
    async def _update_source_metrics(self, source_id: str, batch: DataBatch):
        """Update quality metrics for data source"""
        
        try:
            if source_id not in self.quality_metrics:
                self.quality_metrics[source_id] = {
                    "total_batches": 0,
                    "total_records": 0,
                    "avg_quality": 0.0,
                    "avg_confidence": 0.0,
                    "error_rate": 0.0
                }
            
            metrics = self.quality_metrics[source_id]
            
            # Update metrics
            metrics["total_batches"] += 1
            metrics["total_records"] += batch.total_records
            
            if batch.records:
                avg_quality = sum(r.quality_score for r in batch.records) / len(batch.records)
                avg_confidence = sum(r.confidence for r in batch.records) / len(batch.records)
                
                # Running average
                metrics["avg_quality"] = (
                    (metrics["avg_quality"] * (metrics["total_batches"] - 1) + avg_quality) /
                    metrics["total_batches"]
                )
                metrics["avg_confidence"] = (
                    (metrics["avg_confidence"] * (metrics["total_batches"] - 1) + avg_confidence) /
                    metrics["total_batches"]
                )
            
            # Error rate
            if batch.errors:
                metrics["error_rate"] = len(batch.errors) / max(batch.total_records, 1)
            
            # Store in Redis
            await self.redis_client.hset(
                f"source_metrics:{source_id}",
                mapping={k: str(v) for k, v in metrics.items()}
            )
            
        except Exception as e:
            logger.error(f"Failed to update source metrics for {source_id}: {e}")
    
    async def get_latest_data(self, source_id: str, limit: int = 100) -> List[DataRecord]:
        """Get latest data records from a source"""
        
        try:
            # Check cache first
            records = []
            
            for batch in self.data_cache.values():
                if batch.source_id == source_id:
                    records.extend(batch.records)
            
            # Sort by timestamp and limit
            records.sort(key=lambda r: r.timestamp, reverse=True)
            return records[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get latest data for {source_id}: {e}")
            return []
    
    async def get_data_quality_report(self) -> Dict[str, Any]:
        """Get comprehensive data quality report"""
        
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "sources": {},
                "overall_metrics": {
                    "total_sources": len(self.sources),
                    "active_sources": len([s for s in self.sources.values() if s.enabled]),
                    "total_records_collected": 0,
                    "avg_quality_score": 0.0,
                    "avg_confidence_score": 0.0
                }
            }
            
            total_records = 0
            total_quality = 0.0
            total_confidence = 0.0
            
            for source_id, metrics in self.quality_metrics.items():
                source_config = self.sources.get(source_id)
                
                report["sources"][source_id] = {
                    "source_type": source_config.source_type.value if source_config else "unknown",
                    "provider": source_config.provider.value if source_config else "unknown",
                    "enabled": source_config.enabled if source_config else False,
                    "total_batches": metrics["total_batches"],
                    "total_records": metrics["total_records"],
                    "avg_quality": metrics["avg_quality"],
                    "avg_confidence": metrics["avg_confidence"],
                    "error_rate": metrics["error_rate"],
                    "last_updated": source_config.last_updated.isoformat() if source_config and source_config.last_updated else None
                }
                
                total_records += metrics["total_records"]
                total_quality += metrics["avg_quality"] * metrics["total_records"]
                total_confidence += metrics["avg_confidence"] * metrics["total_records"]
            
            # Calculate overall metrics
            if total_records > 0:
                report["overall_metrics"]["total_records_collected"] = total_records
                report["overall_metrics"]["avg_quality_score"] = total_quality / total_records
                report["overall_metrics"]["avg_confidence_score"] = total_confidence / total_records
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate data quality report: {e}")
            return {"error": str(e)}
    
    # Collection task methods
    async def _collect_realtime_data(self, source_id: str):
        """Collect real-time data continuously"""
        
        while True:
            try:
                config = self.sources.get(source_id)
                if not config or not config.enabled:
                    await asyncio.sleep(60)
                    continue
                
                # Collect based on source type
                if config.source_type == DataSourceType.FINANCIAL_MARKET:
                    await self.collect_financial_data(config.parameters.get("symbols", []))
                elif config.source_type == DataSourceType.CRYPTOCURRENCY:
                    await self.collect_crypto_data(config.parameters.get("symbols", []))
                
                await asyncio.sleep(1)  # Real-time collection
                
            except Exception as e:
                logger.error(f"Real-time collection error for {source_id}: {e}")
                await asyncio.sleep(60)
    
    async def _collect_periodic_data(self, source_id: str, interval_seconds: int):
        """Collect data at periodic intervals"""
        
        while True:
            try:
                config = self.sources.get(source_id)
                if not config or not config.enabled:
                    await asyncio.sleep(interval_seconds)
                    continue
                
                # Collect based on source type
                if config.source_type == DataSourceType.ECONOMIC_INDICATORS:
                    await self.collect_economic_indicators(config.parameters.get("series", []))
                elif config.source_type == DataSourceType.QUANTUM_RESEARCH:
                    await self.collect_quantum_research(config.parameters.get("categories", []))
                elif config.source_type == DataSourceType.NEWS_SENTIMENT:
                    await self.collect_market_sentiment(config.parameters.get("topics", []))
                elif config.source_type == DataSourceType.FINANCIAL_MARKET:
                    await self.collect_financial_data(config.parameters.get("symbols", []))
                elif config.source_type == DataSourceType.CRYPTOCURRENCY:
                    await self.collect_crypto_data(config.parameters.get("symbols", []))
                
                # Update last updated timestamp
                config.last_updated = datetime.now()
                
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Periodic collection error for {source_id}: {e}")
                await asyncio.sleep(interval_seconds)
    
    async def cleanup(self):
        """Cleanup resources"""
        
        try:
            if self.session:
                await self.session.close()
            
            logger.info("Data sources cleanup completed")
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")


# Example usage
if __name__ == "__main__":
    async def test_data_sources():
        """Test the data sources"""
        
        from unittest.mock import AsyncMock
        
        data_sources = RealTimeDataSources(
            db_session=AsyncMock(),
            redis_client=AsyncMock(),
            ltc_logger=logger
        )
        
        # Wait for initialization
        await asyncio.sleep(2)
        
        # Test financial data collection
        financial_batch = await data_sources.collect_financial_data(["AAPL", "GOOGL"])
        print(f"Financial batch: {financial_batch.total_records} records")
        
        # Test quality report
        report = await data_sources.get_data_quality_report()
        print(f"Quality report: {report}")
        
        # Cleanup
        await data_sources.cleanup()
    
    # Run test
    # asyncio.run(test_data_sources())
    pass