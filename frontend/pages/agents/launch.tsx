import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import Head from 'next/head';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Box,
  Button,
  Card,
  CardContent,
  CardHeader,
  Chip,
  CircularProgress,
  Container,
  Dialog,
  DialogContent,
  DialogTitle,
  Divider,
  Grid,
  IconButton,
  LinearProgress,
  Paper,
  Stack,
  TextField,
  Typography,
  Alert,
  Tooltip,
  Badge,
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  Settings,
  Timeline,
  Psychology,
  Speed,
  Security,
  CloudQueue,
  Refresh,
  Info,
  CheckCircle,
  Error,
  Warning,
} from '@mui/icons-material';

// Types
interface QuantumJob {
  id: string;
  type: 'parallel_exploration' | 'reversal_reasoning' | 'quantum_ranking' | 'lead_qualification';
  status: 'pending' | 'running' | 'completed' | 'failed';
  progress: number;
  result?: any;
  error?: string;
  createdAt: Date;
  completedAt?: Date;
}

interface AgentConfig {
  agentId: string;
  name: string;
  role: 'sales' | 'support' | 'analyst';
  quantumEnabled: boolean;
  riskThreshold: number;
  maxConcurrentJobs: number;
}

interface LaunchMetrics {
  totalJobs: number;
  completedJobs: number;
  failedJobs: number;
  averageResponseTime: number;
  quantumEnhancementRate: number;
  uptime: number;
}

const QuantumAgentLaunch: NextPage = () => {
  // State management
  const [agentConfig, setAgentConfig] = useState<AgentConfig>({
    agentId: '',
    name: 'Quantum Sales Agent',
    role: 'sales',
    quantumEnabled: true,
    riskThreshold: 0.7,
    maxConcurrentJobs: 5,
  });
  
  const [isLaunched, setIsLaunched] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [jobs, setJobs] = useState<QuantumJob[]>([]);
  const [metrics, setMetrics] = useState<LaunchMetrics>({
    totalJobs: 0,
    completedJobs: 0,
    failedJobs: 0,
    averageResponseTime: 0,
    quantumEnhancementRate: 0,
    uptime: 0,
  });
  
  const [selectedJob, setSelectedJob] = useState<QuantumJob | null>(null);
  const [showConfig, setShowConfig] = useState(false);
  const [healthStatus, setHealthStatus] = useState<'healthy' | 'degraded' | 'unhealthy'>('healthy');
  const [countdown, setCountdown] = useState<number | null>(null);

  // Quantum High Council countdown
  useEffect(() => {
    const fetchCountdown = async () => {
      try {
        const response = await fetch('/api/launch/countdown');
        const data = await response.json();
        setCountdown(data.secondsRemaining);
      } catch (error) {
        console.error('Failed to fetch countdown:', error);
      }
    };

    fetchCountdown();
    const interval = setInterval(fetchCountdown, 1000);
    return () => clearInterval(interval);
  }, []);

  // Health check polling
  useEffect(() => {
    if (isLaunched) {
      const healthCheck = async () => {
        try {
          const response = await fetch('/api/agents/health');
          const data = await response.json();
          setHealthStatus(data.status);
          setMetrics(data.metrics);
        } catch (error) {
          setHealthStatus('unhealthy');
        }
      };

      const interval = setInterval(healthCheck, 5000);
      return () => clearInterval(interval);
    }
  }, [isLaunched]);

  // Launch agent
  const handleLaunch = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/agents/launch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(agentConfig),
      });
      
      if (response.ok) {
        const data = await response.json();
        setAgentConfig(prev => ({ ...prev, agentId: data.agentId }));
        setIsLaunched(true);
      } else {
        throw new Error('Failed to launch agent');
      }
    } catch (error) {
      console.error('Launch failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Stop agent
  const handleStop = async () => {
    setIsLoading(true);
    try {
      await fetch(`/api/agents/${agentConfig.agentId}/stop`, {
        method: 'POST',
      });
      setIsLaunched(false);
      setJobs([]);
    } catch (error) {
      console.error('Stop failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Submit test job
  const handleTestJob = async (jobType: QuantumJob['type']) => {
    try {
      const response = await fetch('/api/agents/demo-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: jobType,
          agentId: agentConfig.agentId,
          testData: getTestData(jobType),
        }),
      });
      
      if (response.ok) {
        const job = await response.json();
        setJobs(prev => [job, ...prev]);
      }
    } catch (error) {
      console.error('Test job failed:', error);
    }
  };

  const getTestData = (jobType: QuantumJob['type']) => {
    switch (jobType) {
      case 'parallel_exploration':
        return {
          lead_profile: { name: 'John Smith', company: 'TechCorp', title: 'VP Engineering' },
          objective: 'schedule_demo',
        };
      case 'reversal_reasoning':
        return {
          outcome: 'Sales forecast dropped 15%',
          context: { timeline: 'Q4 2024', metrics: { conversion_rate: 0.12 } },
        };
      case 'quantum_ranking':
        return {
          candidates: [
            { id: '1', name: 'Lead A', attributes: { fit_score: 85 } },
            { id: '2', name: 'Lead B', attributes: { fit_score: 92 } },
          ],
          optimization_goal: 'maximize_conversion',
        };
      case 'lead_qualification':
        return {
          lead_data: {
            contact_info: { name: 'Jane Doe', company: 'StartupCo' },
            company_info: { industry: 'SaaS', size: '50-100' },
          },
        };
      default:
        return {};
    }
  };

  const formatCountdown = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${days}d ${hours}h ${minutes}m ${secs}s`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy': return 'success';
      case 'degraded': return 'warning';
      case 'unhealthy': return 'error';
      default: return 'default';
    }
  };

  const getJobStatusIcon = (status: QuantumJob['status']) => {
    switch (status) {
      case 'completed': return <CheckCircle color="success" />;
      case 'failed': return <Error color="error" />;
      case 'running': return <CircularProgress size={20} />;
      default: return <Warning color="warning" />;
    }
  };

  return (
    <>
      <Head>
        <title>Quantum Agent Launch | FLYFOX AI</title>
        <meta name="description" content="Launch and manage quantum-enhanced AI agents" />
      </Head>

      <Container maxWidth="xl" sx={{ py: 4 }}>
        {/* Header */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom>
            🚀 Quantum Agent Launch
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Deploy quantum-enhanced AI agents with Dynex optimization
          </Typography>
        </Box>

        {/* Quantum High Council Countdown */}
        {countdown !== null && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Alert
              severity="info"
              icon={<CloudQueue />}
              sx={{ mb: 3, background: 'linear-gradient(45deg, #1e3a8a, #3b82f6)' }}
            >
              <Typography variant="h6" color="white">
                🎯 Quantum High Council Launch: {formatCountdown(countdown)}
              </Typography>
            </Alert>
          </motion.div>
        )}

        <Grid container spacing={3}>
          {/* Control Panel */}
          <Grid item xs={12} md={4}>
            <Card sx={{ height: 'fit-content' }}>
              <CardHeader
                title="Agent Control"
                action={
                  <IconButton onClick={() => setShowConfig(true)}>
                    <Settings />
                  </IconButton>
                }
              />
              <CardContent>
                <Stack spacing={2}>
                  <Box>
                    <Typography variant="subtitle2" gutterBottom>
                      Agent Status
                    </Typography>
                    <Chip
                      label={isLaunched ? 'Active' : 'Inactive'}
                      color={isLaunched ? 'success' : 'default'}
                      icon={isLaunched ? <CheckCircle /> : <Stop />}
                    />
                    {isLaunched && (
                      <Chip
                        label={healthStatus}
                        color={getStatusColor(healthStatus) as any}
                        size="small"
                        sx={{ ml: 1 }}
                      />
                    )}
                  </Box>

                  <TextField
                    label="Agent Name"
                    value={agentConfig.name}
                    onChange={(e) => setAgentConfig(prev => ({ ...prev, name: e.target.value }))}
                    disabled={isLaunched}
                    size="small"
                  />

                  <Box>
                    <Typography variant="subtitle2" gutterBottom>
                      Quantum Features
                    </Typography>
                    <Stack direction="row" spacing={1} flexWrap="wrap">
                      <Chip
                        icon={<Psychology />}
                        label="Parallel Exploration"
                        color={agentConfig.quantumEnabled ? 'primary' : 'default'}
                        size="small"
                      />
                      <Chip
                        icon={<Timeline />}
                        label="Reversal Reasoning"
                        color={agentConfig.quantumEnabled ? 'primary' : 'default'}
                        size="small"
                      />
                      <Chip
                        icon={<Speed />}
                        label="Quantum Ranking"
                        color={agentConfig.quantumEnabled ? 'primary' : 'default'}
                        size="small"
                      />
                    </Stack>
                  </Box>

                  <Button
                    variant="contained"
                    size="large"
                    onClick={isLaunched ? handleStop : handleLaunch}
                    disabled={isLoading}
                    startIcon={isLaunched ? <Stop /> : <PlayArrow />}
                    sx={{
                      background: isLaunched
                        ? 'linear-gradient(45deg, #dc2626, #ef4444)'
                        : 'linear-gradient(45deg, #059669, #10b981)',
                      '&:hover': {
                        background: isLaunched
                          ? 'linear-gradient(45deg, #b91c1c, #dc2626)'
                          : 'linear-gradient(45deg, #047857, #059669)',
                      },
                    }}
                  >
                    {isLoading ? (
                      <CircularProgress size={20} color="inherit" />
                    ) : isLaunched ? (
                      'Stop Agent'
                    ) : (
                      'Launch Agent'
                    )}
                  </Button>
                </Stack>
              </CardContent>
            </Card>

            {/* Test Jobs */}
            {isLaunched && (
              <Card sx={{ mt: 2 }}>
                <CardHeader title="Test Quantum Jobs" />
                <CardContent>
                  <Stack spacing={1}>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => handleTestJob('parallel_exploration')}
                      startIcon={<Psychology />}
                    >
                      Parallel Exploration
                    </Button>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => handleTestJob('reversal_reasoning')}
                      startIcon={<Timeline />}
                    >
                      Reversal Reasoning
                    </Button>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => handleTestJob('quantum_ranking')}
                      startIcon={<Speed />}
                    >
                      Quantum Ranking
                    </Button>
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => handleTestJob('lead_qualification')}
                      startIcon={<Security />}
                    >
                      Lead Qualification
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            )}
          </Grid>

          {/* Metrics Dashboard */}
          <Grid item xs={12} md={8}>
            {isLaunched ? (
              <Grid container spacing={2}>
                {/* Metrics Cards */}
                <Grid item xs={6} sm={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="primary">
                      {metrics.totalJobs}
                    </Typography>
                    <Typography variant="caption">Total Jobs</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="success.main">
                      {metrics.completedJobs}
                    </Typography>
                    <Typography variant="caption">Completed</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="warning.main">
                      {metrics.averageResponseTime.toFixed(1)}s
                    </Typography>
                    <Typography variant="caption">Avg Response</Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6} sm={3}>
                  <Paper sx={{ p: 2, textAlign: 'center' }}>
                    <Typography variant="h4" color="info.main">
                      {(metrics.quantumEnhancementRate * 100).toFixed(0)}%
                    </Typography>
                    <Typography variant="caption">Quantum Enhanced</Typography>
                  </Paper>
                </Grid>

                {/* Job History */}
                <Grid item xs={12}>
                  <Card>
                    <CardHeader
                      title="Job History"
                      action={
                        <IconButton onClick={() => window.location.reload()}>
                          <Refresh />
                        </IconButton>
                      }
                    />
                    <CardContent>
                      {jobs.length === 0 ? (
                        <Typography color="text.secondary" textAlign="center">
                          No jobs yet. Try running a test job!
                        </Typography>
                      ) : (
                        <Stack spacing={1}>
                          {jobs.map((job) => (
                            <Paper
                              key={job.id}
                              sx={{ p: 2, cursor: 'pointer' }}
                              onClick={() => setSelectedJob(job)}
                            >
                              <Box display="flex" alignItems="center" justifyContent="space-between">
                                <Box display="flex" alignItems="center" gap={1}>
                                  {getJobStatusIcon(job.status)}
                                  <Typography variant="subtitle2">
                                    {job.type.replace('_', ' ').toUpperCase()}
                                  </Typography>
                                  <Chip label={job.status} size="small" />
                                </Box>
                                <Typography variant="caption" color="text.secondary">
                                  {job.createdAt.toLocaleTimeString()}
                                </Typography>
                              </Box>
                              {job.status === 'running' && (
                                <LinearProgress
                                  variant="determinate"
                                  value={job.progress}
                                  sx={{ mt: 1 }}
                                />
                              )}
                            </Paper>
                          ))}
                        </Stack>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            ) : (
              <Card sx={{ height: 400, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Box textAlign="center">
                  <CloudQueue sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h5" color="text.secondary" gutterBottom>
                    Agent Not Launched
                  </Typography>
                  <Typography color="text.secondary">
                    Launch your quantum agent to see metrics and job history
                  </Typography>
                </Box>
              </Card>
            )}
          </Grid>
        </Grid>

        {/* Configuration Dialog */}
        <Dialog open={showConfig} onClose={() => setShowConfig(false)} maxWidth="sm" fullWidth>
          <DialogTitle>Agent Configuration</DialogTitle>
          <DialogContent>
            <Stack spacing={2} sx={{ mt: 1 }}>
              <TextField
                label="Agent Name"
                value={agentConfig.name}
                onChange={(e) => setAgentConfig(prev => ({ ...prev, name: e.target.value }))}
                fullWidth
              />
              <TextField
                label="Risk Threshold"
                type="number"
                value={agentConfig.riskThreshold}
                onChange={(e) => setAgentConfig(prev => ({ ...prev, riskThreshold: parseFloat(e.target.value) }))}
                inputProps={{ min: 0, max: 1, step: 0.1 }}
                fullWidth
              />
              <TextField
                label="Max Concurrent Jobs"
                type="number"
                value={agentConfig.maxConcurrentJobs}
                onChange={(e) => setAgentConfig(prev => ({ ...prev, maxConcurrentJobs: parseInt(e.target.value) }))}
                inputProps={{ min: 1, max: 20 }}
                fullWidth
              />
            </Stack>
          </DialogContent>
        </Dialog>

        {/* Job Details Dialog */}
        <Dialog
          open={!!selectedJob}
          onClose={() => setSelectedJob(null)}
          maxWidth="md"
          fullWidth
        >
          {selectedJob && (
            <>
              <DialogTitle>
                Job Details: {selectedJob.type.replace('_', ' ').toUpperCase()}
              </DialogTitle>
              <DialogContent>
                <Stack spacing={2}>
                  <Box>
                    <Typography variant="subtitle2">Status</Typography>
                    <Chip label={selectedJob.status} color={selectedJob.status === 'completed' ? 'success' : 'default'} />
                  </Box>
                  <Box>
                    <Typography variant="subtitle2">Progress</Typography>
                    <LinearProgress variant="determinate" value={selectedJob.progress} />
                  </Box>
                  {selectedJob.result && (
                    <Box>
                      <Typography variant="subtitle2">Result</Typography>
                      <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                        <pre style={{ fontSize: '0.875rem', overflow: 'auto' }}>
                          {JSON.stringify(selectedJob.result, null, 2)}
                        </pre>
                      </Paper>
                    </Box>
                  )}
                  {selectedJob.error && (
                    <Alert severity="error">
                      <Typography variant="subtitle2">Error</Typography>
                      <Typography variant="body2">{selectedJob.error}</Typography>
                    </Alert>
                  )}
                </Stack>
              </DialogContent>
            </>
          )}
        </Dialog>
      </Container>
    </>
  );
};

export default QuantumAgentLaunch;