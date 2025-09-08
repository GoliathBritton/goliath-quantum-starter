import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Avatar,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Paper,
  IconButton,
  Tooltip,
  Alert,
  LinearProgress,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  ListItemSecondaryAction,
  Divider,
  Switch,
  FormControlLabel,
  Badge,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Slider,
  Stack,
} from '@mui/material';
import {
  Psychology,
  TrendingUp,
  TrendingDown,
  Speed,
  Memory,
  Timeline,
  Assessment,
  Settings,
  PlayArrow,
  Stop,
  Refresh,
  Download,
  Upload,
  Save,
  Share,
  Visibility,
  VisibilityOff,
  ExpandMore,
  AccountBalance,
  LocalShipping,
  ElectricBolt,
  AutoAwesome,
  Science,
  Insights,
  Analytics,
  Dashboard,
  Tune,
  CheckCircle,
  Error,
  Warning,
  Info,
  Lightbulb,
  Bolt,
  Eco,
  AttachMoney,
  Schedule,
  Security,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  AreaChart,
  Area,
  ScatterChart,
  Scatter,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ComposedChart,
  Legend,
} from 'recharts';
import quantumOptimizationService, {
  OptimizationResult,
  PortfolioOptimizationResult,
  SupplyChainOptimizationResult,
  EnergyOptimizationResult,
  Asset,
  PortfolioConstraints,
  SupplyChainNode,
  SupplyChainEdge,
  SupplyChainConstraints,
  EnergySource,
  EnergyDemand,
  EnergyConstraints,
} from '../../services/quantumOptimizationService';

interface OptimizationJob {
  id: string;
  type: 'portfolio' | 'supply_chain' | 'energy' | 'multi_objective';
  name: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  startTime: Date;
  endTime?: Date;
  result?: OptimizationResult;
  parameters: any;
  quantumAdvantage?: number;
  errorMessage?: string;
}

interface QuantumMetrics {
  totalOptimizations: number;
  averageQuantumAdvantage: number;
  totalComputeTime: number;
  successRate: number;
  qubitsUtilized: number;
  circuitDepth: number;
  fidelity: number;
  coherenceTime: number;
}

const QuantumOptimizationDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [optimizationJobs, setOptimizationJobs] = useState<OptimizationJob[]>([]);
  const [selectedJob, setSelectedJob] = useState<OptimizationJob | null>(null);
  const [newJobDialogOpen, setNewJobDialogOpen] = useState(false);
  const [jobType, setJobType] = useState<'portfolio' | 'supply_chain' | 'energy'>('portfolio');
  const [isRunning, setIsRunning] = useState(false);
  const [quantumMetrics, setQuantumMetrics] = useState<QuantumMetrics>({
    totalOptimizations: 1247,
    averageQuantumAdvantage: 410.7,
    totalComputeTime: 15.6,
    successRate: 98.3,
    qubitsUtilized: 127,
    circuitDepth: 1000,
    fidelity: 99.2,
    coherenceTime: 100.5,
  });

  // Sample optimization jobs
  useEffect(() => {
    const sampleJobs: OptimizationJob[] = [
      {
        id: '1',
        type: 'portfolio',
        name: 'Tech Portfolio Optimization',
        status: 'completed',
        progress: 100,
        startTime: new Date(Date.now() - 5 * 60 * 1000),
        endTime: new Date(Date.now() - 2 * 60 * 1000),
        quantumAdvantage: 523.4,
        parameters: {
          assets: 50,
          budget: 1000000,
          riskTolerance: 0.15,
        },
        result: {
          solution: {},
          objectiveValue: 0.127,
          feasible: true,
          iterations: 8192,
          convergenceTime: 180000,
          quantumAdvantage: 523.4,
          confidence: 0.95,
          metadata: {
            algorithm: 'QAOA',
            qubits: 50,
            depth: 150,
            shots: 8192,
            errorRate: 0.008,
          },
        },
      },
      {
        id: '2',
        type: 'supply_chain',
        name: 'Global Supply Chain Optimization',
        status: 'running',
        progress: 67,
        startTime: new Date(Date.now() - 3 * 60 * 1000),
        parameters: {
          nodes: 25,
          edges: 75,
          demandNodes: 10,
        },
      },
      {
        id: '3',
        type: 'energy',
        name: 'Smart Grid Energy Dispatch',
        status: 'completed',
        progress: 100,
        startTime: new Date(Date.now() - 10 * 60 * 1000),
        endTime: new Date(Date.now() - 7 * 60 * 1000),
        quantumAdvantage: 298.1,
        parameters: {
          sources: 15,
          totalDemand: 1500,
          renewableTarget: 0.6,
        },
        result: {
          solution: {},
          objectiveValue: 45600,
          feasible: true,
          iterations: 4096,
          convergenceTime: 120000,
          quantumAdvantage: 298.1,
          confidence: 0.92,
          metadata: {
            algorithm: 'QAOA',
            qubits: 15,
            depth: 80,
            shots: 4096,
            errorRate: 0.012,
          },
        },
      },
      {
        id: '4',
        type: 'portfolio',
        name: 'ESG Portfolio Optimization',
        status: 'failed',
        progress: 0,
        startTime: new Date(Date.now() - 15 * 60 * 1000),
        endTime: new Date(Date.now() - 14 * 60 * 1000),
        errorMessage: 'Quantum circuit depth exceeded maximum limit',
        parameters: {
          assets: 200,
          budget: 5000000,
          esgScore: 0.8,
        },
      },
    ];
    
    setOptimizationJobs(sampleJobs);
  }, []);

  const getStatusColor = (status: OptimizationJob['status']) => {
    switch (status) {
      case 'completed': return 'success';
      case 'running': return 'info';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: OptimizationJob['status']) => {
    switch (status) {
      case 'completed': return <CheckCircle />;
      case 'running': return <CircularProgress size={16} />;
      case 'failed': return <Error />;
      default: return <Schedule />;
    }
  };

  const getTypeIcon = (type: OptimizationJob['type']) => {
    switch (type) {
      case 'portfolio': return <AccountBalance />;
      case 'supply_chain': return <LocalShipping />;
      case 'energy': return <ElectricBolt />;
      default: return <Psychology />;
    }
  };

  const getTypeColor = (type: OptimizationJob['type']) => {
    switch (type) {
      case 'portfolio': return '#1976d2';
      case 'supply_chain': return '#388e3c';
      case 'energy': return '#f57c00';
      default: return '#7b1fa2';
    }
  };

  const formatDuration = (ms: number) => {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  };

  const formatNumber = (num: number, decimals: number = 1) => {
    if (num >= 1000000) return (num / 1000000).toFixed(decimals) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(decimals) + 'K';
    return num.toFixed(decimals);
  };

  const handleStartOptimization = async (type: string, parameters: any) => {
    setIsRunning(true);
    
    const newJob: OptimizationJob = {
      id: Date.now().toString(),
      type: type as any,
      name: `${type.charAt(0).toUpperCase() + type.slice(1)} Optimization`,
      status: 'running',
      progress: 0,
      startTime: new Date(),
      parameters,
    };
    
    setOptimizationJobs([newJob, ...optimizationJobs]);
    setNewJobDialogOpen(false);
    
    // Simulate optimization progress
    const progressInterval = setInterval(() => {
      setOptimizationJobs(jobs => 
        jobs.map(job => 
          job.id === newJob.id 
            ? { ...job, progress: Math.min(job.progress + Math.random() * 20, 100) }
            : job
        )
      );
    }, 1000);
    
    // Simulate completion
    setTimeout(() => {
      clearInterval(progressInterval);
      setOptimizationJobs(jobs => 
        jobs.map(job => 
          job.id === newJob.id 
            ? {
                ...job,
                status: 'completed' as const,
                progress: 100,
                endTime: new Date(),
                quantumAdvantage: Math.random() * 500 + 100,
                result: {
                  solution: {},
                  objectiveValue: Math.random() * 1000,
                  feasible: true,
                  iterations: 4096,
                  convergenceTime: Math.random() * 300000 + 60000,
                  quantumAdvantage: Math.random() * 500 + 100,
                  confidence: 0.9 + Math.random() * 0.1,
                  metadata: {
                    algorithm: 'QAOA',
                    qubits: Math.floor(Math.random() * 100) + 10,
                    depth: Math.floor(Math.random() * 500) + 50,
                    shots: 4096,
                    errorRate: Math.random() * 0.02,
                  },
                },
              }
            : job
        )
      );
      setIsRunning(false);
    }, 8000);
  };

  const handleStopOptimization = (jobId: string) => {
    setOptimizationJobs(jobs => 
      jobs.map(job => 
        job.id === jobId && job.status === 'running'
          ? { ...job, status: 'failed' as const, errorMessage: 'Optimization stopped by user' }
          : job
      )
    );
  };

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );

  // Sample data for charts
  const quantumAdvantageData = [
    { name: 'Jan', advantage: 245.3, classical: 1.0 },
    { name: 'Feb', advantage: 298.7, classical: 1.0 },
    { name: 'Mar', advantage: 356.2, classical: 1.0 },
    { name: 'Apr', advantage: 410.7, classical: 1.0 },
    { name: 'May', advantage: 523.4, classical: 1.0 },
    { name: 'Jun', advantage: 612.8, classical: 1.0 },
  ];

  const optimizationTypeData = [
    { name: 'Portfolio', value: 45, color: '#1976d2' },
    { name: 'Supply Chain', value: 30, color: '#388e3c' },
    { name: 'Energy', value: 20, color: '#f57c00' },
    { name: 'Multi-Objective', value: 5, color: '#7b1fa2' },
  ];

  const performanceData = [
    { name: 'Qubits', value: quantumMetrics.qubitsUtilized, max: 127 },
    { name: 'Depth', value: quantumMetrics.circuitDepth, max: 1000 },
    { name: 'Fidelity', value: quantumMetrics.fidelity, max: 100 },
    { name: 'Success Rate', value: quantumMetrics.successRate, max: 100 },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Quantum Optimization Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={() => window.location.reload()}
          >
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={<PlayArrow />}
            onClick={() => setNewJobDialogOpen(true)}
            disabled={isRunning}
          >
            New Optimization
          </Button>
        </Box>
      </Box>

      {/* Quantum Metrics Overview */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Psychology color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Quantum Advantage</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {quantumMetrics.averageQuantumAdvantage.toFixed(1)}x
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TrendingUp color="success" fontSize="small" />
                <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                  +23.4% this month
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Speed color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Success Rate</Typography>
              </Box>
              <Typography variant="h4">{quantumMetrics.successRate}%</Typography>
              <Typography variant="body2" color="text.secondary">
                {quantumMetrics.totalOptimizations} total optimizations
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Memory color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Qubits Utilized</Typography>
              </Box>
              <Typography variant="h4">{quantumMetrics.qubitsUtilized}</Typography>
              <LinearProgress 
                variant="determinate" 
                value={(quantumMetrics.qubitsUtilized / 127) * 100} 
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Timeline color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Compute Time</Typography>
              </Box>
              <Typography variant="h4">{quantumMetrics.totalComputeTime}h</Typography>
              <Typography variant="body2" color="text.secondary">
                Avg: {(quantumMetrics.totalComputeTime * 60 / quantumMetrics.totalOptimizations).toFixed(1)}min
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quantum Advantage Trend
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={quantumAdvantageData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <RechartsTooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="advantage" 
                    stroke="#1976d2" 
                    strokeWidth={3}
                    name="Quantum Advantage"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="classical" 
                    stroke="#666666" 
                    strokeDasharray="5 5"
                    name="Classical Baseline"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Optimization Types
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={optimizationTypeData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {optimizationTypeData.map((entry, index) => (
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

      {/* Performance Metrics */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Quantum System Performance
          </Typography>
          <Grid container spacing={3}>
            {performanceData.map((metric) => (
              <Grid item xs={12} sm={6} md={3} key={metric.name}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography variant="subtitle1" gutterBottom>
                    {metric.name}
                  </Typography>
                  <Box sx={{ position: 'relative', display: 'inline-flex' }}>
                    <CircularProgress
                      variant="determinate"
                      value={(metric.value / metric.max) * 100}
                      size={80}
                      thickness={4}
                    />
                    <Box
                      sx={{
                        top: 0,
                        left: 0,
                        bottom: 0,
                        right: 0,
                        position: 'absolute',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      <Typography variant="caption" component="div" color="text.secondary">
                        {metric.name === 'Fidelity' || metric.name === 'Success Rate' 
                          ? `${metric.value.toFixed(1)}%`
                          : metric.value.toFixed(0)
                        }
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Optimization Jobs */}
      <Paper sx={{ width: '100%' }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Active Jobs" icon={<PlayArrow />} />
          <Tab label="Job History" icon={<Timeline />} />
          <Tab label="Analytics" icon={<Analytics />} />
          <Tab label="Settings" icon={<Settings />} />
        </Tabs>
      </Paper>

      <TabPanel value={activeTab} index={0}>
        <Grid container spacing={3}>
          {optimizationJobs
            .filter(job => job.status === 'running' || job.status === 'pending')
            .map((job) => (
              <Grid item xs={12} md={6} lg={4} key={job.id}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Avatar sx={{ bgcolor: getTypeColor(job.type), mr: 2 }}>
                          {getTypeIcon(job.type)}
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle1">{job.name}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            Started: {job.startTime.toLocaleTimeString()}
                          </Typography>
                        </Box>
                      </Box>
                      <Chip
                        label={job.status}
                        color={getStatusColor(job.status)}
                        icon={getStatusIcon(job.status)}
                        size="small"
                      />
                    </Box>
                    
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2">Progress</Typography>
                        <Typography variant="body2">{job.progress.toFixed(0)}%</Typography>
                      </Box>
                      <LinearProgress variant="determinate" value={job.progress} />
                    </Box>
                    
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMore />}>
                        <Typography variant="body2">Parameters</Typography>
                      </AccordionSummary>
                      <AccordionDetails>
                        <pre style={{ fontSize: '12px', margin: 0 }}>
                          {JSON.stringify(job.parameters, null, 2)}
                        </pre>
                      </AccordionDetails>
                    </Accordion>
                    
                    <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                      <Button
                        size="small"
                        startIcon={<Visibility />}
                        onClick={() => setSelectedJob(job)}
                      >
                        View
                      </Button>
                      {job.status === 'running' && (
                        <Button
                          size="small"
                          color="error"
                          startIcon={<Stop />}
                          onClick={() => handleStopOptimization(job.id)}
                        >
                          Stop
                        </Button>
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))
          }
          
          {optimizationJobs.filter(job => job.status === 'running' || job.status === 'pending').length === 0 && (
            <Grid item xs={12}>
              <Paper sx={{ p: 4, textAlign: 'center' }}>
                <Psychology sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  No Active Optimizations
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  Start a new quantum optimization to see real-time progress here.
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<PlayArrow />}
                  onClick={() => setNewJobDialogOpen(true)}
                >
                  Start Optimization
                </Button>
              </Paper>
            </Grid>
          )}
        </Grid>
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Duration</TableCell>
                <TableCell>Quantum Advantage</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {optimizationJobs.map((job) => (
                <TableRow key={job.id}>
                  <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar sx={{ bgcolor: getTypeColor(job.type), mr: 2, width: 32, height: 32 }}>
                        {getTypeIcon(job.type)}
                      </Avatar>
                      <Box>
                        <Typography variant="body2">{job.name}</Typography>
                        <Typography variant="caption" color="text.secondary">
                          {job.startTime.toLocaleString()}
                        </Typography>
                      </Box>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Chip label={job.type.replace('_', ' ')} size="small" />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={job.status}
                      color={getStatusColor(job.status)}
                      icon={getStatusIcon(job.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    {job.endTime 
                      ? formatDuration(job.endTime.getTime() - job.startTime.getTime())
                      : job.status === 'running' 
                        ? formatDuration(Date.now() - job.startTime.getTime())
                        : '-'
                    }
                  </TableCell>
                  <TableCell>
                    {job.quantumAdvantage 
                      ? `${job.quantumAdvantage.toFixed(1)}x`
                      : '-'
                    }
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => setSelectedJob(job)}
                    >
                      <Visibility />
                    </IconButton>
                    <IconButton size="small">
                      <Download />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Optimization Performance
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={performanceData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <RechartsTooltip />
                    <Bar dataKey="value" fill="#1976d2" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quantum vs Classical Performance
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <RadarChart data={[
                    { subject: 'Speed', quantum: 95, classical: 20 },
                    { subject: 'Accuracy', quantum: 92, classical: 85 },
                    { subject: 'Scalability', quantum: 88, classical: 30 },
                    { subject: 'Energy Efficiency', quantum: 75, classical: 60 },
                    { subject: 'Cost Effectiveness', quantum: 70, classical: 90 },
                  ]}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis angle={90} domain={[0, 100]} />
                    <Radar name="Quantum" dataKey="quantum" stroke="#1976d2" fill="#1976d2" fillOpacity={0.3} />
                    <Radar name="Classical" dataKey="classical" stroke="#666666" fill="#666666" fillOpacity={0.3} />
                    <Legend />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={activeTab} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quantum System Configuration
                </Typography>
                <Stack spacing={3}>
                  <Box>
                    <Typography gutterBottom>Maximum Qubits</Typography>
                    <Slider
                      value={quantumMetrics.qubitsUtilized}
                      min={1}
                      max={127}
                      valueLabelDisplay="auto"
                      marks={[
                        { value: 1, label: '1' },
                        { value: 64, label: '64' },
                        { value: 127, label: '127' },
                      ]}
                    />
                  </Box>
                  
                  <Box>
                    <Typography gutterBottom>Circuit Depth Limit</Typography>
                    <Slider
                      value={quantumMetrics.circuitDepth}
                      min={10}
                      max={1000}
                      valueLabelDisplay="auto"
                      marks={[
                        { value: 10, label: '10' },
                        { value: 500, label: '500' },
                        { value: 1000, label: '1000' },
                      ]}
                    />
                  </Box>
                  
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Enable Error Mitigation"
                  />
                  
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Quantum Error Correction"
                  />
                  
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Adaptive Circuit Optimization"
                  />
                </Stack>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Algorithm Settings
                </Typography>
                <Stack spacing={3}>
                  <FormControl fullWidth>
                    <InputLabel>Default Algorithm</InputLabel>
                    <Select value="QAOA" label="Default Algorithm">
                      <MenuItem value="QAOA">QAOA</MenuItem>
                      <MenuItem value="VQE">VQE</MenuItem>
                      <MenuItem value="Quantum Annealing">Quantum Annealing</MenuItem>
                    </Select>
                  </FormControl>
                  
                  <TextField
                    label="Default Shots"
                    type="number"
                    value={8192}
                    fullWidth
                  />
                  
                  <TextField
                    label="Convergence Threshold"
                    type="number"
                    value={0.001}
                    step={0.001}
                    fullWidth
                  />
                  
                  <TextField
                    label="Maximum Iterations"
                    type="number"
                    value={10000}
                    fullWidth
                  />
                  
                  <Button variant="contained" startIcon={<Save />}>
                    Save Settings
                  </Button>
                </Stack>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* New Job Dialog */}
      <Dialog
        open={newJobDialogOpen}
        onClose={() => setNewJobDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Start New Quantum Optimization</DialogTitle>
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Optimization Type</InputLabel>
                <Select
                  value={jobType}
                  onChange={(e) => setJobType(e.target.value as any)}
                >
                  <MenuItem value="portfolio">
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <AccountBalance sx={{ mr: 1 }} />
                      Portfolio Optimization
                    </Box>
                  </MenuItem>
                  <MenuItem value="supply_chain">
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <LocalShipping sx={{ mr: 1 }} />
                      Supply Chain Optimization
                    </Box>
                  </MenuItem>
                  <MenuItem value="energy">
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <ElectricBolt sx={{ mr: 1 }} />
                      Energy Grid Optimization
                    </Box>
                  </MenuItem>
                </Select>
              </FormControl>
            </Grid>
            
            {jobType === 'portfolio' && (
              <>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Number of Assets"
                    type="number"
                    defaultValue={50}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Budget ($)"
                    type="number"
                    defaultValue={1000000}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Risk Tolerance"
                    type="number"
                    defaultValue={0.15}
                    step={0.01}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Target Return"
                    type="number"
                    defaultValue={0.12}
                    step={0.01}
                    fullWidth
                  />
                </Grid>
              </>
            )}
            
            {jobType === 'supply_chain' && (
              <>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Number of Nodes"
                    type="number"
                    defaultValue={25}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Number of Edges"
                    type="number"
                    defaultValue={75}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Budget Limit ($)"
                    type="number"
                    defaultValue={500000}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Sustainability Target"
                    type="number"
                    defaultValue={0.8}
                    step={0.1}
                    fullWidth
                  />
                </Grid>
              </>
            )}
            
            {jobType === 'energy' && (
              <>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Number of Sources"
                    type="number"
                    defaultValue={15}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Total Demand (MW)"
                    type="number"
                    defaultValue={1500}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Renewable Target"
                    type="number"
                    defaultValue={0.6}
                    step={0.1}
                    fullWidth
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    label="Max Cost ($/MWh)"
                    type="number"
                    defaultValue={50}
                    fullWidth
                  />
                </Grid>
              </>
            )}
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewJobDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => handleStartOptimization(jobType, { test: 'parameters' })}
            disabled={isRunning}
            startIcon={isRunning ? <CircularProgress size={16} /> : <PlayArrow />}
          >
            {isRunning ? 'Starting...' : 'Start Optimization'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Job Details Dialog */}
      <Dialog
        open={!!selectedJob}
        onClose={() => setSelectedJob(null)}
        maxWidth="lg"
        fullWidth
      >
        {selectedJob && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: getTypeColor(selectedJob.type), mr: 2 }}>
                  {getTypeIcon(selectedJob.type)}
                </Avatar>
                {selectedJob.name}
              </Box>
            </DialogTitle>
            <DialogContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" gutterBottom>Job Information</Typography>
                  <List>
                    <ListItem>
                      <ListItemText primary="Status" secondary={selectedJob.status} />
                    </ListItem>
                    <ListItem>
                      <ListItemText primary="Type" secondary={selectedJob.type} />
                    </ListItem>
                    <ListItem>
                      <ListItemText primary="Started" secondary={selectedJob.startTime.toLocaleString()} />
                    </ListItem>
                    {selectedJob.endTime && (
                      <ListItem>
                        <ListItemText primary="Completed" secondary={selectedJob.endTime.toLocaleString()} />
                      </ListItem>
                    )}
                    {selectedJob.quantumAdvantage && (
                      <ListItem>
                        <ListItemText primary="Quantum Advantage" secondary={`${selectedJob.quantumAdvantage.toFixed(1)}x`} />
                      </ListItem>
                    )}
                  </List>
                </Grid>
                
                {selectedJob.result && (
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>Results</Typography>
                    <List>
                      <ListItem>
                        <ListItemText primary="Objective Value" secondary={selectedJob.result.objectiveValue.toFixed(4)} />
                      </ListItem>
                      <ListItem>
                        <ListItemText primary="Feasible" secondary={selectedJob.result.feasible ? 'Yes' : 'No'} />
                      </ListItem>
                      <ListItem>
                        <ListItemText primary="Iterations" secondary={selectedJob.result.iterations} />
                      </ListItem>
                      <ListItem>
                        <ListItemText primary="Confidence" secondary={`${(selectedJob.result.confidence * 100).toFixed(1)}%`} />
                      </ListItem>
                      <ListItem>
                        <ListItemText primary="Qubits Used" secondary={selectedJob.result.metadata.qubits} />
                      </ListItem>
                      <ListItem>
                        <ListItemText primary="Circuit Depth" secondary={selectedJob.result.metadata.depth} />
                      </ListItem>
                    </List>
                  </Grid>
                )}
                
                <Grid item xs={12}>
                  <Typography variant="h6" gutterBottom>Parameters</Typography>
                  <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <pre style={{ margin: 0, fontSize: '12px' }}>
                      {JSON.stringify(selectedJob.parameters, null, 2)}
                    </pre>
                  </Paper>
                </Grid>
              </Grid>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setSelectedJob(null)}>Close</Button>
              <Button startIcon={<Download />}>Export Results</Button>
              <Button startIcon={<Share />}>Share</Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default QuantumOptimizationDashboard;