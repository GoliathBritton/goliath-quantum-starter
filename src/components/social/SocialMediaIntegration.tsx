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
} from '@mui/material';
import {
  Add,
  Refresh,
  Settings,
  Analytics,
  Campaign,
  Schedule,
  Psychology,
  TrendingUp,
  TrendingDown,
  Visibility,
  ThumbUp,
  Comment,
  Share,
  People,
  AttachMoney,
  Speed,
  CheckCircle,
  Warning,
  Error,
  Link,
  LinkOff,
  Sync,
  SyncDisabled,
  Instagram,
  Facebook,
  Twitter,
  LinkedIn,
  YouTube,
  TikTok,
  ExpandMore,
  Dashboard,
  ContentCopy,
  AutoAwesome,
  Notifications,
  NotificationsOff,
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
} from 'recharts';
import SocialMediaDashboard from './SocialMediaDashboard';
import ContentScheduler from './ContentScheduler';
import SocialAnalytics from './SocialAnalytics';
import CampaignManager from './CampaignManager';
import socialMediaService, { SocialAccount, Post } from '../../services/socialMediaService';

interface PlatformConnection {
  id: string;
  platform: string;
  accountName: string;
  accountId: string;
  isConnected: boolean;
  lastSync: Date;
  status: 'active' | 'error' | 'pending' | 'disconnected';
  permissions: string[];
  metrics: {
    followers: number;
    posts: number;
    engagement: number;
    reach: number;
  };
  settings: {
    autoPost: boolean;
    notifications: boolean;
    quantumOptimization: boolean;
  };
}

interface QuickAction {
  id: string;
  title: string;
  description: string;
  icon: React.ElementType;
  color: string;
  action: () => void;
  disabled?: boolean;
}

const SocialMediaIntegration: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [connectDialogOpen, setConnectDialogOpen] = useState(false);
  const [selectedPlatform, setSelectedPlatform] = useState('');
  const [isConnecting, setIsConnecting] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const [connections, setConnections] = useState<PlatformConnection[]>([
    {
      id: '1',
      platform: 'instagram',
      accountName: '@quantumtech_ai',
      accountId: 'inst_12345',
      isConnected: true,
      lastSync: new Date(Date.now() - 5 * 60 * 1000),
      status: 'active',
      permissions: ['read', 'write', 'analytics'],
      metrics: {
        followers: 18500,
        posts: 245,
        engagement: 4.2,
        reach: 125000,
      },
      settings: {
        autoPost: true,
        notifications: true,
        quantumOptimization: true,
      },
    },
    {
      id: '2',
      platform: 'twitter',
      accountName: '@QuantumTechAI',
      accountId: 'tw_67890',
      isConnected: true,
      lastSync: new Date(Date.now() - 2 * 60 * 1000),
      status: 'active',
      permissions: ['read', 'write', 'analytics'],
      metrics: {
        followers: 12300,
        posts: 892,
        engagement: 3.8,
        reach: 85000,
      },
      settings: {
        autoPost: true,
        notifications: true,
        quantumOptimization: true,
      },
    },
    {
      id: '3',
      platform: 'linkedin',
      accountName: 'Quantum Technologies Inc.',
      accountId: 'li_54321',
      isConnected: true,
      lastSync: new Date(Date.now() - 10 * 60 * 1000),
      status: 'active',
      permissions: ['read', 'write', 'analytics'],
      metrics: {
        followers: 5600,
        posts: 156,
        engagement: 6.1,
        reach: 35000,
      },
      settings: {
        autoPost: false,
        notifications: true,
        quantumOptimization: true,
      },
    },
    {
      id: '4',
      platform: 'facebook',
      accountName: 'Quantum Tech AI',
      accountId: 'fb_98765',
      isConnected: false,
      lastSync: new Date(Date.now() - 24 * 60 * 60 * 1000),
      status: 'disconnected',
      permissions: [],
      metrics: {
        followers: 0,
        posts: 0,
        engagement: 0,
        reach: 0,
      },
      settings: {
        autoPost: false,
        notifications: false,
        quantumOptimization: false,
      },
    },
    {
      id: '5',
      platform: 'youtube',
      accountName: 'Quantum Tech Channel',
      accountId: 'yt_13579',
      isConnected: false,
      lastSync: new Date(0),
      status: 'disconnected',
      permissions: [],
      metrics: {
        followers: 0,
        posts: 0,
        engagement: 0,
        reach: 0,
      },
      settings: {
        autoPost: false,
        notifications: false,
        quantumOptimization: false,
      },
    },
    {
      id: '6',
      platform: 'tiktok',
      accountName: '@quantumtech',
      accountId: 'tt_24680',
      isConnected: false,
      lastSync: new Date(0),
      status: 'disconnected',
      permissions: [],
      metrics: {
        followers: 0,
        posts: 0,
        engagement: 0,
        reach: 0,
      },
      settings: {
        autoPost: false,
        notifications: false,
        quantumOptimization: false,
      },
    },
  ]);

  const platforms = [
    { id: 'instagram', name: 'Instagram', icon: Instagram, color: '#E4405F' },
    { id: 'facebook', name: 'Facebook', icon: Facebook, color: '#1877F2' },
    { id: 'twitter', name: 'Twitter', icon: Twitter, color: '#1DA1F2' },
    { id: 'linkedin', name: 'LinkedIn', icon: LinkedIn, color: '#0A66C2' },
    { id: 'youtube', name: 'YouTube', icon: YouTube, color: '#FF0000' },
    { id: 'tiktok', name: 'TikTok', icon: TikTok, color: '#000000' },
  ];

  const getPlatformIcon = (platformId: string) => {
    const platform = platforms.find(p => p.id === platformId);
    if (!platform) return null;
    const IconComponent = platform.icon;
    return <IconComponent sx={{ color: platform.color }} />;
  };

  const getPlatformColor = (platformId: string) => {
    const platform = platforms.find(p => p.id === platformId);
    return platform?.color || '#666666';
  };

  const getStatusColor = (status: PlatformConnection['status']) => {
    switch (status) {
      case 'active': return 'success';
      case 'error': return 'error';
      case 'pending': return 'warning';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: PlatformConnection['status']) => {
    switch (status) {
      case 'active': return <CheckCircle />;
      case 'error': return <Error />;
      case 'pending': return <Warning />;
      default: return <LinkOff />;
    }
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const handleConnectPlatform = async (platformId: string) => {
    setIsConnecting(true);
    try {
      // Simulate OAuth connection process
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setConnections(connections.map(conn => 
        conn.platform === platformId 
          ? { 
              ...conn, 
              isConnected: true, 
              status: 'active' as const,
              lastSync: new Date(),
              permissions: ['read', 'write', 'analytics'],
              metrics: {
                followers: Math.floor(Math.random() * 10000) + 1000,
                posts: Math.floor(Math.random() * 500) + 50,
                engagement: Math.random() * 5 + 1,
                reach: Math.floor(Math.random() * 50000) + 10000,
              }
            }
          : conn
      ));
      
      setConnectDialogOpen(false);
      setSelectedPlatform('');
    } catch (error) {
      console.error('Connection failed:', error);
    } finally {
      setIsConnecting(false);
    }
  };

  const handleDisconnectPlatform = (platformId: string) => {
    setConnections(connections.map(conn => 
      conn.platform === platformId 
        ? { 
            ...conn, 
            isConnected: false, 
            status: 'disconnected' as const,
            permissions: [],
            metrics: {
              followers: 0,
              posts: 0,
              engagement: 0,
              reach: 0,
            },
            settings: {
              autoPost: false,
              notifications: false,
              quantumOptimization: false,
            }
          }
        : conn
    ));
  };

  const handleRefreshAll = async () => {
    setRefreshing(true);
    try {
      // Simulate refresh process
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setConnections(connections.map(conn => 
        conn.isConnected 
          ? { ...conn, lastSync: new Date() }
          : conn
      ));
    } catch (error) {
      console.error('Refresh failed:', error);
    } finally {
      setRefreshing(false);
    }
  };

  const handleToggleSetting = (connectionId: string, setting: keyof PlatformConnection['settings']) => {
    setConnections(connections.map(conn => 
      conn.id === connectionId 
        ? { 
            ...conn, 
            settings: { 
              ...conn.settings, 
              [setting]: !conn.settings[setting] 
            }
          }
        : conn
    ));
  };

  const connectedPlatforms = connections.filter(c => c.isConnected);
  const totalFollowers = connectedPlatforms.reduce((sum, c) => sum + c.metrics.followers, 0);
  const totalPosts = connectedPlatforms.reduce((sum, c) => sum + c.metrics.posts, 0);
  const avgEngagement = connectedPlatforms.length > 0 
    ? connectedPlatforms.reduce((sum, c) => sum + c.metrics.engagement, 0) / connectedPlatforms.length 
    : 0;
  const totalReach = connectedPlatforms.reduce((sum, c) => sum + c.metrics.reach, 0);

  const quickActions: QuickAction[] = [
    {
      id: 'create_post',
      title: 'Create Post',
      description: 'Create and schedule a new post',
      icon: Add,
      color: '#1976d2',
      action: () => setActiveTab(1),
    },
    {
      id: 'view_analytics',
      title: 'View Analytics',
      description: 'Check performance metrics',
      icon: Analytics,
      color: '#388e3c',
      action: () => setActiveTab(2),
    },
    {
      id: 'manage_campaigns',
      title: 'Manage Campaigns',
      description: 'Create and manage campaigns',
      icon: Campaign,
      color: '#f57c00',
      action: () => setActiveTab(3),
    },
    {
      id: 'quantum_optimize',
      title: 'Quantum Optimize',
      description: 'AI-powered content optimization',
      icon: Psychology,
      color: '#7b1fa2',
      action: () => {
        // Trigger quantum optimization
        console.log('Quantum optimization triggered');
      },
    },
  ];

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box>{children}</Box>}
    </div>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Social Media Integration
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="outlined"
            startIcon={refreshing ? <CircularProgress size={16} /> : <Refresh />}
            onClick={handleRefreshAll}
            disabled={refreshing}
          >
            {refreshing ? 'Refreshing...' : 'Refresh All'}
          </Button>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setConnectDialogOpen(true)}
          >
            Connect Platform
          </Button>
        </Box>
      </Box>

      {/* Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Link color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Connected Platforms</Typography>
              </Box>
              <Typography variant="h4">{connectedPlatforms.length}</Typography>
              <Typography variant="body2" color="text.secondary">
                of {platforms.length} available
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <People color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Total Followers</Typography>
              </Box>
              <Typography variant="h4">{formatNumber(totalFollowers)}</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <TrendingUp color="success" fontSize="small" />
                <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                  +12.5% this month
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <ThumbUp color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Avg Engagement</Typography>
              </Box>
              <Typography variant="h4">{avgEngagement.toFixed(1)}%</Typography>
              <Typography variant="body2" color="text.secondary">
                {totalPosts} total posts
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Psychology color="primary" />
                <Typography variant="h6" sx={{ ml: 1 }}>Quantum Advantage</Typography>
              </Box>
              <Typography variant="h4" color="primary">410.7x</Typography>
              <Typography variant="body2" color="text.secondary">
                Faster optimization
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Quick Actions
          </Typography>
          <Grid container spacing={2}>
            {quickActions.map((action) => (
              <Grid item xs={12} sm={6} md={3} key={action.id}>
                <Paper
                  sx={{
                    p: 2,
                    cursor: 'pointer',
                    transition: 'all 0.2s',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: 3,
                    },
                  }}
                  onClick={action.action}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Avatar sx={{ bgcolor: action.color, mr: 2 }}>
                      <action.icon />
                    </Avatar>
                    <Typography variant="subtitle1">{action.title}</Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {action.description}
                  </Typography>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Platform Connections */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Platform Connections
          </Typography>
          <Grid container spacing={2}>
            {connections.map((connection) => (
              <Grid item xs={12} md={6} lg={4} key={connection.id}>
                <Card variant="outlined">
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Avatar sx={{ bgcolor: getPlatformColor(connection.platform), mr: 2 }}>
                          {getPlatformIcon(connection.platform)}
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle1">
                            {platforms.find(p => p.id === connection.platform)?.name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {connection.accountName}
                          </Typography>
                        </Box>
                      </Box>
                      <Chip
                        label={connection.status}
                        color={getStatusColor(connection.status)}
                        icon={getStatusIcon(connection.status)}
                        size="small"
                      />
                    </Box>
                    
                    {connection.isConnected && (
                      <>
                        <Grid container spacing={1} sx={{ mb: 2 }}>
                          <Grid item xs={6}>
                            <Typography variant="body2" color="text.secondary">Followers</Typography>
                            <Typography variant="h6">{formatNumber(connection.metrics.followers)}</Typography>
                          </Grid>
                          <Grid item xs={6}>
                            <Typography variant="body2" color="text.secondary">Engagement</Typography>
                            <Typography variant="h6">{connection.metrics.engagement.toFixed(1)}%</Typography>
                          </Grid>
                        </Grid>
                        
                        <Accordion>
                          <AccordionSummary expandIcon={<ExpandMore />}>
                            <Typography variant="body2">Settings</Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            <FormControlLabel
                              control={
                                <Switch
                                  checked={connection.settings.autoPost}
                                  onChange={() => handleToggleSetting(connection.id, 'autoPost')}
                                  size="small"
                                />
                              }
                              label="Auto-Post"
                            />
                            <FormControlLabel
                              control={
                                <Switch
                                  checked={connection.settings.notifications}
                                  onChange={() => handleToggleSetting(connection.id, 'notifications')}
                                  size="small"
                                />
                              }
                              label="Notifications"
                            />
                            <FormControlLabel
                              control={
                                <Switch
                                  checked={connection.settings.quantumOptimization}
                                  onChange={() => handleToggleSetting(connection.id, 'quantumOptimization')}
                                  size="small"
                                />
                              }
                              label="Quantum Optimization"
                            />
                          </AccordionDetails>
                        </Accordion>
                      </>
                    )}
                    
                    <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                      {connection.isConnected ? (
                        <>
                          <Button
                            size="small"
                            startIcon={<Sync />}
                            onClick={() => {
                              setConnections(connections.map(c => 
                                c.id === connection.id 
                                  ? { ...c, lastSync: new Date() }
                                  : c
                              ));
                            }}
                          >
                            Sync
                          </Button>
                          <Button
                            size="small"
                            color="error"
                            startIcon={<LinkOff />}
                            onClick={() => handleDisconnectPlatform(connection.platform)}
                          >
                            Disconnect
                          </Button>
                        </>
                      ) : (
                        <Button
                          size="small"
                          variant="contained"
                          startIcon={<Link />}
                          onClick={() => {
                            setSelectedPlatform(connection.platform);
                            setConnectDialogOpen(true);
                          }}
                        >
                          Connect
                        </Button>
                      )}
                    </Box>
                    
                    {connection.isConnected && (
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                        Last sync: {connection.lastSync.toLocaleTimeString()}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>

      {/* Main Content Tabs */}
      <Paper sx={{ width: '100%' }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Dashboard" icon={<Dashboard />} />
          <Tab label="Content Scheduler" icon={<Schedule />} />
          <Tab label="Analytics" icon={<Analytics />} />
          <Tab label="Campaign Manager" icon={<Campaign />} />
        </Tabs>
      </Paper>

      <TabPanel value={activeTab} index={0}>
        <SocialMediaDashboard />
      </TabPanel>

      <TabPanel value={activeTab} index={1}>
        <ContentScheduler />
      </TabPanel>

      <TabPanel value={activeTab} index={2}>
        <SocialAnalytics />
      </TabPanel>

      <TabPanel value={activeTab} index={3}>
        <CampaignManager />
      </TabPanel>

      {/* Connect Platform Dialog */}
      <Dialog
        open={connectDialogOpen}
        onClose={() => setConnectDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Connect Social Media Platform</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Select a platform to connect to your account. You'll be redirected to authorize the connection.
          </Typography>
          
          <FormControl fullWidth sx={{ mt: 2 }}>
            <InputLabel>Platform</InputLabel>
            <Select
              value={selectedPlatform}
              onChange={(e) => setSelectedPlatform(e.target.value)}
            >
              {platforms
                .filter(p => !connections.find(c => c.platform === p.id && c.isConnected))
                .map((platform) => (
                  <MenuItem key={platform.id} value={platform.id}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {getPlatformIcon(platform.id)}
                      <Typography sx={{ ml: 1 }}>{platform.name}</Typography>
                    </Box>
                  </MenuItem>
                ))
              }
            </Select>
          </FormControl>
          
          {selectedPlatform && (
            <Alert severity="info" sx={{ mt: 2 }}>
              <Typography variant="body2">
                You'll be redirected to {platforms.find(p => p.id === selectedPlatform)?.name} to authorize 
                access to your account. We'll only request the minimum permissions needed for posting and analytics.
              </Typography>
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConnectDialogOpen(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => handleConnectPlatform(selectedPlatform)}
            disabled={!selectedPlatform || isConnecting}
            startIcon={isConnecting ? <CircularProgress size={16} /> : <Link />}
          >
            {isConnecting ? 'Connecting...' : 'Connect'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SocialMediaIntegration;