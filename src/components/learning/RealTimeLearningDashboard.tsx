import React, { useState, useEffect, useCallback } from 'react';
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
  LinearProgress,
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
  Switch,
  FormControlLabel,
  Alert,
  Tooltip,
  IconButton,
  Fab,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Slider,
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  Add,
  Refresh,
  Settings,
  TrendingUp,
  Memory,
  Speed,
  Psychology,
  AutoFixHigh,
  ExpandMore,
  Delete,
  Edit,
  Visibility,
  Timeline,
  Analytics,
  ModelTraining,
  Science,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  BarChart,
  Bar,
  ScatterPlot,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import realTimeLearningService, {
  LearningModel,
  LearningMetrics,
  QuantumCircuitTemplate,
  AdaptiveOptimizer,
  AutoMLConfig,
  TrainingDataPoint,
  RealtimeFeedback,
} from '../../services/realTimeLearningService';

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
      id={`learning-tabpanel-${index}`}
      aria-labelledby={`learning-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const RealTimeLearningDashboard: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [models, setModels] = useState<LearningModel[]>([]);
  const [metrics, setMetrics] = useState<LearningMetrics | null>(null);
  const [circuitTemplates, setCircuitTemplates] = useState<QuantumCircuitTemplate[]>([]);
  const [optimizers, setOptimizers] = useState<AdaptiveOptimizer[]>([]);
  const [autoMLConfig, setAutoMLConfig] = useState<AutoMLConfig | null>(null);
  const [isLearning, setIsLearning] = useState(false);
  const [selectedModel, setSelectedModel] = useState<LearningModel | null>(null);
  const [trainingProgress, setTrainingProgress] = useState<Record<string, number>>({});
  const [realtimeData, setRealtimeData] = useState<any[]>([]);
  
  // Dialog states
  const [createModelDialog, setCreateModelDialog] = useState(false);
  const [modelDetailsDialog, setModelDetailsDialog] = useState(false);
  const [settingsDialog, setSettingsDialog] = useState(false);
  const [optimizeDialog, setOptimizeDialog] = useState(false);
  
  // Form states
  const [newModelForm, setNewModelForm] = useState({
    name: '',
    type: 'quantum_ml' as const,
    algorithm: 'VQC',
    qubits: 4,
    layers: 2,
    learningRate: 0.01,
  });

  // Load initial data
  useEffect(() => {
    loadData();
    setupEventListeners();
    
    // Start real-time updates
    const interval = setInterval(() => {
      updateMetrics();
      updateRealtimeData();
    }, 2000);
    
    return () => {
      clearInterval(interval);
      realTimeLearningService.removeAllListeners();
    };
  }, []);

  const loadData = async () => {
    try {
      setModels(realTimeLearningService.getAllModels());
      setMetrics(realTimeLearningService.getMetrics());
      setCircuitTemplates(realTimeLearningService.getAllCircuitTemplates());
      setOptimizers(realTimeLearningService.getAllOptimizers());
      setAutoMLConfig(realTimeLearningService.getAutoMLConfig());
    } catch (error) {
      console.error('Failed to load learning data:', error);
    }
  };

  const setupEventListeners = () => {
    realTimeLearningService.on('modelCreated', (model: LearningModel) => {
      setModels(prev => [...prev, model]);
    });
    
    realTimeLearningService.on('modelTrained', (model: LearningModel) => {
      setModels(prev => prev.map(m => m.id === model.id ? model : m));
    });
    
    realTimeLearningService.on('trainingProgress', (progress: any) => {
      setTrainingProgress(prev => ({
        ...prev,
        [progress.modelId]: progress.progress,
      }));
    });
    
    realTimeLearningService.on('realTimeLearningStarted', () => {
      setIsLearning(true);
    });
    
    realTimeLearningService.on('realTimeLearningStopped', () => {
      setIsLearning(false);
    });
    
    realTimeLearningService.on('hyperparameterOptimizationComplete', (result: any) => {
      setModels(prev => [...prev, result.optimized]);
    });
  };

  const updateMetrics = () => {
    setMetrics(realTimeLearningService.getMetrics());
  };

  const updateRealtimeData = () => {
    // Simulate real-time performance data
    const newDataPoint = {
      timestamp: new Date().toLocaleTimeString(),
      accuracy: Math.random() * 0.2 + 0.8,
      loss: Math.random() * 0.5,
      quantumAdvantage: Math.random() * 50 + 50,
      convergenceRate: Math.random() * 0.1 + 0.9,
      throughput: Math.random() * 100 + 50,
    };
    
    setRealtimeData(prev => {
      const updated = [...prev, newDataPoint];
      return updated.slice(-20); // Keep last 20 points
    });
  };

  const handleStartLearning = () => {
    realTimeLearningService.startRealTimeLearning();
  };

  const handleStopLearning = () => {
    realTimeLearningService.stopRealTimeLearning();
  };

  const handleCreateModel = async () => {
    try {
      const modelConfig = {
        name: newModelForm.name,
        type: newModelForm.type,
        algorithm: newModelForm.algorithm,
        parameters: {
          qubits: newModelForm.qubits,
          layers: newModelForm.layers,
          learningRate: newModelForm.learningRate,
        },
      };
      
      await realTimeLearningService.createModel(modelConfig);
      setCreateModelDialog(false);
      setNewModelForm({
        name: '',
        type: 'quantum_ml',
        algorithm: 'VQC',
        qubits: 4,
        layers: 2,
        learningRate: 0.01,
      });
    } catch (error) {
      console.error('Failed to create model:', error);
    }
  };

  const handleOptimizeModel = async (modelId: string) => {
    try {
      await realTimeLearningService.optimizeHyperparameters(modelId);
      setOptimizeDialog(false);
    } catch (error) {
      console.error('Failed to optimize model:', error);
    }
  };

  const handleEvolveCircuit = async (templateId: string) => {
    try {
      await realTimeLearningService.evolveCircuitArchitecture(templateId);
      setCircuitTemplates(realTimeLearningService.getAllCircuitTemplates());
    } catch (error) {
      console.error('Failed to evolve circuit:', error);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready': return 'success';
      case 'training': return 'warning';
      case 'updating': return 'info';
      case 'error': return 'error';
      default: return 'default';
    }
  };

  const getAlgorithmIcon = (algorithm: string) => {
    switch (algorithm) {
      case 'VQC': return <Psychology />;
      case 'QSVM': return <Science />;
      case 'QNN': return <ModelTraining />;
      case 'QAOA': return <AutoFixHigh />;
      default: return <Memory />;
    }
  };

  const renderOverviewTab = () => (
    <Grid container spacing={3}>
      {/* Control Panel */}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6">Real-Time Learning Control</Typography>
              <Box>
                <Button
                  variant={isLearning ? "outlined" : "contained"}
                  color={isLearning ? "error" : "primary"}
                  startIcon={isLearning ? <Stop /> : <PlayArrow />}
                  onClick={isLearning ? handleStopLearning : handleStartLearning}
                  sx={{ mr: 1 }}
                >
                  {isLearning ? 'Stop Learning' : 'Start Learning'}
                </Button>
                <IconButton onClick={() => setSettingsDialog(true)}>
                  <Settings />
                </IconButton>
              </Box>
            </Box>
            
            {isLearning && (
              <Alert severity="info" sx={{ mb: 2 }}>
                Real-time learning is active. Models are continuously adapting to new data.
              </Alert>
            )}
            
            <Grid container spacing={2}>
              <Grid item xs={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="primary">
                    {metrics?.activeModels || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Active Models
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="success.main">
                    {((metrics?.averageAccuracy || 0) * 100).toFixed(1)}%
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Avg Accuracy
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="warning.main">
                    {(metrics?.quantumAdvantageGain || 0).toFixed(1)}x
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Quantum Advantage
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={3}>
                <Box textAlign="center">
                  <Typography variant="h4" color="info.main">
                    {metrics?.dataPointsProcessed || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Data Points
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Real-time Performance Charts */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Real-time Performance
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={realtimeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Line type="monotone" dataKey="accuracy" stroke="#2196f3" strokeWidth={2} />
                <Line type="monotone" dataKey="convergenceRate" stroke="#4caf50" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Quantum Advantage Metrics
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={realtimeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <RechartsTooltip />
                <Legend />
                <Area type="monotone" dataKey="quantumAdvantage" stroke="#ff9800" fill="#ff9800" fillOpacity={0.3} />
                <Area type="monotone" dataKey="throughput" stroke="#9c27b0" fill="#9c27b0" fillOpacity={0.3} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Model Performance Radar */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Model Performance Radar
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={[
                {
                  metric: 'Accuracy',
                  value: (metrics?.averageAccuracy || 0) * 100,
                  fullMark: 100,
                },
                {
                  metric: 'Speed',
                  value: 85,
                  fullMark: 100,
                },
                {
                  metric: 'Quantum Advantage',
                  value: (metrics?.quantumAdvantageGain || 0),
                  fullMark: 100,
                },
                {
                  metric: 'Convergence',
                  value: 92,
                  fullMark: 100,
                },
                {
                  metric: 'Efficiency',
                  value: 88,
                  fullMark: 100,
                },
                {
                  metric: 'Adaptability',
                  value: 95,
                  fullMark: 100,
                },
              ]}>
                <PolarGrid />
                <PolarAngleAxis dataKey="metric" />
                <PolarRadiusAxis angle={90} domain={[0, 100]} />
                <Radar name="Performance" dataKey="value" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
              </RadarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
      
      {/* Algorithm Distribution */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Algorithm Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={[
                    { name: 'VQC', value: 35, fill: '#8884d8' },
                    { name: 'QSVM', value: 25, fill: '#82ca9d' },
                    { name: 'QNN', value: 20, fill: '#ffc658' },
                    { name: 'QAOA', value: 15, fill: '#ff7300' },
                    { name: 'VQE', value: 5, fill: '#00ff00' },
                  ]}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {[
                    { name: 'VQC', value: 35, fill: '#8884d8' },
                    { name: 'QSVM', value: 25, fill: '#82ca9d' },
                    { name: 'QNN', value: 20, fill: '#ffc658' },
                    { name: 'QAOA', value: 15, fill: '#ff7300' },
                    { name: 'VQE', value: 5, fill: '#00ff00' },
                  ].map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <RechartsTooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const renderModelsTab = () => (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6">Learning Models</Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setCreateModelDialog(true)}
        >
          Create Model
        </Button>
      </Box>
      
      <Grid container spacing={3}>
        {models.map((model) => (
          <Grid item xs={12} md={6} lg={4} key={model.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                  <Box display="flex" alignItems="center">
                    {getAlgorithmIcon(model.algorithm)}
                    <Box ml={1}>
                      <Typography variant="h6">{model.name}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        {model.algorithm} • v{model.version}
                      </Typography>
                    </Box>
                  </Box>
                  <Chip
                    label={model.status}
                    color={getStatusColor(model.status) as any}
                    size="small"
                  />
                </Box>
                
                {trainingProgress[model.id] && (
                  <Box mb={2}>
                    <Typography variant="body2" gutterBottom>
                      Training Progress: {trainingProgress[model.id].toFixed(1)}%
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={trainingProgress[model.id]}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                )}
                
                <Grid container spacing={1} sx={{ mb: 2 }}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      Accuracy
                    </Typography>
                    <Typography variant="h6">
                      {(model.performance.accuracy * 100).toFixed(1)}%
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      F1 Score
                    </Typography>
                    <Typography variant="h6">
                      {model.performance.f1Score.toFixed(3)}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      Quantum Advantage
                    </Typography>
                    <Typography variant="h6" color="primary">
                      {model.performance.quantumAdvantage.toFixed(1)}x
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      Training Data
                    </Typography>
                    <Typography variant="h6">
                      {model.trainingData.length}
                    </Typography>
                  </Grid>
                </Grid>
                
                <Box display="flex" justifyContent="space-between">
                  <Button
                    size="small"
                    startIcon={<Visibility />}
                    onClick={() => {
                      setSelectedModel(model);
                      setModelDetailsDialog(true);
                    }}
                  >
                    Details
                  </Button>
                  <Button
                    size="small"
                    startIcon={<AutoFixHigh />}
                    onClick={() => handleOptimizeModel(model.id)}
                    disabled={model.status !== 'ready'}
                  >
                    Optimize
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderCircuitsTab = () => (
    <Box>
      <Typography variant="h6" gutterBottom>
        Quantum Circuit Templates
      </Typography>
      
      <Grid container spacing={3}>
        {circuitTemplates.map((template) => (
          <Grid item xs={12} md={6} key={template.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                  <Box>
                    <Typography variant="h6">{template.name}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      {template.qubits} qubits • Depth {template.depth}
                    </Typography>
                  </Box>
                  <Chip
                    label={template.optimizationTarget}
                    color="primary"
                    size="small"
                  />
                </Box>
                
                <Grid container spacing={2} sx={{ mb: 2 }}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      Fidelity
                    </Typography>
                    <Typography variant="h6" color="success.main">
                      {(template.fidelity * 100).toFixed(1)}%
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      Error Rate
                    </Typography>
                    <Typography variant="h6" color="error.main">
                      {(template.errorRate * 100).toFixed(2)}%
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      Gates
                    </Typography>
                    <Typography variant="h6">
                      {template.gates.length}
                    </Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">
                      Parameters
                    </Typography>
                    <Typography variant="h6">
                      {template.parameters.length}
                    </Typography>
                  </Grid>
                </Grid>
                
                <Accordion>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography variant="body2">Circuit Details</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Typography variant="body2" gutterBottom>
                      <strong>Gates:</strong>
                    </Typography>
                    {template.gates.slice(0, 5).map((gate, index) => (
                      <Chip
                        key={index}
                        label={`${gate.type}(${gate.qubits.join(',')})`}
                        size="small"
                        sx={{ mr: 0.5, mb: 0.5 }}
                      />
                    ))}
                    {template.gates.length > 5 && (
                      <Typography variant="body2" color="textSecondary">
                        ... and {template.gates.length - 5} more
                      </Typography>
                    )}
                  </AccordionDetails>
                </Accordion>
                
                <Box display="flex" justifyContent="space-between" mt={2}>
                  <Button
                    size="small"
                    startIcon={<Science />}
                    onClick={() => handleEvolveCircuit(template.id)}
                  >
                    Evolve
                  </Button>
                  <Button size="small" startIcon={<Edit />}>
                    Edit
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );

  const renderAnalyticsTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Learning Analytics
            </Typography>
            
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" gutterBottom>
                  Training Performance Over Time
                </Typography>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={realtimeData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="timestamp" />
                    <YAxis />
                    <RechartsTooltip />
                    <Legend />
                    <Line type="monotone" dataKey="accuracy" stroke="#2196f3" name="Accuracy" />
                    <Line type="monotone" dataKey="loss" stroke="#f44336" name="Loss" />
                  </LineChart>
                </ResponsiveContainer>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle1" gutterBottom>
                  Resource Utilization
                </Typography>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={[
                    { name: 'CPU', usage: 75, limit: 100 },
                    { name: 'Memory', usage: 60, limit: 100 },
                    { name: 'Quantum', usage: 45, limit: 100 },
                    { name: 'Network', usage: 30, limit: 100 },
                  ]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <RechartsTooltip />
                    <Bar dataKey="usage" fill="#8884d8" />
                    <Bar dataKey="limit" fill="#e0e0e0" />
                  </BarChart>
                </ResponsiveContainer>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Model Comparison
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Model</TableCell>
                    <TableCell align="right">Accuracy</TableCell>
                    <TableCell align="right">F1 Score</TableCell>
                    <TableCell align="right">Quantum Advantage</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {models.slice(0, 5).map((model) => (
                    <TableRow key={model.id}>
                      <TableCell>{model.name}</TableCell>
                      <TableCell align="right">
                        {(model.performance.accuracy * 100).toFixed(1)}%
                      </TableCell>
                      <TableCell align="right">
                        {model.performance.f1Score.toFixed(3)}
                      </TableCell>
                      <TableCell align="right">
                        {model.performance.quantumAdvantage.toFixed(1)}x
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      </Grid>
      
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Learning Efficiency Metrics
            </Typography>
            <Box>
              <Typography variant="body2" gutterBottom>
                Convergence Speed: {((metrics?.convergenceSpeed || 0) * 100).toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(metrics?.convergenceSpeed || 0) * 100}
                sx={{ mb: 2, height: 8, borderRadius: 4 }}
              />
              
              <Typography variant="body2" gutterBottom>
                Adaptation Rate: {((metrics?.adaptationRate || 0) * 100).toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(metrics?.adaptationRate || 0) * 100}
                sx={{ mb: 2, height: 8, borderRadius: 4 }}
              />
              
              <Typography variant="body2" gutterBottom>
                Resource Efficiency: {((metrics?.resourceUtilization || 0) * 100).toFixed(1)}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={(metrics?.resourceUtilization || 0) * 100}
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Overview" icon={<Analytics />} />
          <Tab label="Models" icon={<ModelTraining />} />
          <Tab label="Circuits" icon={<Memory />} />
          <Tab label="Analytics" icon={<Timeline />} />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        {renderOverviewTab()}
      </TabPanel>
      <TabPanel value={tabValue} index={1}>
        {renderModelsTab()}
      </TabPanel>
      <TabPanel value={tabValue} index={2}>
        {renderCircuitsTab()}
      </TabPanel>
      <TabPanel value={tabValue} index={3}>
        {renderAnalyticsTab()}
      </TabPanel>

      {/* Create Model Dialog */}
      <Dialog open={createModelDialog} onClose={() => setCreateModelDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Learning Model</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Model Name"
                value={newModelForm.name}
                onChange={(e) => setNewModelForm(prev => ({ ...prev, name: e.target.value }))}
              />
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Algorithm</InputLabel>
                <Select
                  value={newModelForm.algorithm}
                  onChange={(e) => setNewModelForm(prev => ({ ...prev, algorithm: e.target.value }))}
                >
                  <MenuItem value="VQC">Variational Quantum Classifier</MenuItem>
                  <MenuItem value="QSVM">Quantum Support Vector Machine</MenuItem>
                  <MenuItem value="QNN">Quantum Neural Network</MenuItem>
                  <MenuItem value="QAOA">Quantum Approximate Optimization</MenuItem>
                  <MenuItem value="VQE">Variational Quantum Eigensolver</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={6}>
              <FormControl fullWidth>
                <InputLabel>Type</InputLabel>
                <Select
                  value={newModelForm.type}
                  onChange={(e) => setNewModelForm(prev => ({ ...prev, type: e.target.value as any }))}
                >
                  <MenuItem value="quantum_ml">Quantum ML</MenuItem>
                  <MenuItem value="reinforcement">Reinforcement Learning</MenuItem>
                  <MenuItem value="supervised">Supervised Learning</MenuItem>
                  <MenuItem value="unsupervised">Unsupervised Learning</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={4}>
              <Typography gutterBottom>Qubits: {newModelForm.qubits}</Typography>
              <Slider
                value={newModelForm.qubits}
                onChange={(_, value) => setNewModelForm(prev => ({ ...prev, qubits: value as number }))}
                min={2}
                max={20}
                marks
                valueLabelDisplay="auto"
              />
            </Grid>
            <Grid item xs={4}>
              <Typography gutterBottom>Layers: {newModelForm.layers}</Typography>
              <Slider
                value={newModelForm.layers}
                onChange={(_, value) => setNewModelForm(prev => ({ ...prev, layers: value as number }))}
                min={1}
                max={10}
                marks
                valueLabelDisplay="auto"
              />
            </Grid>
            <Grid item xs={4}>
              <Typography gutterBottom>Learning Rate: {newModelForm.learningRate}</Typography>
              <Slider
                value={newModelForm.learningRate}
                onChange={(_, value) => setNewModelForm(prev => ({ ...prev, learningRate: value as number }))}
                min={0.001}
                max={0.1}
                step={0.001}
                valueLabelDisplay="auto"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateModelDialog(false)}>Cancel</Button>
          <Button onClick={handleCreateModel} variant="contained">Create Model</Button>
        </DialogActions>
      </Dialog>

      {/* Model Details Dialog */}
      <Dialog open={modelDetailsDialog} onClose={() => setModelDetailsDialog(false)} maxWidth="lg" fullWidth>
        <DialogTitle>
          {selectedModel?.name} Details
        </DialogTitle>
        <DialogContent>
          {selectedModel && (
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>Performance Metrics</Typography>
                <TableContainer component={Paper}>
                  <Table>
                    <TableBody>
                      <TableRow>
                        <TableCell>Accuracy</TableCell>
                        <TableCell align="right">{(selectedModel.performance.accuracy * 100).toFixed(2)}%</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Precision</TableCell>
                        <TableCell align="right">{selectedModel.performance.precision.toFixed(3)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Recall</TableCell>
                        <TableCell align="right">{selectedModel.performance.recall.toFixed(3)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>F1 Score</TableCell>
                        <TableCell align="right">{selectedModel.performance.f1Score.toFixed(3)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Loss</TableCell>
                        <TableCell align="right">{selectedModel.performance.loss.toFixed(4)}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Quantum Advantage</TableCell>
                        <TableCell align="right">{selectedModel.performance.quantumAdvantage.toFixed(1)}x</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="h6" gutterBottom>Model Information</Typography>
                <TableContainer component={Paper}>
                  <Table>
                    <TableBody>
                      <TableRow>
                        <TableCell>Algorithm</TableCell>
                        <TableCell align="right">{selectedModel.algorithm}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Type</TableCell>
                        <TableCell align="right">{selectedModel.type}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Version</TableCell>
                        <TableCell align="right">{selectedModel.version}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Status</TableCell>
                        <TableCell align="right">
                          <Chip label={selectedModel.status} color={getStatusColor(selectedModel.status) as any} size="small" />
                        </TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Created</TableCell>
                        <TableCell align="right">{selectedModel.created.toLocaleDateString()}</TableCell>
                      </TableRow>
                      <TableRow>
                        <TableCell>Last Trained</TableCell>
                        <TableCell align="right">{selectedModel.lastTrained.toLocaleDateString()}</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setModelDetailsDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Floating Action Button */}
      <Fab
        color="primary"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        onClick={() => loadData()}
      >
        <Refresh />
      </Fab>
    </Box>
  );
};

export default RealTimeLearningDashboard;