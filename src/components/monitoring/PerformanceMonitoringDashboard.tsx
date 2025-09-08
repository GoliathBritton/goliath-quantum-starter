import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  LinearProgress,
  Button,
  Switch,
  FormControlLabel,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tabs,
  Tab,
  Alert,
  AlertTitle,
  IconButton,
  Tooltip,
  Badge,
} from '@mui/material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
} from 'recharts';
import {
  PlayArrow,
  Stop,
  Refresh,
  Settings,
  Notifications,
  Warning,
  Error,
  CheckCircle,
  Speed,
  Memory,
  Storage,
  NetworkCheck,
  Security,
  TrendingUp,
  TrendingDown,
  Dashboard,
  Analytics,
  Timeline,
  Assessment,
} from '@mui/icons-material';
import PerformanceMonitoringService, {
  PerformanceMetrics,
  Alert as AlertType,
  Threshold,
  Dashboard as DashboardType,
} from '../../services/performanceMonitoringService';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`monitoring-tabpanel-${index}`}
      aria-labelledby={`monitoring-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const PerformanceMonitoringDashboard: React.FC = () => {
  const [monitoringService] = useState(() => new PerformanceMonitoringService());
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [metrics, setMetrics] = useState<PerformanceMetrics[]>([]);
  const [latestMetrics, setLatestMetrics] = useState<PerformanceMetrics | null>(null);
  const [alerts, setAlerts] = useState<AlertType[]>([]);
  const [activeTab, setActiveTab] = useState(0);
  const [refreshInterval, setRefreshInterval] = useState(30);
  const [timeRange, setTimeRange] = useState('1h');
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [alertDetailsOpen, setAlertDetailsOpen] = useState(false);
  const [selectedAlert, setSelectedAlert] = useState<AlertType | null>(null);

  // Colors for charts
  const colors = {
    primary: '#6366f1',
    secondary: '#8b5cf6',
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
    quantum: '#7c3aed',
  };

  useEffect(() => {
    // Initialize monitoring service
    monitoringService.on('metricsCollected', (newMetrics: PerformanceMetrics) => {
      setMetrics(prev => [...prev.slice(-99), newMetrics]); // Keep last 100 metrics
      setLatestMetrics(newMetrics);
    });

    monitoringService.on('alertCreated', (alert: AlertType) => {
      setAlerts(prev => [alert, ...prev]);
    });

    // Load initial data
    loadInitialData();

    return () => {
      monitoringService.removeAllListeners();
      if (isMonitoring) {
        monitoringService.stopMonitoring();
      }
    };
  }, []);

  const loadInitialData = useCallback(async () => {
    const historicalMetrics = monitoringService.getMetrics();
    const currentAlerts = monitoringService.getAlerts();
    const latest = monitoringService.getLatestMetrics();
    
    setMetrics(historicalMetrics);
    setAlerts(currentAlerts);
    setLatestMetrics(latest);
  }, [monitoringService]);

  const handleStartMonitoring = () => {
    monitoringService.startMonitoring(refreshInterval * 1000);
    setIsMonitoring(true);
  };

  const handleStopMonitoring = () => {
    monitoringService.stopMonitoring();
    setIsMonitoring(false);
  };

  const handleRefresh = () => {
    loadInitialData();
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setActiveTab(newValue);
  };

  const handleAlertClick = (alert: AlertType) => {
    setSelectedAlert(alert);
    setAlertDetailsOpen(true);
  };

  const handleAcknowledgeAlert = (alertId: string) => {
    monitoringService.acknowledgeAlert(alertId, 'admin');
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId ? { ...alert, acknowledged: true } : alert
    ));
  };

  const handleResolveAlert = (alertId: string) => {
    monitoringService.resolveAlert(alertId);
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId ? { ...alert, resolved: true, acknowledged: true } : alert
    ));
  };

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms.toFixed(0)}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    if (ms < 3600000) return `${(ms / 60000).toFixed(1)}m`;
    return `${(ms / 3600000).toFixed(1)}h`;
  };

  const getMetricTrend = (metricPath: string): number => {
    if (metrics.length < 2) return 0;
    
    const recent = metrics.slice(-10);
    const getValue = (m: PerformanceMetrics) => {
      const parts = metricPath.split('.');
      let value: any = m;
      for (const part of parts) {
        if (value && typeof value === 'object' && part in value) {
          value = value[part];
        } else {
          return 0;
        }
      }
      return typeof value === 'number' ? value : 0;
    };
    
    const firstHalf = recent.slice(0, Math.floor(recent.length / 2));
    const secondHalf = recent.slice(Math.floor(recent.length / 2));
    
    const firstAvg = firstHalf.reduce((sum, m) => sum + getValue(m), 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((sum, m) => sum + getValue(m), 0) / secondHalf.length;
    
    return firstAvg === 0 ? 0 : ((secondAvg - firstAvg) / firstAvg) * 100;
  };

  const renderMetricCard = (
    title: string,
    value: string | number,
    unit: string = '',
    trend?: number,
    color: string = colors.primary,
    icon?: React.ReactNode
  ) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
          <Typography variant="h6" color="textSecondary">
            {title}
          </Typography>
          {icon}
        </Box>
        <Typography variant="h4" color={color} fontWeight="bold">
          {typeof value === 'number' ? value.toFixed(2) : value}{unit}
        </Typography>
        {trend !== undefined && (
          <Box display="flex" alignItems="center" mt={1}>
            {trend > 0 ? (
              <TrendingUp color="success" fontSize="small" />
            ) : trend < 0 ? (
              <TrendingDown color="error" fontSize="small" />
            ) : null}
            <Typography
              variant="body2"
              color={trend > 0 ? 'success.main' : trend < 0 ? 'error.main' : 'textSecondary'}
              ml={0.5}
            >
              {trend > 0 ? '+' : ''}{trend.toFixed(1)}%
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  const renderSystemOverview = () => {
    if (!latestMetrics) return null;

    const { system, quantum, application } = latestMetrics;

    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'CPU Usage',
            system.cpu.usage,
            '%',
            getMetricTrend('system.cpu.usage'),
            system.cpu.usage > 80 ? colors.error : system.cpu.usage > 60 ? colors.warning : colors.success,
            <Speed />
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'Memory Usage',
            system.memory.usage,
            '%',
            getMetricTrend('system.memory.usage'),
            system.memory.usage > 85 ? colors.error : system.memory.usage > 70 ? colors.warning : colors.success,
            <Memory />
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'Disk Usage',
            system.disk.usage,
            '%',
            getMetricTrend('system.disk.usage'),
            system.disk.usage > 90 ? colors.error : system.disk.usage > 75 ? colors.warning : colors.success,
            <Storage />
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'Network Latency',
            system.network.latency,
            'ms',
            getMetricTrend('system.network.latency'),
            system.network.latency > 100 ? colors.error : system.network.latency > 50 ? colors.warning : colors.success,
            <NetworkCheck />
          )}
        </Grid>

        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'Quantum Advantage',
            quantum.advantage.advantageScore,
            '/100',
            getMetricTrend('quantum.advantage.advantageScore'),
            colors.quantum,
            <Assessment />
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'Quantum Error Rate',
            quantum.errors.errorRate,
            '%',
            getMetricTrend('quantum.errors.errorRate'),
            quantum.errors.errorRate > 5 ? colors.error : quantum.errors.errorRate > 2 ? colors.warning : colors.success
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'Response Time',
            application.response.averageResponseTime,
            'ms',
            getMetricTrend('application.response.averageResponseTime'),
            application.response.averageResponseTime > 1000 ? colors.error : application.response.averageResponseTime > 500 ? colors.warning : colors.success
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderMetricCard(
            'Active Users',
            application.users.activeUsers,
            '',
            getMetricTrend('application.users.activeUsers'),
            colors.info
          )}
        </Grid>

        {/* Performance Charts */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Performance Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={metrics.slice(-20)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                  />
                  <YAxis />
                  <RechartsTooltip 
                    labelFormatter={(value) => new Date(value).toLocaleString()}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="system.cpu.usage" 
                    stroke={colors.primary} 
                    name="CPU %"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="system.memory.usage" 
                    stroke={colors.secondary} 
                    name="Memory %"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="system.disk.usage" 
                    stroke={colors.warning} 
                    name="Disk %"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quantum Performance
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={metrics.slice(-20)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                  />
                  <YAxis />
                  <RechartsTooltip 
                    labelFormatter={(value) => new Date(value).toLocaleString()}
                  />
                  <Legend />
                  <Area 
                    type="monotone" 
                    dataKey="quantum.advantage.advantageScore" 
                    stroke={colors.quantum} 
                    fill={colors.quantum}
                    fillOpacity={0.3}
                    name="Advantage Score"
                  />
                  <Area 
                    type="monotone" 
                    dataKey="quantum.advantage.efficiency" 
                    stroke={colors.success} 
                    fill={colors.success}
                    fillOpacity={0.3}
                    name="Efficiency %"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderAlertsPanel = () => {
    const unresolvedAlerts = alerts.filter(alert => !alert.resolved);
    const criticalAlerts = unresolvedAlerts.filter(alert => alert.severity === 'critical');
    const warningAlerts = unresolvedAlerts.filter(alert => alert.severity === 'warning');

    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          {renderMetricCard(
            'Critical Alerts',
            criticalAlerts.length,
            '',
            undefined,
            colors.error,
            <Error />
          )}
        </Grid>
        <Grid item xs={12} md={4}>
          {renderMetricCard(
            'Warning Alerts',
            warningAlerts.length,
            '',
            undefined,
            colors.warning,
            <Warning />
          )}
        </Grid>
        <Grid item xs={12} md={4}>
          {renderMetricCard(
            'Total Unresolved',
            unresolvedAlerts.length,
            '',
            undefined,
            colors.info,
            <Notifications />
          )}
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Alerts
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Severity</TableCell>
                      <TableCell>Category</TableCell>
                      <TableCell>Title</TableCell>
                      <TableCell>Metric</TableCell>
                      <TableCell>Value</TableCell>
                      <TableCell>Threshold</TableCell>
                      <TableCell>Time</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {alerts.slice(0, 10).map((alert) => (
                      <TableRow key={alert.id}>
                        <TableCell>
                          <Chip
                            label={alert.severity}
                            color={
                              alert.severity === 'critical' ? 'error' :
                              alert.severity === 'warning' ? 'warning' :
                              alert.severity === 'error' ? 'error' : 'info'
                            }
                            size="small"
                          />
                        </TableCell>
                        <TableCell>{alert.category}</TableCell>
                        <TableCell>{alert.title}</TableCell>
                        <TableCell>{alert.metric}</TableCell>
                        <TableCell>{alert.currentValue.toFixed(2)}</TableCell>
                        <TableCell>{alert.threshold}</TableCell>
                        <TableCell>{alert.timestamp.toLocaleTimeString()}</TableCell>
                        <TableCell>
                          {alert.resolved ? (
                            <Chip label="Resolved" color="success" size="small" />
                          ) : alert.acknowledged ? (
                            <Chip label="Acknowledged" color="warning" size="small" />
                          ) : (
                            <Chip label="New" color="error" size="small" />
                          )}
                        </TableCell>
                        <TableCell>
                          <Box display="flex" gap={1}>
                            {!alert.acknowledged && (
                              <Button
                                size="small"
                                onClick={() => handleAcknowledgeAlert(alert.id)}
                              >
                                Acknowledge
                              </Button>
                            )}
                            {!alert.resolved && (
                              <Button
                                size="small"
                                color="success"
                                onClick={() => handleResolveAlert(alert.id)}
                              >
                                Resolve
                              </Button>
                            )}
                            <Button
                              size="small"
                              onClick={() => handleAlertClick(alert)}
                            >
                              Details
                            </Button>
                          </Box>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderAnalytics = () => {
    if (!latestMetrics) return null;

    const quantumReport = monitoringService.getQuantumAdvantageReport();
    const performanceSummary = monitoringService.getPerformanceSummary();

    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quantum Advantage Report
              </Typography>
              <Box mb={2}>
                <Typography variant="body2" color="textSecondary">
                  Average Speedup: {quantumReport?.averageSpeedup?.toFixed(2)}x
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Average Efficiency: {quantumReport?.averageEfficiency?.toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Problems Solved: {quantumReport?.problemsSolved}
                </Typography>
              </Box>
              <ResponsiveContainer width="100%" height={200}>
                <RadialBarChart cx="50%" cy="50%" innerRadius="20%" outerRadius="80%" data={[
                  { name: 'Advantage Score', value: quantumReport?.averageAdvantageScore || 0, fill: colors.quantum }
                ]}>
                  <RadialBar dataKey="value" cornerRadius={10} fill={colors.quantum} />
                  <RechartsTooltip />
                </RadialBarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resource Utilization
              </Typography>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'CPU', value: latestMetrics.system.cpu.usage, fill: colors.primary },
                      { name: 'Memory', value: latestMetrics.system.memory.usage, fill: colors.secondary },
                      { name: 'Disk', value: latestMetrics.system.disk.usage, fill: colors.warning },
                      { name: 'Available', value: 100 - (latestMetrics.system.cpu.usage + latestMetrics.system.memory.usage + latestMetrics.system.disk.usage) / 3, fill: colors.success },
                    ]}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label
                  >
                  </Pie>
                  <RechartsTooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Application Performance Metrics
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={metrics.slice(-10)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                  />
                  <YAxis />
                  <RechartsTooltip 
                    labelFormatter={(value) => new Date(value).toLocaleString()}
                  />
                  <Legend />
                  <Bar dataKey="application.response.averageResponseTime" fill={colors.primary} name="Response Time (ms)" />
                  <Bar dataKey="application.throughput.requestsPerSecond" fill={colors.secondary} name="Requests/sec" />
                  <Bar dataKey="application.users.activeUsers" fill={colors.success} name="Active Users" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  return (
    <Box sx={{ width: '100%', bgcolor: 'background.default', minHeight: '100vh' }}>
      {/* Header */}
      <Box sx={{ p: 3, borderBottom: 1, borderColor: 'divider', bgcolor: 'background.paper' }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="h4" fontWeight="bold" color="primary">
              Performance Monitoring Dashboard
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              Real-time quantum platform performance and health monitoring
            </Typography>
          </Box>
          <Box display="flex" gap={2} alignItems="center">
            <FormControlLabel
              control={
                <Switch
                  checked={isMonitoring}
                  onChange={isMonitoring ? handleStopMonitoring : handleStartMonitoring}
                  color="primary"
                />
              }
              label={isMonitoring ? 'Monitoring Active' : 'Start Monitoring'}
            />
            <Tooltip title="Refresh Data">
              <IconButton onClick={handleRefresh}>
                <Refresh />
              </IconButton>
            </Tooltip>
            <Tooltip title="Settings">
              <IconButton onClick={() => setSettingsOpen(true)}>
                <Settings />
              </IconButton>
            </Tooltip>
            <Badge badgeContent={alerts.filter(a => !a.resolved).length} color="error">
              <Notifications />
            </Badge>
          </Box>
        </Box>
      </Box>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={activeTab} onChange={handleTabChange}>
          <Tab icon={<Dashboard />} label="Overview" />
          <Tab icon={<Notifications />} label="Alerts" />
          <Tab icon={<Analytics />} label="Analytics" />
          <Tab icon={<Timeline />} label="History" />
        </Tabs>
      </Box>

      {/* Tab Panels */}
      <TabPanel value={activeTab} index={0}>
        {renderSystemOverview()}
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        {renderAlertsPanel()}
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        {renderAnalytics()}
      </TabPanel>

      <TabPanel value={activeTab} index={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Historical Performance Data
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={metrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="timestamp" 
                  tickFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <YAxis />
                <RechartsTooltip 
                  labelFormatter={(value) => new Date(value).toLocaleString()}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="quantum.advantage.advantageScore" 
                  stroke={colors.quantum} 
                  name="Quantum Advantage"
                />
                <Line 
                  type="monotone" 
                  dataKey="application.response.averageResponseTime" 
                  stroke={colors.primary} 
                  name="Response Time"
                />
                <Line 
                  type="monotone" 
                  dataKey="system.cpu.usage" 
                  stroke={colors.warning} 
                  name="CPU Usage"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Settings Dialog */}
      <Dialog open={settingsOpen} onClose={() => setSettingsOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Monitoring Settings</DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={3} mt={2}>
            <TextField
              label="Refresh Interval (seconds)"
              type="number"
              value={refreshInterval}
              onChange={(e) => setRefreshInterval(Number(e.target.value))}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>Time Range</InputLabel>
              <Select
                value={timeRange}
                onChange={(e) => setTimeRange(e.target.value)}
                label="Time Range"
              >
                <MenuItem value="1h">Last Hour</MenuItem>
                <MenuItem value="6h">Last 6 Hours</MenuItem>
                <MenuItem value="24h">Last 24 Hours</MenuItem>
                <MenuItem value="7d">Last 7 Days</MenuItem>
                <MenuItem value="30d">Last 30 Days</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSettingsOpen(false)}>Cancel</Button>
          <Button onClick={() => setSettingsOpen(false)} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Alert Details Dialog */}
      <Dialog 
        open={alertDetailsOpen} 
        onClose={() => setAlertDetailsOpen(false)} 
        maxWidth="md" 
        fullWidth
      >
        <DialogTitle>Alert Details</DialogTitle>
        <DialogContent>
          {selectedAlert && (
            <Box display="flex" flexDirection="column" gap={2} mt={2}>
              <Typography><strong>ID:</strong> {selectedAlert.id}</Typography>
              <Typography><strong>Severity:</strong> {selectedAlert.severity}</Typography>
              <Typography><strong>Category:</strong> {selectedAlert.category}</Typography>
              <Typography><strong>Title:</strong> {selectedAlert.title}</Typography>
              <Typography><strong>Description:</strong> {selectedAlert.description}</Typography>
              <Typography><strong>Metric:</strong> {selectedAlert.metric}</Typography>
              <Typography><strong>Current Value:</strong> {selectedAlert.currentValue}</Typography>
              <Typography><strong>Threshold:</strong> {selectedAlert.threshold}</Typography>
              <Typography><strong>Timestamp:</strong> {selectedAlert.timestamp.toLocaleString()}</Typography>
              <Typography><strong>Acknowledged:</strong> {selectedAlert.acknowledged ? 'Yes' : 'No'}</Typography>
              <Typography><strong>Resolved:</strong> {selectedAlert.resolved ? 'Yes' : 'No'}</Typography>
              {selectedAlert.assignee && (
                <Typography><strong>Assignee:</strong> {selectedAlert.assignee}</Typography>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAlertDetailsOpen(false)}>Close</Button>
          {selectedAlert && !selectedAlert.acknowledged && (
            <Button 
              onClick={() => {
                handleAcknowledgeAlert(selectedAlert.id);
                setAlertDetailsOpen(false);
              }}
              variant="outlined"
            >
              Acknowledge
            </Button>
          )}
          {selectedAlert && !selectedAlert.resolved && (
            <Button 
              onClick={() => {
                handleResolveAlert(selectedAlert.id);
                setAlertDetailsOpen(false);
              }}
              variant="contained"
              color="success"
            >
              Resolve
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PerformanceMonitoringDashboard;