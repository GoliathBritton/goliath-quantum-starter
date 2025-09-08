import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  IconButton,
  Tooltip,
  LinearProgress,
  Alert,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Switch,
  FormControlLabel,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Security as SecurityIcon,
  Storage as StorageIcon,
  Speed as SpeedIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Business as BusinessIcon,
  Cloud as CloudIcon,
  Memory as MemoryIcon,
  NetworkCheck as NetworkIcon,
  MonetizationOn as BillingIcon,
  Assessment as MetricsIcon,
  Settings as SettingsIcon,
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
  ResponsiveContainer,
} from 'recharts';
import multiTenantService, {
  Tenant,
  TenantPlan,
  TenantMetrics,
  ResourceUsage,
} from '../../services/multiTenantService';

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
      id={`tenant-tabpanel-${index}`}
      aria-labelledby={`tenant-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const MultiTenantDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [metrics, setMetrics] = useState<Map<string, TenantMetrics>>(new Map());
  const [selectedTenant, setSelectedTenant] = useState<Tenant | null>(null);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [viewDialogOpen, setViewDialogOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form state for tenant creation/editing
  const [formData, setFormData] = useState({
    name: '',
    domain: '',
    subdomain: '',
    planType: 'starter' as 'starter' | 'professional' | 'enterprise' | 'custom',
    status: 'trial' as 'active' | 'suspended' | 'trial' | 'expired',
  });

  useEffect(() => {
    loadTenants();
    loadMetrics();
    
    // Set up real-time updates
    const interval = setInterval(() => {
      loadMetrics();
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const loadTenants = async () => {
    try {
      setLoading(true);
      const allTenants = multiTenantService.getAllTenants();
      setTenants(allTenants);
      setError(null);
    } catch (err) {
      setError('Failed to load tenants');
      console.error('Error loading tenants:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadMetrics = async () => {
    try {
      const allMetrics = await multiTenantService.getAllTenantsMetrics();
      setMetrics(allMetrics);
    } catch (err) {
      console.error('Error loading metrics:', err);
    }
  };

  const handleCreateTenant = async () => {
    try {
      const newTenant = await multiTenantService.createTenant({
        name: formData.name,
        domain: formData.domain,
        subdomain: formData.subdomain,
        plan: getDefaultPlan(formData.planType),
        status: formData.status,
      });
      
      setTenants([...tenants, newTenant]);
      setCreateDialogOpen(false);
      resetForm();
    } catch (err) {
      setError('Failed to create tenant');
      console.error('Error creating tenant:', err);
    }
  };

  const handleUpdateTenant = async () => {
    if (!selectedTenant) return;
    
    try {
      const updatedTenant = await multiTenantService.updateTenant(selectedTenant.id, {
        name: formData.name,
        domain: formData.domain,
        subdomain: formData.subdomain,
        status: formData.status,
      });
      
      setTenants(tenants.map(t => t.id === updatedTenant.id ? updatedTenant : t));
      setEditDialogOpen(false);
      setSelectedTenant(null);
      resetForm();
    } catch (err) {
      setError('Failed to update tenant');
      console.error('Error updating tenant:', err);
    }
  };

  const handleDeleteTenant = async (tenantId: string) => {
    if (!window.confirm('Are you sure you want to delete this tenant?')) return;
    
    try {
      await multiTenantService.deleteTenant(tenantId);
      setTenants(tenants.filter(t => t.id !== tenantId));
    } catch (err) {
      setError('Failed to delete tenant');
      console.error('Error deleting tenant:', err);
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      domain: '',
      subdomain: '',
      planType: 'starter',
      status: 'trial',
    });
  };

  const getDefaultPlan = (planType: string): TenantPlan => {
    const basePlans = {
      starter: {
        type: 'starter' as const,
        features: ['basic_quantum', 'simulator_access', 'api_access', 'email_support'],
        limits: {
          maxUsers: 5,
          maxProjects: 10,
          maxQuantumJobs: 100,
          maxStorageGB: 10,
          maxBandwidthGB: 50,
          maxAPICallsPerMonth: 10000,
          maxConcurrentJobs: 2,
          maxQubits: 10,
          maxCircuitDepth: 100,
        },
      },
      professional: {
        type: 'professional' as const,
        features: ['advanced_quantum', 'hardware_access', 'api_access', 'priority_support', 'analytics'],
        limits: {
          maxUsers: 25,
          maxProjects: 50,
          maxQuantumJobs: 1000,
          maxStorageGB: 100,
          maxBandwidthGB: 500,
          maxAPICallsPerMonth: 100000,
          maxConcurrentJobs: 10,
          maxQubits: 50,
          maxCircuitDepth: 500,
        },
      },
      enterprise: {
        type: 'enterprise' as const,
        features: ['enterprise_quantum', 'dedicated_hardware', 'unlimited_api', '24x7_support', 'custom_analytics', 'sla'],
        limits: {
          maxUsers: 100,
          maxProjects: 200,
          maxQuantumJobs: 10000,
          maxStorageGB: 1000,
          maxBandwidthGB: 5000,
          maxAPICallsPerMonth: 1000000,
          maxConcurrentJobs: 50,
          maxQubits: 100,
          maxCircuitDepth: 1000,
        },
      },
    };
    
    return {
      ...basePlans[planType as keyof typeof basePlans],
      pricing: {
        basePrice: planType === 'starter' ? 99 : planType === 'professional' ? 499 : 2499,
        currency: 'USD',
        billingModel: 'fixed' as const,
        usageRates: [],
        minimumCommitment: 0,
        discounts: [],
      },
      sla: {
        uptime: planType === 'starter' ? 99.5 : planType === 'professional' ? 99.9 : 99.99,
        responseTime: planType === 'starter' ? 1000 : planType === 'professional' ? 500 : 100,
        resolution: planType === 'starter' ? 24 : planType === 'professional' ? 8 : 4,
        support: {
          tier: planType === 'starter' ? 'basic' : planType === 'professional' ? 'standard' : 'enterprise',
          channels: planType === 'starter' ? ['email'] : planType === 'professional' ? ['email', 'chat'] : ['email', 'chat', 'phone'],
          hours: planType === 'starter' ? '9-5 EST' : planType === 'professional' ? '8-8 EST' : '24x7',
          responseTime: planType === 'starter' ? 24 : planType === 'professional' ? 4 : 1,
          escalation: planType !== 'starter',
        },
        penalties: [],
      },
    };
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'trial': return 'info';
      case 'suspended': return 'warning';
      case 'expired': return 'error';
      default: return 'default';
    }
  };

  const getPlanColor = (planType: string) => {
    switch (planType) {
      case 'starter': return 'primary';
      case 'professional': return 'secondary';
      case 'enterprise': return 'success';
      case 'custom': return 'warning';
      default: return 'default';
    }
  };

  const calculateResourceUtilization = (tenant: Tenant) => {
    const usage = tenant.resources.currentUsage;
    const limits = tenant.plan.limits;
    
    return {
      storage: (usage.storageUsedGB / tenant.resources.storage.totalGB) * 100,
      bandwidth: (usage.bandwidthUsedGB / tenant.resources.bandwidth.monthlyLimitGB) * 100,
      users: (usage.activeUsers / limits.maxUsers) * 100,
      apiCalls: (usage.apiCalls / limits.maxAPICallsPerMonth) * 100,
      quantumJobs: (usage.quantumJobs / limits.maxQuantumJobs) * 100,
    };
  };

  const getOverallMetrics = () => {
    const totalTenants = tenants.length;
    const activeTenants = tenants.filter(t => t.status === 'active').length;
    const trialTenants = tenants.filter(t => t.status === 'trial').length;
    const totalRevenue = Array.from(metrics.values()).reduce((sum, m) => sum + m.financial.monthlyRevenue, 0);
    const avgUptime = Array.from(metrics.values()).reduce((sum, m) => sum + m.performance.uptime, 0) / metrics.size || 0;
    
    return {
      totalTenants,
      activeTenants,
      trialTenants,
      totalRevenue,
      avgUptime,
    };
  };

  const overallMetrics = getOverallMetrics();

  // Chart data
  const tenantGrowthData = [
    { month: 'Jan', tenants: 12, revenue: 15000 },
    { month: 'Feb', tenants: 18, revenue: 22000 },
    { month: 'Mar', tenants: 25, revenue: 31000 },
    { month: 'Apr', tenants: 32, revenue: 42000 },
    { month: 'May', tenants: 38, revenue: 48000 },
    { month: 'Jun', tenants: tenants.length, revenue: overallMetrics.totalRevenue },
  ];

  const planDistributionData = [
    { name: 'Starter', value: tenants.filter(t => t.plan.type === 'starter').length, color: '#8884d8' },
    { name: 'Professional', value: tenants.filter(t => t.plan.type === 'professional').length, color: '#82ca9d' },
    { name: 'Enterprise', value: tenants.filter(t => t.plan.type === 'enterprise').length, color: '#ffc658' },
    { name: 'Custom', value: tenants.filter(t => t.plan.type === 'custom').length, color: '#ff7300' },
  ];

  const resourceUtilizationData = tenants.slice(0, 10).map(tenant => {
    const utilization = calculateResourceUtilization(tenant);
    return {
      name: tenant.name.substring(0, 10),
      storage: utilization.storage,
      bandwidth: utilization.bandwidth,
      users: utilization.users,
      api: utilization.apiCalls,
    };
  });

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Multi-Tenant Dashboard
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <BusinessIcon color="primary" />
        Multi-Tenant Dashboard
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Tenants
                  </Typography>
                  <Typography variant="h4">
                    {overallMetrics.totalTenants}
                  </Typography>
                </Box>
                <BusinessIcon color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Active Tenants
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {overallMetrics.activeTenants}
                  </Typography>
                </Box>
                <CheckCircleIcon color="success" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Trial Tenants
                  </Typography>
                  <Typography variant="h4" color="info.main">
                    {overallMetrics.trialTenants}
                  </Typography>
                </Box>
                <SpeedIcon color="info" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Monthly Revenue
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    ${overallMetrics.totalRevenue.toLocaleString()}
                  </Typography>
                </Box>
                <BillingIcon color="success" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Avg Uptime
                  </Typography>
                  <Typography variant="h4" color="primary">
                    {overallMetrics.avgUptime.toFixed(1)}%
                  </Typography>
                </Box>
                <TrendingUpIcon color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
          <Tab label="Tenants" icon={<BusinessIcon />} />
          <Tab label="Analytics" icon={<MetricsIcon />} />
          <Tab label="Resource Usage" icon={<StorageIcon />} />
          <Tab label="Security" icon={<SecurityIcon />} />
          <Tab label="Billing" icon={<BillingIcon />} />
        </Tabs>
      </Box>

      {/* Tenants Tab */}
      <TabPanel value={activeTab} index={0}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">Tenant Management</Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Create Tenant
          </Button>
        </Box>
        
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Domain</TableCell>
                <TableCell>Plan</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Users</TableCell>
                <TableCell>Storage</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {tenants.map((tenant) => {
                const utilization = calculateResourceUtilization(tenant);
                return (
                  <TableRow key={tenant.id}>
                    <TableCell>
                      <Typography variant="subtitle2">{tenant.name}</Typography>
                      <Typography variant="caption" color="textSecondary">
                        {tenant.id}
                      </Typography>
                    </TableCell>
                    <TableCell>{tenant.domain}</TableCell>
                    <TableCell>
                      <Chip
                        label={tenant.plan.type}
                        color={getPlanColor(tenant.plan.type) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={tenant.status}
                        color={getStatusColor(tenant.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {tenant.resources.currentUsage.activeUsers} / {tenant.plan.limits.maxUsers}
                      <LinearProgress
                        variant="determinate"
                        value={utilization.users}
                        sx={{ mt: 0.5, height: 4 }}
                        color={utilization.users > 80 ? 'error' : utilization.users > 60 ? 'warning' : 'primary'}
                      />
                    </TableCell>
                    <TableCell>
                      {tenant.resources.currentUsage.storageUsedGB.toFixed(1)} / {tenant.resources.storage.totalGB} GB
                      <LinearProgress
                        variant="determinate"
                        value={utilization.storage}
                        sx={{ mt: 0.5, height: 4 }}
                        color={utilization.storage > 80 ? 'error' : utilization.storage > 60 ? 'warning' : 'primary'}
                      />
                    </TableCell>
                    <TableCell>
                      {tenant.created.toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Tooltip title="View Details">
                        <IconButton
                          size="small"
                          onClick={() => {
                            setSelectedTenant(tenant);
                            setViewDialogOpen(true);
                          }}
                        >
                          <ViewIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Edit">
                        <IconButton
                          size="small"
                          onClick={() => {
                            setSelectedTenant(tenant);
                            setFormData({
                              name: tenant.name,
                              domain: tenant.domain,
                              subdomain: tenant.subdomain,
                              planType: tenant.plan.type,
                              status: tenant.status,
                            });
                            setEditDialogOpen(true);
                          }}
                        >
                          <EditIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Delete">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteTenant(tenant.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Analytics Tab */}
      <TabPanel value={activeTab} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Tenant Growth & Revenue
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={tenantGrowthData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <RechartsTooltip />
                    <Legend />
                    <Bar yAxisId="left" dataKey="tenants" fill="#8884d8" name="Tenants" />
                    <Line yAxisId="right" type="monotone" dataKey="revenue" stroke="#82ca9d" name="Revenue ($)" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Plan Distribution
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={planDistributionData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {planDistributionData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <RechartsTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Resource Usage Tab */}
      <TabPanel value={activeTab} index={2}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Resource Utilization by Tenant
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={resourceUtilizationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Bar dataKey="storage" stackId="a" fill="#8884d8" name="Storage %" />
                <Bar dataKey="bandwidth" stackId="a" fill="#82ca9d" name="Bandwidth %" />
                <Bar dataKey="users" stackId="a" fill="#ffc658" name="Users %" />
                <Bar dataKey="api" stackId="a" fill="#ff7300" name="API Calls %" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Security Tab */}
      <TabPanel value={activeTab} index={3}>
        <Grid container spacing={3}>
          {tenants.slice(0, 6).map((tenant) => {
            const tenantMetrics = metrics.get(tenant.id);
            return (
              <Grid item xs={12} md={6} key={tenant.id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      {tenant.name} - Security Status
                    </Typography>
                    <List dense>
                      <ListItem>
                        <ListItemIcon>
                          <SecurityIcon color={tenant.security.isolation.level === 'dedicated' ? 'success' : 'warning'} />
                        </ListItemIcon>
                        <ListItemText
                          primary="Isolation Level"
                          secondary={tenant.security.isolation.level}
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <NetworkIcon color={tenant.security.encryption.dataInTransit === 'tls13' ? 'success' : 'warning'} />
                        </ListItemIcon>
                        <ListItemText
                          primary="Encryption"
                          secondary={`${tenant.security.encryption.dataAtRest} / ${tenant.security.encryption.dataInTransit}`}
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <CheckCircleIcon color={tenantMetrics?.security.complianceScore > 90 ? 'success' : 'warning'} />
                        </ListItemIcon>
                        <ListItemText
                          primary="Compliance Score"
                          secondary={`${tenantMetrics?.security.complianceScore.toFixed(1)}%`}
                        />
                      </ListItem>
                      <ListItem>
                        <ListItemIcon>
                          <WarningIcon color={tenantMetrics?.security.threatsDetected > 0 ? 'error' : 'success'} />
                        </ListItemIcon>
                        <ListItemText
                          primary="Threats Detected"
                          secondary={tenantMetrics?.security.threatsDetected || 0}
                        />
                      </ListItem>
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            );
          })}
        </Grid>
      </TabPanel>

      {/* Billing Tab */}
      <TabPanel value={activeTab} index={4}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Tenant</TableCell>
                <TableCell>Plan</TableCell>
                <TableCell>Monthly Revenue</TableCell>
                <TableCell>Usage Costs</TableCell>
                <TableCell>Profit Margin</TableCell>
                <TableCell>Payment Health</TableCell>
                <TableCell>Next Billing</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {tenants.map((tenant) => {
                const tenantMetrics = metrics.get(tenant.id);
                return (
                  <TableRow key={tenant.id}>
                    <TableCell>
                      <Typography variant="subtitle2">{tenant.name}</Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={`${tenant.plan.type} - $${tenant.plan.pricing.basePrice}`}
                        color={getPlanColor(tenant.plan.type) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Typography color="success.main">
                        ${tenantMetrics?.financial.monthlyRevenue.toFixed(2) || '0.00'}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      ${tenantMetrics?.financial.usageCosts.toFixed(2) || '0.00'}
                    </TableCell>
                    <TableCell>
                      <Typography color={tenantMetrics?.financial.profitMargin > 0.3 ? 'success.main' : 'warning.main'}>
                        {((tenantMetrics?.financial.profitMargin || 0) * 100).toFixed(1)}%
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <LinearProgress
                        variant="determinate"
                        value={(tenantMetrics?.financial.paymentHealth || 0) * 100}
                        sx={{ height: 8, borderRadius: 4 }}
                        color={(tenantMetrics?.financial.paymentHealth || 0) > 0.9 ? 'success' : 'warning'}
                      />
                      <Typography variant="caption">
                        {((tenantMetrics?.financial.paymentHealth || 0) * 100).toFixed(1)}%
                      </Typography>
                    </TableCell>
                    <TableCell>
                      {tenant.billing.nextBillingDate.toLocaleDateString()}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Create Tenant Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Tenant</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Tenant Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Subdomain"
                value={formData.subdomain}
                onChange={(e) => setFormData({ ...formData, subdomain: e.target.value })}
                helperText="Will be used as subdomain.quantum-platform.com"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Custom Domain"
                value={formData.domain}
                onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
                helperText="Optional custom domain"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Plan Type</InputLabel>
                <Select
                  value={formData.planType}
                  onChange={(e) => setFormData({ ...formData, planType: e.target.value as any })}
                >
                  <MenuItem value="starter">Starter - $99/month</MenuItem>
                  <MenuItem value="professional">Professional - $499/month</MenuItem>
                  <MenuItem value="enterprise">Enterprise - $2499/month</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Initial Status</InputLabel>
                <Select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value as any })}
                >
                  <MenuItem value="trial">Trial</MenuItem>
                  <MenuItem value="active">Active</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleCreateTenant} variant="contained">
            Create Tenant
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit Tenant Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Edit Tenant</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Tenant Name"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Subdomain"
                value={formData.subdomain}
                onChange={(e) => setFormData({ ...formData, subdomain: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Custom Domain"
                value={formData.domain}
                onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value as any })}
                >
                  <MenuItem value="trial">Trial</MenuItem>
                  <MenuItem value="active">Active</MenuItem>
                  <MenuItem value="suspended">Suspended</MenuItem>
                  <MenuItem value="expired">Expired</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleUpdateTenant} variant="contained">
            Update Tenant
          </Button>
        </DialogActions>
      </Dialog>

      {/* View Tenant Dialog */}
      <Dialog open={viewDialogOpen} onClose={() => setViewDialogOpen(false)} maxWidth="lg" fullWidth>
        <DialogTitle>
          {selectedTenant?.name} - Tenant Details
        </DialogTitle>
        <DialogContent>
          {selectedTenant && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>Basic Information</Typography>
                <List>
                  <ListItem>
                    <ListItemText primary="Tenant ID" secondary={selectedTenant.id} />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Domain" secondary={selectedTenant.domain} />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Subdomain" secondary={selectedTenant.subdomain} />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Created" secondary={selectedTenant.created.toLocaleString()} />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="Last Active" secondary={selectedTenant.lastActive.toLocaleString()} />
                  </ListItem>
                </List>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>Resource Allocation</Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Quantum Qubits"
                      secondary={`${selectedTenant.resources.quantumCompute.allocatedQubits} allocated`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Storage"
                      secondary={`${selectedTenant.resources.storage.totalGB} GB total`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Bandwidth"
                      secondary={`${selectedTenant.resources.bandwidth.monthlyLimitGB} GB/month`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="API Limits"
                      secondary={`${selectedTenant.resources.apiLimits.requestsPerMonth.toLocaleString()} calls/month`}
                    />
                  </ListItem>
                </List>
              </Grid>
              
              <Grid item xs={12}>
                <Typography variant="h6" gutterBottom>Current Usage</Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6} sm={3}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>Active Users</Typography>
                        <Typography variant="h6">
                          {selectedTenant.resources.currentUsage.activeUsers} / {selectedTenant.plan.limits.maxUsers}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>Storage Used</Typography>
                        <Typography variant="h6">
                          {selectedTenant.resources.currentUsage.storageUsedGB.toFixed(1)} GB
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>Quantum Jobs</Typography>
                        <Typography variant="h6">
                          {selectedTenant.resources.currentUsage.quantumJobs}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography color="textSecondary" gutterBottom>API Calls</Typography>
                        <Typography variant="h6">
                          {selectedTenant.resources.currentUsage.apiCalls.toLocaleString()}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setViewDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default MultiTenantDashboard;