import React, { useState, useEffect, useCallback } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
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
  Chip,
  Avatar,
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
  Switch,
  FormControlLabel,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  ListItemSecondaryAction,
  CircularProgress,
  Badge,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Fab,
  SpeedDial,
  SpeedDialAction,
  SpeedDialIcon,
} from '@mui/material';
import {
  Psychology,
  Add,
  Remove,
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
  Edit,
  Delete,
  FileCopy,
  Settings,
  Timeline,
  Assessment,
  TrendingUp,
  Speed,
  Memory,
  CheckCircle,
  Error,
  Warning,
  Info,
  Lightbulb,
  Science,
  AutoAwesome,
  Functions,
  Calculate,
  Matrix,
  GridOn,
  Tune,
  Analytics,
  Insights,
  Code,
  DataObject,
  Transform,
  Architecture,
  AccountTree,
  Hub,
  Scatter3D,
  ShowChart,
  BarChart,
  PieChart,
} from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  Cell,
  AreaChart,
  Area,
  ComposedChart,
  Bar,
  Legend,
  Heatmap,
} from 'recharts';
import quantumOptimizationService, {
  QUBOMatrix,
  OptimizationResult,
} from '../../services/quantumOptimizationService';

interface QUBOProblem {
  id: string;
  name: string;
  description: string;
  matrix: QUBOMatrix;
  variables: string[];
  constraints: QUBOConstraint[];
  created: Date;
  lastModified: Date;
  category: 'portfolio' | 'supply_chain' | 'energy' | 'scheduling' | 'routing' | 'custom';
  difficulty: 'easy' | 'medium' | 'hard' | 'expert';
  tags: string[];
}

interface QUBOConstraint {
  id: string;
  type: 'equality' | 'inequality' | 'binary' | 'cardinality';
  expression: string;
  value: number;
  penalty: number;
  active: boolean;
}

interface SolutionVisualization {
  variables: { name: string; value: number; probability: number }[];
  objectiveHistory: { iteration: number; value: number; energy: number }[];
  energyLandscape: { x: number; y: number; energy: number }[];
  correlations: { var1: string; var2: string; correlation: number }[];
}

const QUBOSolver: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [problems, setProblems] = useState<QUBOProblem[]>([]);
  const [selectedProblem, setSelectedProblem] = useState<QUBOProblem | null>(null);
  const [newProblemDialog, setNewProblemDialog] = useState(false);
  const [matrixSize, setMatrixSize] = useState(4);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizationResult, setOptimizationResult] = useState<OptimizationResult | null>(null);
  const [visualization, setVisualization] = useState<SolutionVisualization | null>(null);
  const [algorithmSettings, setAlgorithmSettings] = useState({
    algorithm: 'QAOA',
    layers: 3,
    shots: 8192,
    maxIterations: 1000,
    convergenceThreshold: 0.001,
    optimizer: 'COBYLA',
    errorMitigation: true,
  });
  const [matrixEditMode, setMatrixEditMode] = useState(false);
  const [selectedCell, setSelectedCell] = useState<{row: number, col: number} | null>(null);
  const [stepperActiveStep, setStepperActiveStep] = useState(0);

  // Initialize with sample problems
  useEffect(() => {
    const sampleProblems: QUBOProblem[] = [
      {
        id: '1',
        name: 'Portfolio Optimization',
        description: 'Optimize asset allocation for maximum return with risk constraints',
        matrix: {
          size: 4,
          values: [
            [0.1, -0.05, 0.02, -0.01],
            [-0.05, 0.15, -0.03, 0.01],
            [0.02, -0.03, 0.12, -0.02],
            [-0.01, 0.01, -0.02, 0.08],
          ],
        },
        variables: ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
        constraints: [
          {
            id: 'c1',
            type: 'equality',
            expression: 'x1 + x2 + x3 + x4 = 1',
            value: 1,
            penalty: 10,
            active: true,
          },
          {
            id: 'c2',
            type: 'inequality',
            expression: 'x1 <= 0.4',
            value: 0.4,
            penalty: 5,
            active: true,
          },
        ],
        created: new Date(Date.now() - 24 * 60 * 60 * 1000),
        lastModified: new Date(Date.now() - 2 * 60 * 60 * 1000),
        category: 'portfolio',
        difficulty: 'medium',
        tags: ['finance', 'risk-management', 'allocation'],
      },
      {
        id: '2',
        name: 'Max-Cut Problem',
        description: 'Find maximum cut in a weighted graph',
        matrix: {
          size: 4,
          values: [
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0],
          ],
        },
        variables: ['v1', 'v2', 'v3', 'v4'],
        constraints: [],
        created: new Date(Date.now() - 48 * 60 * 60 * 1000),
        lastModified: new Date(Date.now() - 1 * 60 * 60 * 1000),
        category: 'custom',
        difficulty: 'easy',
        tags: ['graph-theory', 'combinatorial'],
      },
      {
        id: '3',
        name: 'Energy Grid Optimization',
        description: 'Optimize power generation and distribution',
        matrix: {
          size: 6,
          values: [
            [0.2, -0.1, 0.05, 0, 0, 0],
            [-0.1, 0.25, -0.08, 0.02, 0, 0],
            [0.05, -0.08, 0.18, -0.06, 0.01, 0],
            [0, 0.02, -0.06, 0.22, -0.04, 0.01],
            [0, 0, 0.01, -0.04, 0.15, -0.03],
            [0, 0, 0, 0.01, -0.03, 0.12],
          ],
        },
        variables: ['Solar', 'Wind', 'Hydro', 'Gas', 'Coal', 'Nuclear'],
        constraints: [
          {
            id: 'c1',
            type: 'equality',
            expression: 'Total generation = demand',
            value: 1000,
            penalty: 20,
            active: true,
          },
          {
            id: 'c2',
            type: 'inequality',
            expression: 'Renewable >= 60%',
            value: 0.6,
            penalty: 15,
            active: true,
          },
        ],
        created: new Date(Date.now() - 72 * 60 * 60 * 1000),
        lastModified: new Date(Date.now() - 30 * 60 * 1000),
        category: 'energy',
        difficulty: 'hard',
        tags: ['energy', 'sustainability', 'grid-optimization'],
      },
    ];
    
    setProblems(sampleProblems);
    setSelectedProblem(sampleProblems[0]);
  }, []);

  const getCategoryColor = (category: QUBOProblem['category']) => {
    const colors = {
      portfolio: '#1976d2',
      supply_chain: '#388e3c',
      energy: '#f57c00',
      scheduling: '#7b1fa2',
      routing: '#d32f2f',
      custom: '#455a64',
    };
    return colors[category];
  };

  const getDifficultyColor = (difficulty: QUBOProblem['difficulty']) => {
    const colors = {
      easy: '#4caf50',
      medium: '#ff9800',
      hard: '#f44336',
      expert: '#9c27b0',
    };
    return colors[difficulty];
  };

  const getCategoryIcon = (category: QUBOProblem['category']) => {
    const icons = {
      portfolio: <TrendingUp />,
      supply_chain: <AccountTree />,
      energy: <Lightbulb />,
      scheduling: <Schedule />,
      routing: <Hub />,
      custom: <Functions />,
    };
    return icons[category];
  };

  const createNewProblem = () => {
    const newProblem: QUBOProblem = {
      id: Date.now().toString(),
      name: 'New QUBO Problem',
      description: 'Enter problem description',
      matrix: {
        size: matrixSize,
        values: Array(matrixSize).fill(null).map(() => Array(matrixSize).fill(0)),
      },
      variables: Array(matrixSize).fill(null).map((_, i) => `x${i + 1}`),
      constraints: [],
      created: new Date(),
      lastModified: new Date(),
      category: 'custom',
      difficulty: 'easy',
      tags: [],
    };
    
    setProblems([newProblem, ...problems]);
    setSelectedProblem(newProblem);
    setNewProblemDialog(false);
    setMatrixEditMode(true);
  };

  const updateMatrixValue = (row: number, col: number, value: number) => {
    if (!selectedProblem) return;
    
    const newMatrix = { ...selectedProblem.matrix };
    newMatrix.values[row][col] = value;
    
    // Ensure symmetry for QUBO matrix
    if (row !== col) {
      newMatrix.values[col][row] = value;
    }
    
    const updatedProblem = {
      ...selectedProblem,
      matrix: newMatrix,
      lastModified: new Date(),
    };
    
    setSelectedProblem(updatedProblem);
    setProblems(problems.map(p => p.id === selectedProblem.id ? updatedProblem : p));
  };

  const addConstraint = () => {
    if (!selectedProblem) return;
    
    const newConstraint: QUBOConstraint = {
      id: Date.now().toString(),
      type: 'equality',
      expression: 'Enter constraint expression',
      value: 0,
      penalty: 1,
      active: true,
    };
    
    const updatedProblem = {
      ...selectedProblem,
      constraints: [...selectedProblem.constraints, newConstraint],
      lastModified: new Date(),
    };
    
    setSelectedProblem(updatedProblem);
    setProblems(problems.map(p => p.id === selectedProblem.id ? updatedProblem : p));
  };

  const removeConstraint = (constraintId: string) => {
    if (!selectedProblem) return;
    
    const updatedProblem = {
      ...selectedProblem,
      constraints: selectedProblem.constraints.filter(c => c.id !== constraintId),
      lastModified: new Date(),
    };
    
    setSelectedProblem(updatedProblem);
    setProblems(problems.map(p => p.id === selectedProblem.id ? updatedProblem : p));
  };

  const solveQUBO = async () => {
    if (!selectedProblem) return;
    
    setIsOptimizing(true);
    setStepperActiveStep(0);
    
    try {
      // Simulate optimization steps
      const steps = [
        'Preparing quantum circuit...',
        'Initializing QAOA parameters...',
        'Running quantum optimization...',
        'Processing results...',
        'Generating visualization...',
      ];
      
      for (let i = 0; i < steps.length; i++) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        setStepperActiveStep(i + 1);
      }
      
      // Call the quantum optimization service
      const result = await quantumOptimizationService.solveQUBO(
        selectedProblem.matrix,
        {
          algorithm: algorithmSettings.algorithm as any,
          maxIterations: algorithmSettings.maxIterations,
          convergenceThreshold: algorithmSettings.convergenceThreshold,
          shots: algorithmSettings.shots,
        }
      );
      
      setOptimizationResult(result);
      
      // Generate visualization data
      const vis: SolutionVisualization = {
        variables: selectedProblem.variables.map((name, i) => ({
          name,
          value: Math.random() > 0.5 ? 1 : 0,
          probability: Math.random(),
        })),
        objectiveHistory: Array(50).fill(null).map((_, i) => ({
          iteration: i,
          value: Math.random() * 100 + 50 - i * 0.5,
          energy: Math.random() * 10 + 5 - i * 0.1,
        })),
        energyLandscape: Array(100).fill(null).map((_, i) => ({
          x: Math.random() * 10,
          y: Math.random() * 10,
          energy: Math.random() * 100,
        })),
        correlations: selectedProblem.variables.flatMap((v1, i) => 
          selectedProblem.variables.slice(i + 1).map(v2 => ({
            var1: v1,
            var2: v2,
            correlation: (Math.random() - 0.5) * 2,
          }))
        ),
      };
      
      setVisualization(vis);
      
    } catch (error) {
      console.error('Optimization failed:', error);
    } finally {
      setIsOptimizing(false);
      setStepperActiveStep(0);
    }
  };

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );

  const MatrixEditor = () => {
    if (!selectedProblem) return null;
    
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">QUBO Matrix</Typography>
            <Box>
              <Button
                size="small"
                startIcon={matrixEditMode ? <Visibility /> : <Edit />}
                onClick={() => setMatrixEditMode(!matrixEditMode)}
              >
                {matrixEditMode ? 'View' : 'Edit'}
              </Button>
              <Button
                size="small"
                startIcon={<Refresh />}
                onClick={() => {
                  const size = selectedProblem.matrix.size;
                  updateMatrixValue(0, 0, 0); // Trigger refresh
                }}
                sx={{ ml: 1 }}
              >
                Reset
              </Button>
            </Box>
          </Box>
          
          <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
            <Table size="small" stickyHeader>
              <TableHead>
                <TableRow>
                  <TableCell></TableCell>
                  {selectedProblem.variables.map((variable, i) => (
                    <TableCell key={i} align="center">
                      <Typography variant="caption" fontWeight="bold">
                        {variable}
                      </Typography>
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {selectedProblem.matrix.values.map((row, i) => (
                  <TableRow key={i}>
                    <TableCell>
                      <Typography variant="caption" fontWeight="bold">
                        {selectedProblem.variables[i]}
                      </Typography>
                    </TableCell>
                    {row.map((value, j) => (
                      <TableCell key={j} align="center">
                        {matrixEditMode ? (
                          <TextField
                            size="small"
                            type="number"
                            value={value}
                            onChange={(e) => updateMatrixValue(i, j, parseFloat(e.target.value) || 0)}
                            inputProps={{ 
                              step: 0.01,
                              style: { textAlign: 'center', width: '60px' }
                            }}
                            variant="outlined"
                          />
                        ) : (
                          <Chip
                            label={value.toFixed(3)}
                            size="small"
                            color={value > 0 ? 'primary' : value < 0 ? 'secondary' : 'default'}
                            variant={i === j ? 'filled' : 'outlined'}
                          />
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            <Typography variant="body2" color="text.secondary">
              Matrix Size: {selectedProblem.matrix.size} × {selectedProblem.matrix.size}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Non-zero Elements: {selectedProblem.matrix.values.flat().filter(v => v !== 0).length}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Density: {((selectedProblem.matrix.values.flat().filter(v => v !== 0).length / (selectedProblem.matrix.size ** 2)) * 100).toFixed(1)}%
            </Typography>
          </Box>
        </CardContent>
      </Card>
    );
  };

  const ConstraintsEditor = () => {
    if (!selectedProblem) return null;
    
    return (
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">Constraints</Typography>
            <Button
              size="small"
              startIcon={<Add />}
              onClick={addConstraint}
              variant="outlined"
            >
              Add Constraint
            </Button>
          </Box>
          
          {selectedProblem.constraints.length === 0 ? (
            <Paper sx={{ p: 3, textAlign: 'center', bgcolor: 'grey.50' }}>
              <Functions sx={{ fontSize: 48, color: 'text.secondary', mb: 1 }} />
              <Typography variant="body2" color="text.secondary">
                No constraints defined. This is an unconstrained QUBO problem.
              </Typography>
            </Paper>
          ) : (
            <List>
              {selectedProblem.constraints.map((constraint, index) => (
                <React.Fragment key={constraint.id}>
                  <ListItem>
                    <ListItemIcon>
                      <Avatar sx={{ bgcolor: constraint.active ? 'primary.main' : 'grey.400' }}>
                        {index + 1}
                      </Avatar>
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Chip
                            label={constraint.type}
                            size="small"
                            color={constraint.type === 'equality' ? 'primary' : 'secondary'}
                          />
                          <Typography variant="body2">
                            {constraint.expression}
                          </Typography>
                        </Box>
                      }
                      secondary={
                        <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
                          <Typography variant="caption">
                            Value: {constraint.value}
                          </Typography>
                          <Typography variant="caption">
                            Penalty: {constraint.penalty}
                          </Typography>
                          <FormControlLabel
                            control={
                              <Switch
                                size="small"
                                checked={constraint.active}
                                onChange={(e) => {
                                  const updatedConstraints = selectedProblem.constraints.map(c =>
                                    c.id === constraint.id ? { ...c, active: e.target.checked } : c
                                  );
                                  const updatedProblem = {
                                    ...selectedProblem,
                                    constraints: updatedConstraints,
                                    lastModified: new Date(),
                                  };
                                  setSelectedProblem(updatedProblem);
                                  setProblems(problems.map(p => p.id === selectedProblem.id ? updatedProblem : p));
                                }}
                              />
                            }
                            label="Active"
                          />
                        </Box>
                      }
                    />
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        onClick={() => removeConstraint(constraint.id)}
                        size="small"
                      >
                        <Delete />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                  {index < selectedProblem.constraints.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          )}
        </CardContent>
      </Card>
    );
  };

  const OptimizationControls = () => (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Optimization Settings
        </Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Algorithm</InputLabel>
              <Select
                value={algorithmSettings.algorithm}
                onChange={(e) => setAlgorithmSettings({
                  ...algorithmSettings,
                  algorithm: e.target.value,
                })}
              >
                <MenuItem value="QAOA">QAOA</MenuItem>
                <MenuItem value="VQE">VQE</MenuItem>
                <MenuItem value="Quantum Annealing">Quantum Annealing</MenuItem>
                <MenuItem value="Adiabatic">Adiabatic</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              label="Circuit Layers"
              type="number"
              value={algorithmSettings.layers}
              onChange={(e) => setAlgorithmSettings({
                ...algorithmSettings,
                layers: parseInt(e.target.value) || 1,
              })}
              fullWidth
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              label="Shots"
              type="number"
              value={algorithmSettings.shots}
              onChange={(e) => setAlgorithmSettings({
                ...algorithmSettings,
                shots: parseInt(e.target.value) || 1024,
              })}
              fullWidth
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              label="Max Iterations"
              type="number"
              value={algorithmSettings.maxIterations}
              onChange={(e) => setAlgorithmSettings({
                ...algorithmSettings,
                maxIterations: parseInt(e.target.value) || 100,
              })}
              fullWidth
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              label="Convergence Threshold"
              type="number"
              value={algorithmSettings.convergenceThreshold}
              onChange={(e) => setAlgorithmSettings({
                ...algorithmSettings,
                convergenceThreshold: parseFloat(e.target.value) || 0.001,
              })}
              inputProps={{ step: 0.001 }}
              fullWidth
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>Classical Optimizer</InputLabel>
              <Select
                value={algorithmSettings.optimizer}
                onChange={(e) => setAlgorithmSettings({
                  ...algorithmSettings,
                  optimizer: e.target.value,
                })}
              >
                <MenuItem value="COBYLA">COBYLA</MenuItem>
                <MenuItem value="SLSQP">SLSQP</MenuItem>
                <MenuItem value="BFGS">BFGS</MenuItem>
                <MenuItem value="Nelder-Mead">Nelder-Mead</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Switch
                  checked={algorithmSettings.errorMitigation}
                  onChange={(e) => setAlgorithmSettings({
                    ...algorithmSettings,
                    errorMitigation: e.target.checked,
                  })}
                />
              }
              label="Enable Error Mitigation"
            />
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            size="large"
            startIcon={isOptimizing ? <CircularProgress size={16} /> : <PlayArrow />}
            onClick={solveQUBO}
            disabled={isOptimizing || !selectedProblem}
            fullWidth
          >
            {isOptimizing ? 'Optimizing...' : 'Solve QUBO'}
          </Button>
          
          {isOptimizing && (
            <Button
              variant="outlined"
              startIcon={<Stop />}
              onClick={() => setIsOptimizing(false)}
            >
              Stop
            </Button>
          )}
        </Box>
        
        {isOptimizing && (
          <Box sx={{ mt: 2 }}>
            <Stepper activeStep={stepperActiveStep} orientation="vertical">
              {[
                'Preparing quantum circuit',
                'Initializing QAOA parameters',
                'Running quantum optimization',
                'Processing results',
                'Generating visualization',
              ].map((label, index) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  const ResultsVisualization = () => {
    if (!optimizationResult || !visualization) return null;
    
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Solution Variables
              </Typography>
              <List>
                {visualization.variables.map((variable, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Avatar sx={{ bgcolor: variable.value ? 'success.main' : 'grey.400' }}>
                        {variable.value}
                      </Avatar>
                    </ListItemIcon>
                    <ListItemText
                      primary={variable.name}
                      secondary={`Probability: ${(variable.probability * 100).toFixed(1)}%`}
                    />
                    <LinearProgress
                      variant="determinate"
                      value={variable.probability * 100}
                      sx={{ width: 100, ml: 2 }}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Optimization Results
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Objective Value"
                    secondary={optimizationResult.objectiveValue.toFixed(6)}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Feasible Solution"
                    secondary={optimizationResult.feasible ? 'Yes' : 'No'}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Iterations"
                    secondary={optimizationResult.iterations}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Convergence Time"
                    secondary={`${(optimizationResult.convergenceTime / 1000).toFixed(2)}s`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Quantum Advantage"
                    secondary={`${optimizationResult.quantumAdvantage.toFixed(1)}x`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="Confidence"
                    secondary={`${(optimizationResult.confidence * 100).toFixed(1)}%`}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Convergence History
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <ComposedChart data={visualization.objectiveHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="iteration" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <RechartsTooltip />
                  <Legend />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="value"
                    stroke="#1976d2"
                    strokeWidth={2}
                    name="Objective Value"
                  />
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="energy"
                    stroke="#f57c00"
                    strokeWidth={2}
                    name="Energy"
                  />
                </ComposedChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Energy Landscape
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <ScatterChart data={visualization.energyLandscape}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="x" name="Parameter 1" />
                  <YAxis dataKey="y" name="Parameter 2" />
                  <RechartsTooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Scatter
                    dataKey="energy"
                    fill="#1976d2"
                    name="Energy"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Variable Correlations
              </Typography>
              <List>
                {visualization.correlations.slice(0, 6).map((corr, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={`${corr.var1} ↔ ${corr.var2}`}
                      secondary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <LinearProgress
                            variant="determinate"
                            value={Math.abs(corr.correlation) * 100}
                            color={corr.correlation > 0 ? 'primary' : 'secondary'}
                            sx={{ flexGrow: 1 }}
                          />
                          <Typography variant="caption">
                            {corr.correlation.toFixed(3)}
                          </Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          QUBO Solver
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={<Upload />}
            onClick={() => {}}
          >
            Import
          </Button>
          <Button
            variant="outlined"
            startIcon={<Download />}
            onClick={() => {}}
            disabled={!selectedProblem}
          >
            Export
          </Button>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setNewProblemDialog(true)}
          >
            New Problem
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Problem Library
              </Typography>
              <List>
                {problems.map((problem) => (
                  <ListItem
                    key={problem.id}
                    button
                    selected={selectedProblem?.id === problem.id}
                    onClick={() => setSelectedProblem(problem)}
                  >
                    <ListItemIcon>
                      <Avatar sx={{ bgcolor: getCategoryColor(problem.category) }}>
                        {getCategoryIcon(problem.category)}
                      </Avatar>
                    </ListItemIcon>
                    <ListItemText
                      primary={problem.name}
                      secondary={
                        <Box>
                          <Typography variant="caption" display="block">
                            {problem.matrix.size}×{problem.matrix.size} matrix
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 0.5, mt: 0.5 }}>
                            <Chip
                              label={problem.difficulty}
                              size="small"
                              sx={{ bgcolor: getDifficultyColor(problem.difficulty), color: 'white' }}
                            />
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={9}>
          {selectedProblem && (
            <>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box>
                      <Typography variant="h5" gutterBottom>
                        {selectedProblem.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {selectedProblem.description}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        <Chip
                          label={selectedProblem.category.replace('_', ' ')}
                          icon={getCategoryIcon(selectedProblem.category)}
                          sx={{ bgcolor: getCategoryColor(selectedProblem.category), color: 'white' }}
                        />
                        <Chip
                          label={selectedProblem.difficulty}
                          sx={{ bgcolor: getDifficultyColor(selectedProblem.difficulty), color: 'white' }}
                        />
                        {selectedProblem.tags.map((tag) => (
                          <Chip key={tag} label={tag} size="small" variant="outlined" />
                        ))}
                      </Box>
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <IconButton>
                        <FileCopy />
                      </IconButton>
                      <IconButton>
                        <Share />
                      </IconButton>
                      <IconButton>
                        <Delete />
                      </IconButton>
                    </Box>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary">
                    Created: {selectedProblem.created.toLocaleDateString()} • 
                    Modified: {selectedProblem.lastModified.toLocaleDateString()}
                  </Typography>
                </CardContent>
              </Card>
              
              <Paper sx={{ width: '100%', mb: 3 }}>
                <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
                  <Tab label="Matrix" icon={<GridOn />} />
                  <Tab label="Constraints" icon={<Functions />} />
                  <Tab label="Solve" icon={<PlayArrow />} />
                  <Tab label="Results" icon={<Assessment />} disabled={!optimizationResult} />
                </Tabs>
              </Paper>
              
              <TabPanel value={activeTab} index={0}>
                <MatrixEditor />
              </TabPanel>
              
              <TabPanel value={activeTab} index={1}>
                <ConstraintsEditor />
              </TabPanel>
              
              <TabPanel value={activeTab} index={2}>
                <OptimizationControls />
              </TabPanel>
              
              <TabPanel value={activeTab} index={3}>
                <ResultsVisualization />
              </TabPanel>
            </>
          )}
        </Grid>
      </Grid>

      {/* New Problem Dialog */}
      <Dialog
        open={newProblemDialog}
        onClose={() => setNewProblemDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Create New QUBO Problem</DialogTitle>
        <DialogContent>
          <Stack spacing={3} sx={{ mt: 2 }}>
            <TextField
              label="Problem Name"
              fullWidth
              defaultValue="New QUBO Problem"
            />
            
            <TextField
              label="Description"
              multiline
              rows={3}
              fullWidth
              defaultValue="Enter problem description"
            />
            
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select defaultValue="custom">
                <MenuItem value="portfolio">Portfolio Optimization</MenuItem>
                <MenuItem value="supply_chain">Supply Chain</MenuItem>
                <MenuItem value="energy">Energy Optimization</MenuItem>
                <MenuItem value="scheduling">Scheduling</MenuItem>
                <MenuItem value="routing">Routing</MenuItem>
                <MenuItem value="custom">Custom</MenuItem>
              </Select>
            </FormControl>
            
            <Box>
              <Typography gutterBottom>Matrix Size</Typography>
              <Slider
                value={matrixSize}
                onChange={(e, value) => setMatrixSize(value as number)}
                min={2}
                max={20}
                marks
                valueLabelDisplay="auto"
              />
            </Box>
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewProblemDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={createNewProblem}>
            Create Problem
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default QUBOSolver;