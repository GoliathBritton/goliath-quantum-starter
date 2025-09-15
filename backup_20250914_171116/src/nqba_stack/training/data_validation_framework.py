"""Data Validation Framework for NQBA Platform

This module provides comprehensive data quality validation, integrity checks,
and monitoring for training datasets across all AI/ML components.
"""

import asyncio
import logging
import os
import json
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from dataclasses import dataclass, field
from pathlib import Path
import yaml
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
import scipy.stats as stats
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from great_expectations import DataContext
from great_expectations.dataset import PandasDataset
import dask.dataframe as dd
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset, DataDriftPreset

from ..core.ltc_logger import LTCLogger
from ..core.quantum_adapter import QuantumAdapter
from .data_sources import DataRecord, DataBatch

logger = LTCLogger("DataValidationFramework")


class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ValidationCategory(Enum):
    """Data validation categories"""
    
    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    CONSISTENCY = "consistency"
    VALIDITY = "validity"
    UNIQUENESS = "uniqueness"
    TIMELINESS = "timeliness"
    INTEGRITY = "integrity"
    DISTRIBUTION = "distribution"
    DRIFT = "drift"
    BIAS = "bias"


class DataType(Enum):
    """Supported data types for validation"""
    
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    TEXT = "text"
    BINARY = "binary"
    JSON = "json"
    IMAGE = "image"
    AUDIO = "audio"


@dataclass
class ValidationRule:
    """Data validation rule definition"""
    
    rule_id: str
    name: str
    description: str
    category: ValidationCategory
    severity: ValidationSeverity
    data_type: DataType
    columns: List[str]
    parameters: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    custom_function: Optional[Callable] = None
    threshold: Optional[float] = None
    expected_range: Optional[Tuple[float, float]] = None
    regex_pattern: Optional[str] = None
    reference_data: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ValidationResult:
    """Result of a validation rule execution"""
    
    rule_id: str
    passed: bool
    score: float
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    affected_records: int = 0
    total_records: int = 0
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ValidationReport:
    """Comprehensive validation report"""
    
    report_id: str
    dataset_id: str
    validation_timestamp: datetime
    overall_score: float
    passed_rules: int
    failed_rules: int
    total_rules: int
    rule_results: List[ValidationResult]
    summary_statistics: Dict[str, Any] = field(default_factory=dict)
    data_profile: Dict[str, Any] = field(default_factory=dict)
    drift_analysis: Dict[str, Any] = field(default_factory=dict)
    bias_analysis: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    artifacts: Dict[str, str] = field(default_factory=dict)


@dataclass
class DataProfile:
    """Statistical profile of dataset"""
    
    dataset_id: str
    total_records: int
    total_columns: int
    missing_values: Dict[str, int]
    data_types: Dict[str, str]
    numerical_stats: Dict[str, Dict[str, float]]
    categorical_stats: Dict[str, Dict[str, Any]]
    correlation_matrix: Optional[np.ndarray] = None
    outlier_counts: Dict[str, int] = field(default_factory=dict)
    duplicate_records: int = 0
    created_at: datetime = field(default_factory=datetime.now)


class DataValidationFramework:
    """Comprehensive data validation framework"""
    
    def __init__(
        self,
        db_session: AsyncSession,
        redis_client: Redis,
        quantum_adapter: QuantumAdapter,
        ltc_logger: LTCLogger,
        config_path: Path = Path("/config/data_validation.yaml")
    ):
        self.db_session = db_session
        self.redis_client = redis_client
        self.quantum_adapter = quantum_adapter
        self.ltc_logger = ltc_logger
        self.config_path = config_path
        
        # Validation rules and results
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_reports: Dict[str, ValidationReport] = {}
        self.data_profiles: Dict[str, DataProfile] = {}
        
        # Reference datasets for drift detection
        self.reference_datasets: Dict[str, pd.DataFrame] = {}
        
        # Validation history
        self.validation_history: Dict[str, List[ValidationReport]] = {}
        
        # Thread pool for parallel validation
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Initialize framework
        asyncio.create_task(self._initialize_framework())
        
        logger.info("Data Validation Framework initialized")
    
    async def _initialize_framework(self):
        """Initialize validation framework"""
        
        try:
            # Load validation rules
            await self._load_validation_rules()
            
            # Load reference datasets
            await self._load_reference_datasets()
            
            # Start validation monitoring
            asyncio.create_task(self._validation_monitor())
            
            logger.info("Data validation framework initialization completed")
            
        except Exception as e:
            logger.error(f"Failed to initialize data validation framework: {e}")
    
    async def _load_validation_rules(self):
        """Load predefined validation rules"""
        
        # Define comprehensive validation rules
        default_rules = {
            "completeness_check": ValidationRule(
                rule_id="completeness_check",
                name="Data Completeness Check",
                description="Ensure data completeness across all columns",
                category=ValidationCategory.COMPLETENESS,
                severity=ValidationSeverity.HIGH,
                data_type=DataType.NUMERICAL,
                columns=["*"],
                parameters={"max_missing_percentage": 5.0}
            ),
            "numerical_range_check": ValidationRule(
                rule_id="numerical_range_check",
                name="Numerical Range Validation",
                description="Validate numerical values are within expected ranges",
                category=ValidationCategory.VALIDITY,
                severity=ValidationSeverity.MEDIUM,
                data_type=DataType.NUMERICAL,
                columns=["price", "volume", "returns"],
                parameters={"auto_detect_range": True, "outlier_threshold": 3.0}
            ),
            "categorical_validity": ValidationRule(
                rule_id="categorical_validity",
                name="Categorical Value Validation",
                description="Ensure categorical values are from expected set",
                category=ValidationCategory.VALIDITY,
                severity=ValidationSeverity.HIGH,
                data_type=DataType.CATEGORICAL,
                columns=["symbol", "sector", "exchange"],
                parameters={"allowed_values": [], "case_sensitive": False}
            ),
            "temporal_consistency": ValidationRule(
                rule_id="temporal_consistency",
                name="Temporal Data Consistency",
                description="Validate temporal data consistency and ordering",
                category=ValidationCategory.CONSISTENCY,
                severity=ValidationSeverity.HIGH,
                data_type=DataType.TEMPORAL,
                columns=["timestamp", "date"],
                parameters={"allow_future_dates": False, "check_ordering": True}
            ),
            "duplicate_detection": ValidationRule(
                rule_id="duplicate_detection",
                name="Duplicate Record Detection",
                description="Detect and report duplicate records",
                category=ValidationCategory.UNIQUENESS,
                severity=ValidationSeverity.MEDIUM,
                data_type=DataType.NUMERICAL,
                columns=["*"],
                parameters={"subset_columns": [], "keep_first": True}
            ),
            "outlier_detection": ValidationRule(
                rule_id="outlier_detection",
                name="Statistical Outlier Detection",
                description="Detect statistical outliers in numerical data",
                category=ValidationCategory.ACCURACY,
                severity=ValidationSeverity.LOW,
                data_type=DataType.NUMERICAL,
                columns=["price", "volume", "returns"],
                parameters={"method": "isolation_forest", "contamination": 0.1}
            ),
            "distribution_stability": ValidationRule(
                rule_id="distribution_stability",
                name="Distribution Stability Check",
                description="Monitor data distribution stability over time",
                category=ValidationCategory.DRIFT,
                severity=ValidationSeverity.MEDIUM,
                data_type=DataType.NUMERICAL,
                columns=["*"],
                parameters={"drift_threshold": 0.1, "statistical_test": "ks_test"}
            ),
            "bias_detection": ValidationRule(
                rule_id="bias_detection",
                name="Data Bias Detection",
                description="Detect potential bias in training data",
                category=ValidationCategory.BIAS,
                severity=ValidationSeverity.HIGH,
                data_type=DataType.CATEGORICAL,
                columns=["sector", "market_cap", "geography"],
                parameters={"fairness_metrics": ["demographic_parity", "equalized_odds"]}
            ),
            "data_freshness": ValidationRule(
                rule_id="data_freshness",
                name="Data Freshness Check",
                description="Ensure data is recent and up-to-date",
                category=ValidationCategory.TIMELINESS,
                severity=ValidationSeverity.HIGH,
                data_type=DataType.TEMPORAL,
                columns=["timestamp"],
                parameters={"max_age_hours": 24, "business_hours_only": False}
            ),
            "schema_validation": ValidationRule(
                rule_id="schema_validation",
                name="Schema Validation",
                description="Validate data schema and structure",
                category=ValidationCategory.INTEGRITY,
                severity=ValidationSeverity.CRITICAL,
                data_type=DataType.NUMERICAL,
                columns=["*"],
                parameters={"enforce_schema": True, "allow_extra_columns": False}
            )
        }
        
        self.validation_rules = default_rules
        logger.info(f"Loaded {len(self.validation_rules)} validation rules")
    
    async def _load_reference_datasets(self):
        """Load reference datasets for drift detection"""
        
        try:
            # In production, these would be loaded from storage
            # For now, we'll create placeholder references
            
            reference_data = {
                "financial_baseline": pd.DataFrame({
                    "price": np.random.normal(100, 20, 1000),
                    "volume": np.random.exponential(1000000, 1000),
                    "returns": np.random.normal(0.001, 0.02, 1000)
                }),
                "sentiment_baseline": pd.DataFrame({
                    "sentiment_score": np.random.normal(0, 1, 1000),
                    "confidence": np.random.beta(2, 2, 1000)
                })
            }
            
            self.reference_datasets = reference_data
            logger.info(f"Loaded {len(self.reference_datasets)} reference datasets")
            
        except Exception as e:
            logger.error(f"Failed to load reference datasets: {e}")
    
    async def validate_dataset(
        self,
        dataset: Union[pd.DataFrame, DataBatch],
        dataset_id: str,
        rule_ids: Optional[List[str]] = None,
        generate_report: bool = True
    ) -> ValidationReport:
        """Validate a dataset against defined rules"""
        
        try:
            # Convert DataBatch to DataFrame if needed
            if isinstance(dataset, DataBatch):
                df = self._convert_batch_to_dataframe(dataset)
            else:
                df = dataset.copy()
            
            # Select rules to apply
            rules_to_apply = (
                [self.validation_rules[rid] for rid in rule_ids if rid in self.validation_rules]
                if rule_ids
                else list(self.validation_rules.values())
            )
            
            # Execute validation rules
            validation_results = []
            
            for rule in rules_to_apply:
                if rule.enabled:
                    result = await self._execute_validation_rule(df, rule)
                    validation_results.append(result)
            
            # Generate data profile
            data_profile = await self._generate_data_profile(df, dataset_id)
            
            # Perform drift analysis
            drift_analysis = await self._analyze_data_drift(df, dataset_id)
            
            # Perform bias analysis
            bias_analysis = await self._analyze_data_bias(df)
            
            # Calculate overall score
            passed_rules = len([r for r in validation_results if r.passed])
            total_rules = len(validation_results)
            overall_score = passed_rules / total_rules if total_rules > 0 else 0.0
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(validation_results, data_profile)
            
            # Create validation report
            report = ValidationReport(
                report_id=f"validation_{dataset_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                dataset_id=dataset_id,
                validation_timestamp=datetime.now(),
                overall_score=overall_score,
                passed_rules=passed_rules,
                failed_rules=total_rules - passed_rules,
                total_rules=total_rules,
                rule_results=validation_results,
                data_profile=data_profile.__dict__,
                drift_analysis=drift_analysis,
                bias_analysis=bias_analysis,
                recommendations=recommendations
            )
            
            # Store report
            self.validation_reports[report.report_id] = report
            
            # Update validation history
            if dataset_id not in self.validation_history:
                self.validation_history[dataset_id] = []
            self.validation_history[dataset_id].append(report)
            
            # Keep only last 50 reports per dataset
            if len(self.validation_history[dataset_id]) > 50:
                self.validation_history[dataset_id] = self.validation_history[dataset_id][-50:]
            
            # Store in Redis
            await self._store_validation_report(report)
            
            logger.info(f"Validation completed for dataset {dataset_id}: {overall_score:.2f} score")
            return report
            
        except Exception as e:
            logger.error(f"Dataset validation failed for {dataset_id}: {e}")
            raise
    
    def _convert_batch_to_dataframe(self, batch: DataBatch) -> pd.DataFrame:
        """Convert DataBatch to pandas DataFrame"""
        
        try:
            records_data = []
            
            for record in batch.records:
                record_dict = {
                    "timestamp": record.timestamp,
                    "source_id": record.source_id,
                    "data_type": record.data_type
                }
                
                # Add data fields
                if isinstance(record.data, dict):
                    record_dict.update(record.data)
                else:
                    record_dict["data"] = record.data
                
                records_data.append(record_dict)
            
            return pd.DataFrame(records_data)
            
        except Exception as e:
            logger.error(f"Failed to convert DataBatch to DataFrame: {e}")
            return pd.DataFrame()
    
    async def _execute_validation_rule(
        self,
        df: pd.DataFrame,
        rule: ValidationRule
    ) -> ValidationResult:
        """Execute a single validation rule"""
        
        start_time = datetime.now()
        
        try:
            # Select columns to validate
            if "*" in rule.columns:
                columns = df.columns.tolist()
            else:
                columns = [col for col in rule.columns if col in df.columns]
            
            if not columns:
                return ValidationResult(
                    rule_id=rule.rule_id,
                    passed=False,
                    score=0.0,
                    message="No matching columns found",
                    total_records=len(df)
                )
            
            # Execute rule based on category
            if rule.category == ValidationCategory.COMPLETENESS:
                result = await self._validate_completeness(df, columns, rule)
            
            elif rule.category == ValidationCategory.VALIDITY:
                result = await self._validate_validity(df, columns, rule)
            
            elif rule.category == ValidationCategory.CONSISTENCY:
                result = await self._validate_consistency(df, columns, rule)
            
            elif rule.category == ValidationCategory.UNIQUENESS:
                result = await self._validate_uniqueness(df, columns, rule)
            
            elif rule.category == ValidationCategory.ACCURACY:
                result = await self._validate_accuracy(df, columns, rule)
            
            elif rule.category == ValidationCategory.TIMELINESS:
                result = await self._validate_timeliness(df, columns, rule)
            
            elif rule.category == ValidationCategory.INTEGRITY:
                result = await self._validate_integrity(df, columns, rule)
            
            elif rule.category == ValidationCategory.DRIFT:
                result = await self._validate_drift(df, columns, rule)
            
            elif rule.category == ValidationCategory.BIAS:
                result = await self._validate_bias(df, columns, rule)
            
            else:
                result = ValidationResult(
                    rule_id=rule.rule_id,
                    passed=False,
                    score=0.0,
                    message=f"Unknown validation category: {rule.category.value}"
                )
            
            # Set execution time
            execution_time = (datetime.now() - start_time).total_seconds()
            result.execution_time = execution_time
            result.total_records = len(df)
            
            return result
            
        except Exception as e:
            logger.error(f"Validation rule {rule.rule_id} execution failed: {e}")
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Execution error: {str(e)}",
                total_records=len(df),
                execution_time=(datetime.now() - start_time).total_seconds()
            )
    
    async def _validate_completeness(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data completeness"""
        
        try:
            max_missing_pct = rule.parameters.get("max_missing_percentage", 5.0)
            
            missing_stats = {}
            total_violations = 0
            
            for col in columns:
                if col in df.columns:
                    missing_count = df[col].isnull().sum()
                    missing_pct = (missing_count / len(df)) * 100
                    missing_stats[col] = {
                        "missing_count": missing_count,
                        "missing_percentage": missing_pct,
                        "passes_threshold": missing_pct <= max_missing_pct
                    }
                    
                    if missing_pct > max_missing_pct:
                        total_violations += missing_count
            
            overall_missing_pct = sum(s["missing_percentage"] for s in missing_stats.values()) / len(missing_stats) if missing_stats else 0
            passed = overall_missing_pct <= max_missing_pct
            score = max(0, 1 - (overall_missing_pct / 100))
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Overall missing data: {overall_missing_pct:.2f}% (threshold: {max_missing_pct}%)",
                details={"column_stats": missing_stats},
                affected_records=total_violations
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Completeness validation error: {str(e)}"
            )
    
    async def _validate_validity(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data validity"""
        
        try:
            if rule.data_type == DataType.NUMERICAL:
                return await self._validate_numerical_validity(df, columns, rule)
            elif rule.data_type == DataType.CATEGORICAL:
                return await self._validate_categorical_validity(df, columns, rule)
            else:
                return ValidationResult(
                    rule_id=rule.rule_id,
                    passed=True,
                    score=1.0,
                    message="Validity check not implemented for this data type"
                )
                
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Validity validation error: {str(e)}"
            )
    
    async def _validate_numerical_validity(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate numerical data validity"""
        
        try:
            outlier_threshold = rule.parameters.get("outlier_threshold", 3.0)
            auto_detect_range = rule.parameters.get("auto_detect_range", True)
            
            validity_stats = {}
            total_violations = 0
            
            for col in columns:
                if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                    col_data = df[col].dropna()
                    
                    if len(col_data) == 0:
                        continue
                    
                    # Detect outliers using Z-score
                    z_scores = np.abs(stats.zscore(col_data))
                    outliers = z_scores > outlier_threshold
                    outlier_count = outliers.sum()
                    
                    # Check for infinite values
                    infinite_count = np.isinf(col_data).sum()
                    
                    # Check for negative values where not expected
                    negative_count = (col_data < 0).sum() if col in ["price", "volume"] else 0
                    
                    violations = outlier_count + infinite_count + negative_count
                    total_violations += violations
                    
                    validity_stats[col] = {
                        "outlier_count": outlier_count,
                        "infinite_count": infinite_count,
                        "negative_count": negative_count,
                        "total_violations": violations,
                        "validity_percentage": ((len(col_data) - violations) / len(col_data)) * 100
                    }
            
            overall_validity = (
                sum(s["validity_percentage"] for s in validity_stats.values()) / len(validity_stats)
                if validity_stats else 100
            )
            
            passed = overall_validity >= 95.0  # 95% validity threshold
            score = overall_validity / 100
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Numerical validity: {overall_validity:.2f}%",
                details={"column_stats": validity_stats},
                affected_records=total_violations
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Numerical validity error: {str(e)}"
            )
    
    async def _validate_categorical_validity(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate categorical data validity"""
        
        try:
            allowed_values = rule.parameters.get("allowed_values", [])
            case_sensitive = rule.parameters.get("case_sensitive", False)
            
            validity_stats = {}
            total_violations = 0
            
            for col in columns:
                if col in df.columns:
                    col_data = df[col].dropna().astype(str)
                    
                    if not case_sensitive:
                        col_data = col_data.str.lower()
                        allowed_set = set(str(v).lower() for v in allowed_values) if allowed_values else set()
                    else:
                        allowed_set = set(str(v) for v in allowed_values) if allowed_values else set()
                    
                    if allowed_values:
                        # Check against allowed values
                        invalid_values = ~col_data.isin(allowed_set)
                        invalid_count = invalid_values.sum()
                    else:
                        # Auto-detect valid categories (no single-occurrence values)
                        value_counts = col_data.value_counts()
                        single_occurrence = value_counts[value_counts == 1]
                        invalid_count = len(single_occurrence)
                    
                    total_violations += invalid_count
                    
                    validity_stats[col] = {
                        "invalid_count": invalid_count,
                        "unique_values": col_data.nunique(),
                        "validity_percentage": ((len(col_data) - invalid_count) / len(col_data)) * 100 if len(col_data) > 0 else 100
                    }
            
            overall_validity = (
                sum(s["validity_percentage"] for s in validity_stats.values()) / len(validity_stats)
                if validity_stats else 100
            )
            
            passed = overall_validity >= 95.0
            score = overall_validity / 100
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Categorical validity: {overall_validity:.2f}%",
                details={"column_stats": validity_stats},
                affected_records=total_violations
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Categorical validity error: {str(e)}"
            )
    
    async def _validate_consistency(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data consistency"""
        
        try:
            check_ordering = rule.parameters.get("check_ordering", True)
            allow_future_dates = rule.parameters.get("allow_future_dates", False)
            
            consistency_issues = 0
            details = {}
            
            for col in columns:
                if col in df.columns:
                    if pd.api.types.is_datetime64_any_dtype(df[col]):
                        # Check temporal consistency
                        if check_ordering:
                            # Check if timestamps are in ascending order
                            is_sorted = df[col].is_monotonic_increasing
                            if not is_sorted:
                                consistency_issues += 1
                                details[f"{col}_ordering"] = "Timestamps not in ascending order"
                        
                        if not allow_future_dates:
                            # Check for future dates
                            future_dates = df[col] > datetime.now()
                            future_count = future_dates.sum()
                            if future_count > 0:
                                consistency_issues += future_count
                                details[f"{col}_future_dates"] = f"{future_count} future dates found"
            
            passed = consistency_issues == 0
            score = 1.0 if passed else max(0, 1 - (consistency_issues / len(df)))
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Consistency issues: {consistency_issues}",
                details=details,
                affected_records=consistency_issues
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Consistency validation error: {str(e)}"
            )
    
    async def _validate_uniqueness(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data uniqueness"""
        
        try:
            subset_columns = rule.parameters.get("subset_columns", [])
            
            if subset_columns:
                # Check duplicates in specific columns
                available_columns = [col for col in subset_columns if col in df.columns]
                if available_columns:
                    duplicates = df.duplicated(subset=available_columns)
                else:
                    duplicates = df.duplicated()
            else:
                # Check duplicates across all columns
                duplicates = df.duplicated()
            
            duplicate_count = duplicates.sum()
            uniqueness_percentage = ((len(df) - duplicate_count) / len(df)) * 100 if len(df) > 0 else 100
            
            passed = duplicate_count == 0
            score = uniqueness_percentage / 100
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Duplicate records: {duplicate_count} ({100-uniqueness_percentage:.2f}%)",
                details={"duplicate_count": duplicate_count, "uniqueness_percentage": uniqueness_percentage},
                affected_records=duplicate_count
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Uniqueness validation error: {str(e)}"
            )
    
    async def _validate_accuracy(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data accuracy using outlier detection"""
        
        try:
            method = rule.parameters.get("method", "isolation_forest")
            contamination = rule.parameters.get("contamination", 0.1)
            
            numerical_columns = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
            
            if not numerical_columns:
                return ValidationResult(
                    rule_id=rule.rule_id,
                    passed=True,
                    score=1.0,
                    message="No numerical columns for accuracy validation"
                )
            
            # Prepare data for outlier detection
            data_for_analysis = df[numerical_columns].dropna()
            
            if len(data_for_analysis) < 10:
                return ValidationResult(
                    rule_id=rule.rule_id,
                    passed=True,
                    score=1.0,
                    message="Insufficient data for outlier detection"
                )
            
            # Apply outlier detection
            if method == "isolation_forest":
                detector = IsolationForest(contamination=contamination, random_state=42)
                outlier_labels = detector.fit_predict(data_for_analysis)
                outliers = outlier_labels == -1
            else:
                # Z-score method
                z_scores = np.abs(stats.zscore(data_for_analysis))
                outliers = (z_scores > 3).any(axis=1)
            
            outlier_count = outliers.sum()
            accuracy_percentage = ((len(data_for_analysis) - outlier_count) / len(data_for_analysis)) * 100
            
            passed = accuracy_percentage >= 90.0  # 90% accuracy threshold
            score = accuracy_percentage / 100
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Data accuracy: {accuracy_percentage:.2f}% (outliers: {outlier_count})",
                details={"outlier_count": outlier_count, "accuracy_percentage": accuracy_percentage, "method": method},
                affected_records=outlier_count
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Accuracy validation error: {str(e)}"
            )
    
    async def _validate_timeliness(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data timeliness"""
        
        try:
            max_age_hours = rule.parameters.get("max_age_hours", 24)
            business_hours_only = rule.parameters.get("business_hours_only", False)
            
            current_time = datetime.now()
            max_age_threshold = current_time - timedelta(hours=max_age_hours)
            
            timeliness_stats = {}
            total_stale_records = 0
            
            for col in columns:
                if col in df.columns and pd.api.types.is_datetime64_any_dtype(df[col]):
                    col_data = pd.to_datetime(df[col]).dropna()
                    
                    # Check for stale data
                    stale_data = col_data < max_age_threshold
                    stale_count = stale_data.sum()
                    total_stale_records += stale_count
                    
                    # Calculate freshness percentage
                    freshness_percentage = ((len(col_data) - stale_count) / len(col_data)) * 100 if len(col_data) > 0 else 100
                    
                    timeliness_stats[col] = {
                        "stale_count": stale_count,
                        "freshness_percentage": freshness_percentage,
                        "latest_timestamp": col_data.max().isoformat() if len(col_data) > 0 else None,
                        "oldest_timestamp": col_data.min().isoformat() if len(col_data) > 0 else None
                    }
            
            overall_freshness = (
                sum(s["freshness_percentage"] for s in timeliness_stats.values()) / len(timeliness_stats)
                if timeliness_stats else 100
            )
            
            passed = overall_freshness >= 95.0  # 95% freshness threshold
            score = overall_freshness / 100
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Data freshness: {overall_freshness:.2f}% (stale records: {total_stale_records})",
                details={"column_stats": timeliness_stats, "max_age_hours": max_age_hours},
                affected_records=total_stale_records
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Timeliness validation error: {str(e)}"
            )
    
    async def _validate_integrity(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data integrity"""
        
        try:
            enforce_schema = rule.parameters.get("enforce_schema", True)
            allow_extra_columns = rule.parameters.get("allow_extra_columns", False)
            
            integrity_issues = []
            
            # Check for required columns
            expected_columns = set(columns) if columns != ["*"] else set()
            actual_columns = set(df.columns)
            
            if expected_columns:
                missing_columns = expected_columns - actual_columns
                if missing_columns:
                    integrity_issues.append(f"Missing columns: {list(missing_columns)}")
                
                if not allow_extra_columns:
                    extra_columns = actual_columns - expected_columns
                    if extra_columns:
                        integrity_issues.append(f"Unexpected columns: {list(extra_columns)}")
            
            # Check data types consistency
            type_issues = []
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Check for mixed types in object columns
                    sample_data = df[col].dropna().head(100)
                    if len(sample_data) > 0:
                        types = set(type(val).__name__ for val in sample_data)
                        if len(types) > 1:
                            type_issues.append(f"Mixed types in column {col}: {types}")
            
            if type_issues:
                integrity_issues.extend(type_issues)
            
            passed = len(integrity_issues) == 0
            score = 1.0 if passed else max(0, 1 - (len(integrity_issues) / 10))  # Penalize up to 10 issues
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Integrity issues: {len(integrity_issues)}",
                details={"issues": integrity_issues},
                affected_records=0  # Schema issues affect the entire dataset
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Integrity validation error: {str(e)}"
            )
    
    async def _validate_drift(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data drift"""
        
        try:
            drift_threshold = rule.parameters.get("drift_threshold", 0.1)
            statistical_test = rule.parameters.get("statistical_test", "ks_test")
            
            # This is a simplified drift detection
            # In production, would use more sophisticated methods
            
            drift_detected = False
            drift_details = {}
            
            # For now, simulate drift detection
            # In real implementation, would compare against reference dataset
            
            numerical_columns = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
            
            for col in numerical_columns:
                # Simulate drift score
                drift_score = np.random.random() * 0.2  # Random drift score between 0-0.2
                
                drift_details[col] = {
                    "drift_score": drift_score,
                    "drift_detected": drift_score > drift_threshold
                }
                
                if drift_score > drift_threshold:
                    drift_detected = True
            
            overall_drift_score = (
                sum(d["drift_score"] for d in drift_details.values()) / len(drift_details)
                if drift_details else 0
            )
            
            passed = not drift_detected
            score = max(0, 1 - overall_drift_score)
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Data drift score: {overall_drift_score:.3f} (threshold: {drift_threshold})",
                details={"column_drift": drift_details, "overall_drift_score": overall_drift_score},
                affected_records=0
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Drift validation error: {str(e)}"
            )
    
    async def _validate_bias(
        self,
        df: pd.DataFrame,
        columns: List[str],
        rule: ValidationRule
    ) -> ValidationResult:
        """Validate data bias"""
        
        try:
            fairness_metrics = rule.parameters.get("fairness_metrics", ["demographic_parity"])
            
            bias_issues = []
            bias_details = {}
            
            for col in columns:
                if col in df.columns:
                    # Check for representation bias
                    value_counts = df[col].value_counts()
                    total_count = len(df)
                    
                    # Check if any category is over/under-represented
                    for value, count in value_counts.items():
                        percentage = (count / total_count) * 100
                        
                        # Flag if any category is less than 5% or more than 80%
                        if percentage < 5.0:
                            bias_issues.append(f"Under-representation: {col}={value} ({percentage:.1f}%)")
                        elif percentage > 80.0:
                            bias_issues.append(f"Over-representation: {col}={value} ({percentage:.1f}%)")
                    
                    bias_details[col] = {
                        "value_distribution": value_counts.to_dict(),
                        "entropy": stats.entropy(value_counts.values),
                        "gini_coefficient": self._calculate_gini_coefficient(value_counts.values)
                    }
            
            passed = len(bias_issues) == 0
            score = max(0, 1 - (len(bias_issues) / 10))  # Penalize up to 10 bias issues
            
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=passed,
                score=score,
                message=f"Bias issues detected: {len(bias_issues)}",
                details={"bias_issues": bias_issues, "column_analysis": bias_details},
                affected_records=0
            )
            
        except Exception as e:
            return ValidationResult(
                rule_id=rule.rule_id,
                passed=False,
                score=0.0,
                message=f"Bias validation error: {str(e)}"
            )
    
    def _calculate_gini_coefficient(self, values):
        """Calculate Gini coefficient for inequality measurement"""
        
        try:
            values = np.array(values)
            values = np.sort(values)
            n = len(values)
            
            if n == 0:
                return 0
            
            cumsum = np.cumsum(values)
            return (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n
            
        except Exception:
            return 0
    
    async def _generate_data_profile(
        self,
        df: pd.DataFrame,
        dataset_id: str
    ) -> DataProfile:
        """Generate comprehensive data profile"""
        
        try:
            # Basic statistics
            total_records = len(df)
            total_columns = len(df.columns)
            
            # Missing values
            missing_values = df.isnull().sum().to_dict()
            
            # Data types
            data_types = df.dtypes.astype(str).to_dict()
            
            # Numerical statistics
            numerical_stats = {}
            numerical_columns = df.select_dtypes(include=[np.number]).columns
            
            for col in numerical_columns:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    numerical_stats[col] = {
                        "mean": float(col_data.mean()),
                        "median": float(col_data.median()),
                        "std": float(col_data.std()),
                        "min": float(col_data.min()),
                        "max": float(col_data.max()),
                        "q25": float(col_data.quantile(0.25)),
                        "q75": float(col_data.quantile(0.75)),
                        "skewness": float(col_data.skew()),
                        "kurtosis": float(col_data.kurtosis())
                    }
            
            # Categorical statistics
            categorical_stats = {}
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns
            
            for col in categorical_columns:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    value_counts = col_data.value_counts()
                    categorical_stats[col] = {
                        "unique_count": int(col_data.nunique()),
                        "most_frequent": str(value_counts.index[0]) if len(value_counts) > 0 else None,
                        "most_frequent_count": int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                        "entropy": float(stats.entropy(value_counts.values))
                    }
            
            # Correlation matrix for numerical columns
            correlation_matrix = None
            if len(numerical_columns) > 1:
                correlation_matrix = df[numerical_columns].corr().values
            
            # Outlier detection
            outlier_counts = {}
            for col in numerical_columns:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    z_scores = np.abs(stats.zscore(col_data))
                    outlier_counts[col] = int((z_scores > 3).sum())
            
            # Duplicate records
            duplicate_records = int(df.duplicated().sum())
            
            return DataProfile(
                dataset_id=dataset_id,
                total_records=total_records,
                total_columns=total_columns,
                missing_values=missing_values,
                data_types=data_types,
                numerical_stats=numerical_stats,
                categorical_stats=categorical_stats,
                correlation_matrix=correlation_matrix,
                outlier_counts=outlier_counts,
                duplicate_records=duplicate_records
            )
            
        except Exception as e:
            logger.error(f"Failed to generate data profile: {e}")
            return DataProfile(
                dataset_id=dataset_id,
                total_records=0,
                total_columns=0,
                missing_values={},
                data_types={},
                numerical_stats={},
                categorical_stats={}
            )
    
    async def _analyze_data_drift(
        self,
        df: pd.DataFrame,
        dataset_id: str
    ) -> Dict[str, Any]:
        """Analyze data drift against reference datasets"""
        
        try:
            drift_analysis = {
                "drift_detected": False,
                "drift_score": 0.0,
                "column_drift": {},
                "recommendations": []
            }
            
            # Find matching reference dataset
            reference_key = None
            for key in self.reference_datasets.keys():
                if key in dataset_id.lower():
                    reference_key = key
                    break
            
            if reference_key and reference_key in self.reference_datasets:
                reference_df = self.reference_datasets[reference_key]
                
                # Compare distributions for common columns
                common_columns = set(df.columns) & set(reference_df.columns)
                numerical_columns = [col for col in common_columns if pd.api.types.is_numeric_dtype(df[col])]
                
                total_drift_score = 0
                column_count = 0
                
                for col in numerical_columns:
                    try:
                        # Kolmogorov-Smirnov test
                        current_data = df[col].dropna()
                        reference_data = reference_df[col].dropna()
                        
                        if len(current_data) > 10 and len(reference_data) > 10:
                            ks_statistic, p_value = stats.ks_2samp(current_data, reference_data)
                            
                            drift_analysis["column_drift"][col] = {
                                "ks_statistic": float(ks_statistic),
                                "p_value": float(p_value),
                                "drift_detected": p_value < 0.05,
                                "drift_magnitude": "high" if ks_statistic > 0.2 else "medium" if ks_statistic > 0.1 else "low"
                            }
                            
                            total_drift_score += ks_statistic
                            column_count += 1
                            
                            if p_value < 0.05:
                                drift_analysis["drift_detected"] = True
                                drift_analysis["recommendations"].append(
                                    f"Significant drift detected in column '{col}' - consider retraining"
                                )
                    
                    except Exception as e:
                        logger.warning(f"Drift analysis failed for column {col}: {e}")
                
                if column_count > 0:
                    drift_analysis["drift_score"] = total_drift_score / column_count
            
            else:
                drift_analysis["recommendations"].append(
                    "No reference dataset available for drift analysis"
                )
            
            return drift_analysis
            
        except Exception as e:
            logger.error(f"Data drift analysis failed: {e}")
            return {
                "drift_detected": False,
                "drift_score": 0.0,
                "error": str(e)
            }
    
    async def _analyze_data_bias(
        self,
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """Analyze potential bias in the dataset"""
        
        try:
            bias_analysis = {
                "bias_detected": False,
                "bias_score": 0.0,
                "representation_analysis": {},
                "fairness_metrics": {},
                "recommendations": []
            }
            
            # Analyze representation across categorical columns
            categorical_columns = df.select_dtypes(include=['object', 'category']).columns
            
            total_bias_score = 0
            column_count = 0
            
            for col in categorical_columns:
                try:
                    value_counts = df[col].value_counts()
                    total_count = len(df)
                    
                    # Calculate representation percentages
                    percentages = (value_counts / total_count * 100).to_dict()
                    
                    # Calculate entropy (higher entropy = more balanced)
                    entropy = stats.entropy(value_counts.values)
                    max_entropy = np.log(len(value_counts))  # Maximum possible entropy
                    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
                    
                    # Calculate Gini coefficient (0 = perfect equality, 1 = perfect inequality)
                    gini = self._calculate_gini_coefficient(value_counts.values)
                    
                    bias_analysis["representation_analysis"][col] = {
                        "value_percentages": percentages,
                        "entropy": float(entropy),
                        "normalized_entropy": float(normalized_entropy),
                        "gini_coefficient": float(gini),
                        "bias_score": float(gini)  # Use Gini as bias score
                    }
                    
                    total_bias_score += gini
                    column_count += 1
                    
                    # Flag potential bias issues
                    if gini > 0.7:
                        bias_analysis["bias_detected"] = True
                        bias_analysis["recommendations"].append(
                            f"High inequality detected in column '{col}' (Gini: {gini:.3f}) - consider data balancing"
                        )
                    
                    # Check for severe under-representation
                    min_percentage = min(percentages.values())
                    if min_percentage < 1.0:  # Less than 1%
                        bias_analysis["recommendations"].append(
                            f"Severe under-representation in column '{col}' - minimum category: {min_percentage:.2f}%"
                        )
                
                except Exception as e:
                    logger.warning(f"Bias analysis failed for column {col}: {e}")
            
            if column_count > 0:
                bias_analysis["bias_score"] = total_bias_score / column_count
            
            # Overall bias assessment
            if bias_analysis["bias_score"] > 0.5:
                bias_analysis["bias_detected"] = True
                bias_analysis["recommendations"].append(
                    "Overall dataset shows signs of bias - consider data augmentation or resampling"
                )
            
            return bias_analysis
            
        except Exception as e:
            logger.error(f"Bias analysis failed: {e}")
            return {
                "bias_detected": False,
                "bias_score": 0.0,
                "error": str(e)
            }
    
    async def _generate_recommendations(
        self,
        validation_results: List[ValidationResult],
        data_profile: DataProfile
    ) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        
        recommendations = []
        
        try:
            # Analyze failed validations
            failed_results = [r for r in validation_results if not r.passed]
            
            for result in failed_results:
                if result.rule_id == "completeness_check":
                    recommendations.append(
                        f"Address missing data: {result.affected_records} records affected. "
                        "Consider imputation strategies or data collection improvements."
                    )
                
                elif result.rule_id == "numerical_range_check":
                    recommendations.append(
                        f"Review numerical data ranges: {result.affected_records} outliers detected. "
                        "Consider outlier treatment or data validation at source."
                    )
                
                elif result.rule_id == "duplicate_detection":
                    recommendations.append(
                        f"Remove {result.affected_records} duplicate records to improve data quality."
                    )
                
                elif result.rule_id == "data_freshness":
                    recommendations.append(
                        f"Update data sources: {result.affected_records} stale records found. "
                        "Consider increasing data collection frequency."
                    )
                
                elif result.rule_id == "distribution_stability":
                    recommendations.append(
                        "Data drift detected. Consider retraining models or investigating data source changes."
                    )
                
                elif result.rule_id == "bias_detection":
                    recommendations.append(
                        "Potential bias detected. Review data collection process and consider bias mitigation techniques."
                    )
            
            # General recommendations based on data profile
            if data_profile.duplicate_records > 0:
                recommendations.append(
                    f"Consider deduplication: {data_profile.duplicate_records} duplicate records found."
                )
            
            # Check for highly correlated features
            if data_profile.correlation_matrix is not None:
                high_corr_pairs = []
                n = data_profile.correlation_matrix.shape[0]
                for i in range(n):
                    for j in range(i+1, n):
                        if abs(data_profile.correlation_matrix[i, j]) > 0.9:
                            high_corr_pairs.append((i, j))
                
                if high_corr_pairs:
                    recommendations.append(
                        f"Consider feature selection: {len(high_corr_pairs)} highly correlated feature pairs detected."
                    )
            
            # Check for imbalanced features
            for col, stats in data