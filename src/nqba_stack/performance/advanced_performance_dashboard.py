"""
Advanced Performance Dashboard for Phase 2
Real-time monitoring, advanced analytics, and intelligent recommendations
"""

import asyncio
import json
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
import numpy as np
from enum import Enum

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class MetricType(Enum):
    """Types of performance metrics"""
    SYSTEM = "system"
    BUSINESS = "business"
    QUANTUM = "quantum"
    USER = "user"
    FINANCIAL = "financial"

@dataclass
class PerformanceAlert:
    """Performance alert definition"""
    alert_id: str
    tenant_id: Optional[str]
    alert_type: str
    severity: AlertSeverity
    message: str
    timestamp: datetime
    metric_name: str
    current_value: float
    threshold_value: float
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PerformanceTrend:
    """Performance trend analysis"""
    metric_name: str
    current_value: float
    previous_value: float
    change_percentage: float
    trend_direction: str  # 'improving', 'stable', 'degrading'
    confidence: float
    prediction: Optional[float] = None
    recommendation: Optional[str] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SystemHealth:
    """Overall system health status"""
    overall_health: str  # 'healthy', 'degraded', 'critical'
    health_score: float  # 0.0 to 1.0
    last_updated: datetime
    
    # Component health
    api_server_health: str
    quantum_adapter_health: str
    business_pods_health: str
    database_health: str
    network_health: str
    
    # Performance indicators
    response_time_avg: float
    throughput_avg: float
    error_rate_avg: float
    availability_avg: float
    
    # Resource utilization
    cpu_utilization: float
    memory_utilization: float
    storage_utilization: float
    quantum_utilization: float
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BusinessMetrics:
    """Business performance metrics"""
    tenant_id: str
    timestamp: datetime
    
    # User engagement
    active_users: int
    new_users: int
    user_retention_rate: float
    
    # Business operations
    operations_per_second: float
    successful_operations: int
    failed_operations: int
    operation_success_rate: float
    
    # Revenue metrics
    revenue_per_hour: float
    revenue_per_user: float
    cost_per_operation: float
    profit_margin: float
    
    # SLA compliance
    sla_compliance_rate: float
    sla_violations: int
    average_response_time: float
    
    metadata: Dict[str, Any] = field(default_factory=dict)

class AdvancedPerformanceDashboard:
    """Advanced performance dashboard with real-time monitoring and analytics"""
    
    def __init__(self, update_interval: int = 30, retention_hours: int = 168):
        self.update_interval = update_interval  # seconds
        self.retention_hours = retention_hours  # 1 week
        
        # Core components
        self.system_health: Optional[SystemHealth] = None
        self.performance_metrics: Dict[str, List[Dict[str, Any]]] = {}
        self.business_metrics: Dict[str, List[BusinessMetrics]] = {}
        self.alerts: Dict[str, PerformanceAlert] = {}
        self.trends: Dict[str, PerformanceTrend] = {}
        
        # Dashboard state
        self.is_running = False
        self.last_update = None
        self.update_count = 0
        
        # Alert configuration
        self.alert_thresholds = {
            'response_time': {'warning': 1.0, 'critical': 2.0},
            'error_rate': {'warning': 0.02, 'critical': 0.05},
            'cpu_utilization': {'warning': 0.8, 'critical': 0.9},
            'memory_utilization': {'warning': 0.75, 'critical': 0.85},
            'availability': {'warning': 0.99, 'critical': 0.95}
        }
        
        # Trend analysis configuration
        self.trend_analysis_window = 24  # hours
        self.min_data_points_for_trend = 10
        
        logger.info("Advanced Performance Dashboard initialized")
    
    async def start_dashboard(self):
        """Start the performance dashboard"""
        try:
            if self.is_running:
                logger.warning("Dashboard is already running")
                return
            
            self.is_running = True
            logger.info("Starting Advanced Performance Dashboard")
            
            # Start monitoring loop
            asyncio.create_task(self._monitoring_loop())
            
        except Exception as e:
            logger.error(f"Error starting dashboard: {e}")
            raise
    
    async def stop_dashboard(self):
        """Stop the performance dashboard"""
        try:
            self.is_running = False
            logger.info("Stopping Advanced Performance Dashboard")
            
        except Exception as e:
            logger.error(f"Error stopping dashboard: {e}")
            raise
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                start_time = datetime.now()
                
                # Collect system health
                await self._collect_system_health()
                
                # Analyze performance trends
                await self._analyze_performance_trends()
                
                # Check for alerts
                await self._check_alerts()
                
                # Generate recommendations
                await self._generate_recommendations()
                
                # Update dashboard state
                self.last_update = datetime.now()
                self.update_count += 1
                
                # Calculate execution time
                execution_time = (datetime.now() - start_time).total_seconds()
                
                # Log update
                logger.debug(f"Dashboard update {self.update_count} completed in {execution_time:.2f}s")
                
                # Wait for next update
                await asyncio.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.update_interval)
    
    async def _collect_system_health(self):
        """Collect overall system health metrics"""
        try:
            # This would integrate with actual system monitoring
            # For now, create mock data
            
            # Simulate system health collection
            health_score = 0.95  # Mock health score
            
            # Determine overall health
            if health_score >= 0.9:
                overall_health = "healthy"
            elif health_score >= 0.7:
                overall_health = "degraded"
            else:
                overall_health = "critical"
            
            # Create system health object
            self.system_health = SystemHealth(
                overall_health=overall_health,
                health_score=health_score,
                last_updated=datetime.now(),
                api_server_health="healthy",
                quantum_adapter_health="healthy",
                business_pods_health="healthy",
                database_health="healthy",
                network_health="healthy",
                response_time_avg=0.15,
                throughput_avg=1000.0,
                error_rate_avg=0.01,
                availability_avg=0.999,
                cpu_utilization=0.65,
                memory_utilization=0.58,
                storage_utilization=0.42,
                quantum_utilization=0.73,
                metadata={'source': 'mock_data'}
            )
            
        except Exception as e:
            logger.error(f"Error collecting system health: {e}")
    
    async def _analyze_performance_trends(self):
        """Analyze performance trends from historical data"""
        try:
            # Analyze trends for each metric type
            for metric_type in MetricType:
                await self._analyze_metric_trends(metric_type.value)
            
        except Exception as e:
            logger.error(f"Error analyzing performance trends: {e}")
    
    async def _analyze_metric_trends(self, metric_type: str):
        """Analyze trends for a specific metric type"""
        try:
            if metric_type not in self.performance_metrics:
                return
            
            metrics_data = self.performance_metrics[metric_type]
            
            # Get recent data points
            cutoff_time = datetime.now() - timedelta(hours=self.trend_analysis_window)
            recent_metrics = [
                m for m in metrics_data
                if m.get('timestamp', datetime.min) >= cutoff_time
            ]
            
            if len(recent_metrics) < self.min_data_points_for_trend:
                return
            
            # Analyze trends for each metric
            for metric_name in self._get_metric_names(metric_type):
                trend = await self._calculate_trend(metric_name, recent_metrics)
                if trend:
                    self.trends[f"{metric_type}_{metric_name}"] = trend
            
        except Exception as e:
            logger.error(f"Error analyzing trends for {metric_type}: {e}")
    
    def _get_metric_names(self, metric_type: str) -> List[str]:
        """Get metric names for a specific type"""
        metric_maps = {
            'system': ['cpu_utilization', 'memory_utilization', 'response_time', 'throughput'],
            'business': ['operations_per_second', 'success_rate', 'revenue_per_hour'],
            'quantum': ['quantum_advantage', 'quantum_utilization', 'optimization_success_rate'],
            'user': ['active_users', 'user_satisfaction', 'feature_usage'],
            'financial': ['cost_per_operation', 'profit_margin', 'revenue_growth']
        }
        return metric_maps.get(metric_type, [])
    
    async def _calculate_trend(
        self,
        metric_name: str,
        metrics_data: List[Dict[str, Any]]
    ) -> Optional[PerformanceTrend]:
        """Calculate trend for a specific metric"""
        try:
            # Extract values for the metric
            values = []
            timestamps = []
            
            for metric in metrics_data:
                if metric_name in metric:
                    values.append(metric[metric_name])
                    timestamps.append(metric.get('timestamp', datetime.now()))
            
            if len(values) < 2:
                return None
            
            # Calculate trend
            current_value = values[-1]
            previous_value = values[-2]
            
            if previous_value == 0:
                change_percentage = 0.0
            else:
                change_percentage = ((current_value - previous_value) / previous_value) * 100
            
            # Determine trend direction
            if change_percentage > 5:
                trend_direction = "improving"
            elif change_percentage < -5:
                trend_direction = "degrading"
            else:
                trend_direction = "stable"
            
            # Calculate confidence based on data consistency
            confidence = self._calculate_trend_confidence(values)
            
            # Generate prediction (simple linear extrapolation)
            prediction = None
            if len(values) >= 3:
                prediction = self._linear_prediction(values)
            
            # Generate recommendation
            recommendation = self._generate_trend_recommendation(
                metric_name, trend_direction, change_percentage, current_value
            )
            
            return PerformanceTrend(
                metric_name=metric_name,
                current_value=current_value,
                previous_value=previous_value,
                change_percentage=change_percentage,
                trend_direction=trend_direction,
                confidence=confidence,
                prediction=prediction,
                recommendation=recommendation,
                metadata={'data_points': len(values)}
            )
            
        except Exception as e:
            logger.error(f"Error calculating trend for {metric_name}: {e}")
            return None
    
    def _calculate_trend_confidence(self, values: List[float]) -> float:
        """Calculate confidence in trend based on data consistency"""
        if len(values) < 2:
            return 0.0
        
        # Calculate coefficient of variation (lower is more consistent)
        mean_value = np.mean(values)
        std_value = np.std(values)
        
        if mean_value == 0:
            return 0.0
        
        cv = std_value / abs(mean_value)
        
        # Convert to confidence (0.0 to 1.0)
        confidence = max(0.0, 1.0 - cv)
        return min(1.0, confidence)
    
    def _linear_prediction(self, values: List[float]) -> float:
        """Generate linear prediction for next value"""
        if len(values) < 3:
            return None
        
        # Simple linear regression
        x = np.arange(len(values))
        y = np.array(values)
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        
        # Predict next value
        next_x = len(values)
        prediction = slope * next_x + (y[0] - slope * 0)
        
        return max(0.0, prediction)  # Ensure non-negative
    
    def _generate_trend_recommendation(
        self,
        metric_name: str,
        trend_direction: str,
        change_percentage: float,
        current_value: float
    ) -> Optional[str]:
        """Generate recommendation based on trend analysis"""
        recommendations = {
            'cpu_utilization': {
                'improving': "CPU utilization is improving. Consider optimizing resource allocation.",
                'degrading': "CPU utilization is degrading. Consider scaling up or optimizing workloads.",
                'stable': "CPU utilization is stable. Monitor for changes in workload patterns."
            },
            'response_time': {
                'improving': "Response time is improving. Performance optimizations are effective.",
                'degrading': "Response time is degrading. Investigate bottlenecks and consider scaling.",
                'stable': "Response time is stable. Continue monitoring for performance issues."
            },
            'error_rate': {
                'improving': "Error rate is improving. System stability is increasing.",
                'degrading': "Error rate is degrading. Investigate system issues immediately.",
                'stable': "Error rate is stable. Monitor for any sudden changes."
            }
        }
        
        metric_recs = recommendations.get(metric_name, {})
        return metric_recs.get(trend_direction, None)
    
    async def _check_alerts(self):
        """Check for performance alerts based on thresholds"""
        try:
            if not self.system_health:
                return
            
            # Check response time alerts
            await self._check_metric_alert(
                'response_time',
                self.system_health.response_time_avg,
                'System Response Time'
            )
            
            # Check error rate alerts
            await self._check_metric_alert(
                'error_rate',
                self.system_health.error_rate_avg,
                'System Error Rate'
            )
            
            # Check CPU utilization alerts
            await self._check_metric_alert(
                'cpu_utilization',
                self.system_health.cpu_utilization,
                'CPU Utilization'
            )
            
            # Check memory utilization alerts
            await self._check_metric_alert(
                'memory_utilization',
                self.system_health.memory_utilization,
                'Memory Utilization'
            )
            
            # Check availability alerts
            await self._check_metric_alert(
                'availability',
                self.system_health.availability_avg,
                'System Availability'
            )
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    async def _check_metric_alert(
        self,
        metric_name: str,
        current_value: float,
        display_name: str
    ):
        """Check if a metric should trigger an alert"""
        try:
            if metric_name not in self.alert_thresholds:
                return
            
            thresholds = self.alert_thresholds[metric_name]
            
            # Check critical threshold
            if 'critical' in thresholds and current_value >= thresholds['critical']:
                await self._create_alert(
                    metric_name, display_name, current_value, thresholds['critical'],
                    AlertSeverity.CRITICAL
                )
            # Check warning threshold
            elif 'warning' in thresholds and current_value >= thresholds['warning']:
                await self._create_alert(
                    metric_name, display_name, current_value, thresholds['warning'],
                    AlertSeverity.WARNING
                )
            
        except Exception as e:
            logger.error(f"Error checking metric alert for {metric_name}: {e}")
    
    async def _create_alert(
        self,
        metric_name: str,
        display_name: str,
        current_value: float,
        threshold_value: float,
        severity: AlertSeverity
    ):
        """Create a new performance alert"""
        try:
            # Check if alert already exists
            alert_key = f"{metric_name}_{severity.value}"
            if alert_key in self.alerts:
                existing_alert = self.alerts[alert_key]
                if not existing_alert.resolved:
                    return  # Alert already active
            
            # Create new alert
            alert = PerformanceAlert(
                alert_id=f"alert_{len(self.alerts) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                tenant_id=None,  # System-wide alert
                alert_type="performance_threshold",
                severity=severity,
                message=f"{display_name} exceeded {severity.value} threshold: {current_value:.3f} > {threshold_value:.3f}",
                timestamp=datetime.now(),
                metric_name=metric_name,
                current_value=current_value,
                threshold_value=threshold_value,
                metadata={'threshold_type': 'upper_bound'}
            )
            
            self.alerts[alert_key] = alert
            
            # Log alert
            logger.warning(f"Performance alert created: {alert.message}")
            
            # Could trigger notifications here (email, webhook, etc.)
            
        except Exception as e:
            logger.error(f"Error creating alert: {e}")
    
    async def _generate_recommendations(self):
        """Generate intelligent recommendations based on current state"""
        try:
            recommendations = []
            
            if self.system_health:
                # CPU utilization recommendations
                if self.system_health.cpu_utilization > 0.8:
                    recommendations.append({
                        'type': 'scaling',
                        'priority': 'high',
                        'message': 'High CPU utilization detected. Consider scaling up compute resources.',
                        'action': 'scale_compute_resources',
                        'estimated_impact': 'high',
                        'estimated_cost': 'medium'
                    })
                
                # Memory utilization recommendations
                if self.system_health.memory_utilization > 0.75:
                    recommendations.append({
                        'type': 'optimization',
                        'priority': 'medium',
                        'message': 'High memory utilization. Consider memory optimization or scaling.',
                        'action': 'optimize_memory_usage',
                        'estimated_impact': 'medium',
                        'estimated_cost': 'low'
                    })
                
                # Response time recommendations
                if self.system_health.response_time_avg > 1.0:
                    recommendations.append({
                        'type': 'performance',
                        'priority': 'high',
                        'message': 'High response time detected. Investigate performance bottlenecks.',
                        'action': 'investigate_performance',
                        'estimated_impact': 'high',
                        'estimated_cost': 'low'
                    })
            
            # Store recommendations
            self.system_health.metadata['recommendations'] = recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
    
    async def record_performance_metrics(
        self,
        metric_type: str,
        metrics_data: Dict[str, Any]
    ):
        """Record performance metrics for analysis"""
        try:
            if metric_type not in self.performance_metrics:
                self.performance_metrics[metric_type] = []
            
            # Add timestamp if not present
            if 'timestamp' not in metrics_data:
                metrics_data['timestamp'] = datetime.now()
            
            # Store metrics
            self.performance_metrics[metric_type].append(metrics_data)
            
            # Clean up old metrics
            await self._cleanup_old_metrics(metric_type)
            
        except Exception as e:
            logger.error(f"Error recording performance metrics: {e}")
    
    async def record_business_metrics(self, business_metrics: BusinessMetrics):
        """Record business performance metrics"""
        try:
            tenant_id = business_metrics.tenant_id
            
            if tenant_id not in self.business_metrics:
                self.business_metrics[tenant_id] = []
            
            self.business_metrics[tenant_id].append(business_metrics)
            
            # Clean up old business metrics
            await self._cleanup_old_business_metrics(tenant_id)
            
        except Exception as e:
            logger.error(f"Error recording business metrics: {e}")
    
    async def _cleanup_old_metrics(self, metric_type: str):
        """Clean up old performance metrics"""
        try:
            if metric_type not in self.performance_metrics:
                return
            
            cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
            
            # Remove old metrics
            self.performance_metrics[metric_type] = [
                m for m in self.performance_metrics[metric_type]
                if m.get('timestamp', datetime.min) >= cutoff_time
            ]
            
        except Exception as e:
            logger.error(f"Error cleaning up old metrics: {e}")
    
    async def _cleanup_old_business_metrics(self, tenant_id: str):
        """Clean up old business metrics"""
        try:
            if tenant_id not in self.business_metrics:
                return
            
            cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
            
            # Remove old metrics
            self.business_metrics[tenant_id] = [
                m for m in self.business_metrics[tenant_id]
                if m.timestamp >= cutoff_time
            ]
            
        except Exception as e:
            logger.error(f"Error cleaning up old business metrics: {e}")
    
    async def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get comprehensive dashboard summary"""
        try:
            summary = {
                'dashboard_status': {
                    'is_running': self.is_running,
                    'last_update': self.last_update.isoformat() if self.last_update else None,
                    'update_count': self.update_count,
                    'update_interval': self.update_interval
                },
                
                'system_health': self.system_health.__dict__ if self.system_health else None,
                
                'alerts_summary': {
                    'total_alerts': len(self.alerts),
                    'active_alerts': len([a for a in self.alerts.values() if not a.resolved]),
                    'critical_alerts': len([a for a in self.alerts.values() if a.severity == AlertSeverity.CRITICAL and not a.resolved]),
                    'warning_alerts': len([a for a in self.alerts.values() if a.severity == AlertSeverity.WARNING and not a.resolved])
                },
                
                'trends_summary': {
                    'total_trends': len(self.trends),
                    'improving_metrics': len([t for t in self.trends.values() if t.trend_direction == 'improving']),
                    'degrading_metrics': len([t for t in self.trends.values() if t.trend_direction == 'degrading']),
                    'stable_metrics': len([t for t in self.trends.values() if t.trend_direction == 'stable'])
                },
                
                'performance_metrics': {
                    'metric_types': list(self.performance_metrics.keys()),
                    'total_metrics': sum(len(metrics) for metrics in self.performance_metrics.values())
                },
                
                'business_metrics': {
                    'tenants_with_metrics': len(self.business_metrics),
                    'total_business_metrics': sum(len(metrics) for metrics in self.business_metrics.values())
                }
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting dashboard summary: {e}")
            return {'error': str(e)}
    
    async def get_tenant_performance(self, tenant_id: str) -> Dict[str, Any]:
        """Get performance data for a specific tenant"""
        try:
            tenant_data = {
                'tenant_id': tenant_id,
                'tenant_name': f"Tenant_{tenant_id}",  # Default tenant name
                'business_metrics': self.business_metrics.get(tenant_id, []),
                'performance_trends': {},
                'recommendations': []
            }
            
            # Get trends relevant to this tenant
            for trend_key, trend in self.trends.items():
                if tenant_id in trend_key:
                    tenant_data['performance_trends'][trend_key] = trend.__dict__
            
            # Generate tenant-specific recommendations
            if tenant_id in self.business_metrics:
                tenant_metrics = self.business_metrics[tenant_id]
                if tenant_metrics:
                    latest_metrics = tenant_metrics[-1]
                    
                    # Check SLA compliance
                    if latest_metrics.sla_compliance_rate < 0.95:
                        tenant_data['recommendations'].append({
                            'type': 'sla_compliance',
                            'priority': 'high',
                            'message': f'Low SLA compliance rate: {latest_metrics.sla_compliance_rate:.1%}',
                            'action': 'investigate_sla_violations'
                        })
                    
                    # Check error rate
                    if latest_metrics.operation_success_rate < 0.95:
                        tenant_data['recommendations'].append({
                            'type': 'error_rate',
                            'priority': 'medium',
                            'message': f'High error rate: {1 - latest_metrics.operation_success_rate:.1%}',
                            'action': 'investigate_errors'
                        })
            
            return tenant_data
            
        except Exception as e:
            logger.error(f"Error getting tenant performance: {e}")
            return {'error': str(e)}
    
    async def acknowledge_alert(self, alert_key: str, acknowledged_by: str) -> bool:
        """Acknowledge a performance alert"""
        try:
            if alert_key not in self.alerts:
                return False
            
            alert = self.alerts[alert_key]
            alert.acknowledged = True
            alert.acknowledged_by = acknowledged_by
            alert.acknowledged_at = datetime.now()
            
            logger.info(f"Alert {alert_key} acknowledged by {acknowledged_by}")
            return True
            
        except Exception as e:
            logger.error(f"Error acknowledging alert: {e}")
            return False
    
    async def resolve_alert(self, alert_key: str) -> bool:
        """Resolve a performance alert"""
        try:
            if alert_key not in self.alerts:
                return False
            
            alert = self.alerts[alert_key]
            alert.resolved = True
            alert.resolved_at = datetime.now()
            
            logger.info(f"Alert {alert_key} resolved")
            return True
            
        except Exception as e:
            logger.error(f"Error resolving alert: {e}")
            return False
