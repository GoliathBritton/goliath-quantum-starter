import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Tabs,
  Tab,
  Button,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  LinearProgress,
  IconButton,
  Tooltip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  CircularProgress
} from '@mui/material';
import {
  Security as SecurityIcon,
  Gavel as ComplianceIcon,
  Public as GlobalIcon,
  Dashboard as DashboardIcon,
  Assessment as AssessmentIcon,
  Report as ReportIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Download as DownloadIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
  TrendingUp as TrendingUpIcon,
  Shield as ShieldIcon,
  CloudDone as CloudDoneIcon
} from '@mui/icons-material';
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
  ResponsiveContainer
} from 'recharts';
import EnterpriseService, {
  ComplianceFramework,
  SecurityFramework,
  GlobalDeployment,
  SecurityAssessment,
  ComplianceAssessment
} from '../../services/enterpriseService';

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
      id={`enterprise-tabpanel-${index}`}
      aria-labelledby={`enterprise-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const EnterpriseDashboard: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [enterpriseService] = useState(() => new EnterpriseService());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // State for compliance
  const [complianceFrameworks, setComplianceFrameworks] = useState<ComplianceFramework[]>([]);
  const [complianceMetrics, setComplianceMetrics] = useState<any>({});
  const [complianceDialogOpen, setComplianceDialogOpen] = useState(false);
  const [selectedCompliance, setSelectedCompliance] = useState<ComplianceFramework | null>(null);

  // State for security
  const [securityFrameworks, setSecurityFrameworks] = useState<SecurityFramework[]>([]);
  const [securityMetrics, setSecurityMetrics] = useState<any>({});
  const [securityDialogOpen, setSecurityDialogOpen] = useState(false);
  const [selectedSecurity, setSelectedSecurity] = useState<SecurityFramework | null>(null);
  const [assessmentDialogOpen, setAssessmentDialogOpen] = useState(false);
  const [assessmentType, setAssessmentType] = useState<SecurityAssessment['type']>('vulnerability');

  // State for global deployment
  const [globalDeployments, setGlobalDeployments] = useState<GlobalDeployment[]>([]);
  const [deploymentMetrics, setDeploymentMetrics] = useState<any>({});
  const [deploymentDialogOpen, setDeploymentDialogOpen] = useState(false);
  const [selectedDeployment, setSelectedDeployment] = useState<GlobalDeployment | null>(null);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [compliance, security, deployments, compMetrics, secMetrics, depMetrics] = await Promise.all([
        enterpriseService.getComplianceFrameworks(),
        enterpriseService.getSecurityFrameworks(),
        enterpriseService.getGlobalDeployments(),
        enterpriseService.getComplianceMetrics(),
        enterpriseService.getSecurityMetrics(),
        enterpriseService.getGlobalDeploymentMetrics()
      ]);

      setComplianceFrameworks(compliance);
      setSecurityFrameworks(security);
      setGlobalDeployments(deployments);
      setComplianceMetrics(compMetrics);
      setSecurityMetrics(secMetrics);
      setDeploymentMetrics(depMetrics);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load enterprise data');
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleComplianceAssessment = async (frameworkId: string) => {
    try {
      await enterpriseService.assessCompliance(frameworkId);
      loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Assessment failed');
    }
  };

  const handleSecurityAssessment = async (frameworkId: string) => {
    try {
      await enterpriseService.conductSecurityAssessment(frameworkId, assessmentType);
      setAssessmentDialogOpen(false);
      loadData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Security assessment failed');
    }
  };

  const handleExportReport = async (type: 'compliance' | 'security', frameworkId: string) => {
    try {
      let report: string;
      if (type === 'compliance') {
        report = await enterpriseService.exportComplianceReport(frameworkId);
      } else {
        report = await enterpriseService.exportSecurityReport(frameworkId);
      }
      
      const blob = new Blob([report], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${type}_report_${frameworkId}_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Export failed');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'compliant':
      case 'active':
      case 'completed':
        return 'success';
      case 'non_compliant':
      case 'failed':
      case 'critical':
        return 'error';
      case 'pending':
      case 'in_progress':
      case 'warning':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compliant':
      case 'active':
      case 'completed':
        return <CheckCircleIcon />;
      case 'non_compliant':
      case 'failed':
      case 'critical':
        return <ErrorIcon />;
      case 'pending':
      case 'in_progress':
      case 'warning':
        return <WarningIcon />;
      default:
        return <ScheduleIcon />;
    }
  };

  const renderOverviewTab = () => {
    const overviewData = [
      {
        title: 'Compliance Status',
        value: `${complianceMetrics.complianceRate || 0}%`,
        icon: <ComplianceIcon />,
        color: '#4CAF50',
        details: `${complianceMetrics.compliantFrameworks || 0}/${complianceMetrics.totalFrameworks || 0} frameworks compliant`
      },
      {
        title: 'Security Maturity',
        value: `${Math.round(securityMetrics.averageMaturityLevel || 0)}/5`,
        icon: <SecurityIcon />,
        color: '#2196F3',
        details: `${securityMetrics.openIncidents || 0} open incidents`
      },
      {
        title: 'Global Coverage',
        value: `${Math.round(deploymentMetrics.globalCoverage || 0)}%`,
        icon: <GlobalIcon />,
        color: '#FF9800',
        details: `${deploymentMetrics.activeRegions || 0}/${deploymentMetrics.totalRegions || 0} regions active`
      },
      {
        title: 'Total Deployments',
        value: deploymentMetrics.totalDeployments || 0,
        icon: <CloudDoneIcon />,
        color: '#9C27B0',
        details: 'Worldwide quantum platform deployment'
      }
    ];

    const complianceChartData = [
      { name: 'Compliant', value: complianceMetrics.compliantFrameworks || 0, color: '#4CAF50' },
      { name: 'Pending', value: complianceMetrics.pendingFrameworks || 0, color: '#FF9800' },
      { name: 'Non-Compliant', value: complianceMetrics.nonCompliantFrameworks || 0, color: '#F44336' }
    ];

    const securityTrendData = [
      { month: 'Jan', incidents: 12, resolved: 10 },
      { month: 'Feb', incidents: 8, resolved: 9 },
      { month: 'Mar', incidents: 15, resolved: 14 },
      { month: 'Apr', incidents: 6, resolved: 8 },
      { month: 'May', incidents: 10, resolved: 11 },
      { month: 'Jun', incidents: 4, resolved: 6 }
    ];

    return (
      <Grid container spacing={3}>
        {/* Overview Cards */}
        <Grid item xs={12}>
          <Grid container spacing={3}>
            {overviewData.map((item, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      <Box
                        sx={{
                          backgroundColor: item.color,
                          color: 'white',
                          borderRadius: 1,
                          p: 1,
                          mr: 2
                        }}
                      >
                        {item.icon}
                      </Box>
                      <Box>
                        <Typography variant="h4" component="div">
                          {item.value}
                        </Typography>
                        <Typography variant="h6" color="text.secondary">
                          {item.title}
                        </Typography>
                      </Box>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {item.details}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Compliance Status Distribution
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={complianceChartData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {complianceChartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Security Incident Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={securityTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <RechartsTooltip />
                  <Legend />
                  <Line type="monotone" dataKey="incidents" stroke="#f44336" name="New Incidents" />
                  <Line type="monotone" dataKey="resolved" stroke="#4caf50" name="Resolved" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Enterprise Activities
              </Typography>
              <List>
                <ListItem>
                  <ListItemIcon>
                    <CheckCircleIcon color="success" />
                  </ListItemIcon>
                  <ListItemText
                    primary="SOC 2 Type II Audit Completed"
                    secondary="Compliance framework assessment passed - 2 hours ago"
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemIcon>
                    <SecurityIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Security Assessment Initiated"
                    secondary="NIST Cybersecurity Framework vulnerability scan started - 4 hours ago"
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemIcon>
                    <GlobalIcon color="warning" />
                  </ListItemIcon>
                  <ListItemText
                    primary="New Region Deployment"
                    secondary="Asia-Pacific quantum platform deployment in progress - 1 day ago"
                  />
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemIcon>
                    <ReportIcon color="info" />
                  </ListItemIcon>
                  <ListItemText
                    primary="Compliance Report Generated"
                    secondary="GDPR compliance report exported for Q2 review - 2 days ago"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  const renderComplianceTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5">Compliance Management</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setComplianceDialogOpen(true)}
          >
            Add Framework
          </Button>
        </Box>
      </Grid>

      <Grid item xs={12}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Framework</TableCell>
                <TableCell>Version</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Last Audit</TableCell>
                <TableCell>Next Audit</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {complianceFrameworks.map((framework) => (
                <TableRow key={framework.id}>
                  <TableCell>
                    <Box>
                      <Typography variant="subtitle2">{framework.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {framework.description}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{framework.version}</TableCell>
                  <TableCell>
                    <Chip
                      icon={getStatusIcon(framework.status)}
                      label={framework.status}
                      color={getStatusColor(framework.status) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {framework.lastAudit.toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    {framework.nextAudit.toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <Tooltip title="Run Assessment">
                      <IconButton
                        size="small"
                        onClick={() => handleComplianceAssessment(framework.id)}
                      >
                        <AssessmentIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Export Report">
                      <IconButton
                        size="small"
                        onClick={() => handleExportReport('compliance', framework.id)}
                      >
                        <DownloadIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        onClick={() => {
                          setSelectedCompliance(framework);
                          setComplianceDialogOpen(true);
                        }}
                      >
                        <ViewIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </Grid>
  );

  const renderSecurityTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5">Security Management</Typography>
          <Box>
            <Button
              variant="outlined"
              startIcon={<AssessmentIcon />}
              onClick={() => setAssessmentDialogOpen(true)}
              sx={{ mr: 2 }}
            >
              Run Assessment
            </Button>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setSecurityDialogOpen(true)}
            >
              Add Framework
            </Button>
          </Box>
        </Box>
      </Grid>

      <Grid item xs={12}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Framework</TableCell>
                <TableCell>Version</TableCell>
                <TableCell>Maturity Level</TableCell>
                <TableCell>Domains</TableCell>
                <TableCell>Incidents</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {securityFrameworks.map((framework) => (
                <TableRow key={framework.id}>
                  <TableCell>
                    <Box>
                      <Typography variant="subtitle2">{framework.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {framework.description}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{framework.version}</TableCell>
                  <TableCell>
                    <Box display="flex" alignItems="center">
                      <LinearProgress
                        variant="determinate"
                        value={(framework.maturityLevel.overall / 5) * 100}
                        sx={{ width: 100, mr: 1 }}
                      />
                      <Typography variant="body2">
                        {framework.maturityLevel.overall}/5
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{framework.domains.length}</TableCell>
                  <TableCell>
                    <Chip
                      label={framework.incidents.length}
                      color={framework.incidents.length > 0 ? 'warning' : 'success'}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Tooltip title="Export Report">
                      <IconButton
                        size="small"
                        onClick={() => handleExportReport('security', framework.id)}
                      >
                        <DownloadIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        onClick={() => {
                          setSelectedSecurity(framework);
                          setSecurityDialogOpen(true);
                        }}
                      >
                        <ViewIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </Grid>
  );

  const renderGlobalDeploymentTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h5">Global Deployment</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setDeploymentDialogOpen(true)}
          >
            Add Deployment
          </Button>
        </Box>
      </Grid>

      <Grid item xs={12}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Deployment</TableCell>
                <TableCell>Regions</TableCell>
                <TableCell>Architecture</TableCell>
                <TableCell>Performance</TableCell>
                <TableCell>Disaster Recovery</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {globalDeployments.map((deployment) => (
                <TableRow key={deployment.id}>
                  <TableCell>
                    <Box>
                      <Typography variant="subtitle2">{deployment.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {deployment.description}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={`${deployment.regions.length} regions`}
                      color="primary"
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={deployment.architecture.pattern}
                      variant="outlined"
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2">
                        Availability: {deployment.performance.sla.availability.current}%
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Target: {deployment.performance.sla.availability.target}%
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2">
                        RTO: {deployment.disaster.strategy.rto}min
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        RPO: {deployment.disaster.strategy.rpo}min
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Tooltip title="View Details">
                      <IconButton
                        size="small"
                        onClick={() => {
                          setSelectedDeployment(deployment);
                          setDeploymentDialogOpen(true);
                        }}
                      >
                        <ViewIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Grid>
    </Grid>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%' }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="enterprise dashboard tabs">
          <Tab icon={<DashboardIcon />} label="Overview" />
          <Tab icon={<ComplianceIcon />} label="Compliance" />
          <Tab icon={<SecurityIcon />} label="Security" />
          <Tab icon={<GlobalIcon />} label="Global Deployment" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        {renderOverviewTab()}
      </TabPanel>
      <TabPanel value={tabValue} index={1}>
        {renderComplianceTab()}
      </TabPanel>
      <TabPanel value={tabValue} index={2}>
        {renderSecurityTab()}
      </TabPanel>
      <TabPanel value={tabValue} index={3}>
        {renderGlobalDeploymentTab()}
      </TabPanel>

      {/* Security Assessment Dialog */}
      <Dialog open={assessmentDialogOpen} onClose={() => setAssessmentDialogOpen(false)}>
        <DialogTitle>Run Security Assessment</DialogTitle>
        <DialogContent>
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Assessment Type</InputLabel>
            <Select
              value={assessmentType}
              onChange={(e) => setAssessmentType(e.target.value as SecurityAssessment['type'])}
            >
              <MenuItem value="vulnerability">Vulnerability Assessment</MenuItem>
              <MenuItem value="penetration">Penetration Testing</MenuItem>
              <MenuItem value="compliance">Compliance Assessment</MenuItem>
              <MenuItem value="risk">Risk Assessment</MenuItem>
              <MenuItem value="architecture">Architecture Review</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAssessmentDialogOpen(false)}>Cancel</Button>
          <Button
            onClick={() => {
              if (securityFrameworks.length > 0) {
                handleSecurityAssessment(securityFrameworks[0].id);
              }
            }}
            variant="contained"
          >
            Start Assessment
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default EnterpriseDashboard;