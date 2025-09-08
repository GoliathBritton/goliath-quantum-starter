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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
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
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Slider,
} from '@mui/material';
import {
  Add,
  Edit,
  Delete,
  PlayArrow,
  Pause,
  Stop,
  Visibility,
  VisibilityOff,
  TrendingUp,
  TrendingDown,
  Campaign,
  Schedule,
  Psychology,
  Analytics,
  Target,
  AutoAwesome,
  Instagram,
  Facebook,
  Twitter,
  LinkedIn,
  YouTube,
  TikTok,
  CalendarToday,
  People,
  AttachMoney,
  Speed,
  ExpandMore,
  Settings,
  Refresh,
  Download,
  Share,
  Star,
  CheckCircle,
  Warning,
  Error,
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
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import socialMediaService from '../../services/socialMediaService';

interface Campaign {
  id: string;
  name: string;
  description: string;
  status: 'draft' | 'active' | 'paused' | 'completed' | 'scheduled';
  platforms: string[];
  startDate: Date;
  endDate: Date;
  budget: number;
  spent: number;
  objective: 'awareness' | 'engagement' | 'traffic' | 'conversions' | 'leads';
  targetAudience: {
    ageRange: [number, number];
    gender: string[];
    interests: string[];
    locations: string[];
  };
  content: {
    posts: CampaignPost[];
    templates: ContentTemplate[];
  };
  metrics: {
    reach: number;
    impressions: number;
    engagement: number;
    clicks: number;
    conversions: number;
    cost: number;
    roi: number;
  };
  quantumOptimization: {
    enabled: boolean;
    optimizationGoal: string;
    predictedPerformance: number;
    recommendations: string[];
  };
  automation: {
    autoPost: boolean;
    autoOptimize: boolean;
    autoScale: boolean;
    triggers: AutomationTrigger[];
  };
  createdAt: Date;
  updatedAt: Date;
}

interface CampaignPost {
  id: string;
  content: string;
  media: string[];
  platforms: string[];
  scheduledTime: Date;
  status: 'draft' | 'scheduled' | 'published' | 'failed';
  performance: {
    likes: number;
    comments: number;
    shares: number;
    views: number;
    clicks: number;
  };
}

interface ContentTemplate {
  id: string;
  name: string;
  category: string;
  content: string;
  variables: string[];
  platforms: string[];
  performance: number;
}

interface AutomationTrigger {
  id: string;
  name: string;
  condition: string;
  action: string;
  enabled: boolean;
}

const CampaignManager: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [campaigns, setCampaigns] = useState<Campaign[]>([
    {
      id: '1',
      name: 'Quantum AI Launch Campaign',
      description: 'Promote our revolutionary quantum AI platform to tech professionals',
      status: 'active',
      platforms: ['linkedin', 'twitter', 'facebook'],
      startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      endDate: new Date(Date.now() + 23 * 24 * 60 * 60 * 1000),
      budget: 10000,
      spent: 3250,
      objective: 'awareness',
      targetAudience: {
        ageRange: [25, 55],
        gender: ['male', 'female'],
        interests: ['technology', 'artificial intelligence', 'quantum computing', 'business'],
        locations: ['United States', 'Canada', 'United Kingdom', 'Germany'],
      },
      content: {
        posts: [],
        templates: [],
      },
      metrics: {
        reach: 125000,
        impressions: 450000,
        engagement: 18500,
        clicks: 3200,
        conversions: 156,
        cost: 3250,
        roi: 4.2,
      },
      quantumOptimization: {
        enabled: true,
        optimizationGoal: 'maximize_engagement',
        predictedPerformance: 87.3,
        recommendations: [
          'Increase posting frequency during 2-4 PM EST',
          'Focus more budget on LinkedIn for B2B audience',
          'Use quantum computing terminology in headlines',
        ],
      },
      automation: {
        autoPost: true,
        autoOptimize: true,
        autoScale: false,
        triggers: [],
      },
      createdAt: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(),
    },
    {
      id: '2',
      name: 'Holiday Season Promotion',
      description: 'Special offers and content for the holiday season',
      status: 'scheduled',
      platforms: ['instagram', 'facebook', 'tiktok'],
      startDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
      endDate: new Date(Date.now() + 35 * 24 * 60 * 60 * 1000),
      budget: 15000,
      spent: 0,
      objective: 'conversions',
      targetAudience: {
        ageRange: [18, 45],
        gender: ['male', 'female'],
        interests: ['shopping', 'technology', 'innovation'],
        locations: ['United States', 'Canada'],
      },
      content: {
        posts: [],
        templates: [],
      },
      metrics: {
        reach: 0,
        impressions: 0,
        engagement: 0,
        clicks: 0,
        conversions: 0,
        cost: 0,
        roi: 0,
      },
      quantumOptimization: {
        enabled: true,
        optimizationGoal: 'maximize_conversions',
        predictedPerformance: 92.1,
        recommendations: [
          'Use festive imagery and quantum-themed holiday content',
          'Target users who engaged with tech content in the past',
          'Schedule posts during peak shopping hours',
        ],
      },
      automation: {
        autoPost: true,
        autoOptimize: true,
        autoScale: true,
        triggers: [],
      },
      createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
      updatedAt: new Date(),
    },
  ]);

  const [selectedCampaign, setSelectedCampaign] = useState<Campaign | null>(null);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  const [newCampaign, setNewCampaign] = useState<Partial<Campaign>>({
    name: '',
    description: '',
    platforms: [],
    budget: 1000,
    objective: 'awareness',
    targetAudience: {
      ageRange: [18, 65],
      gender: ['male', 'female'],
      interests: [],
      locations: [],
    },
    quantumOptimization: {
      enabled: true,
      optimizationGoal: 'maximize_engagement',
      predictedPerformance: 0,
      recommendations: [],
    },
    automation: {
      autoPost: false,
      autoOptimize: false,
      autoScale: false,
      triggers: [],
    },
  });

  const platforms = [
    { id: 'instagram', name: 'Instagram', icon: Instagram, color: '#E4405F' },
    { id: 'facebook', name: 'Facebook', icon: Facebook, color: '#1877F2' },
    { id: 'twitter', name: 'Twitter', icon: Twitter, color: '#1DA1F2' },
    { id: 'linkedin', name: 'LinkedIn', icon: LinkedIn, color: '#0A66C2' },
    { id: 'youtube', name: 'YouTube', icon: YouTube, color: '#FF0000' },
    { id: 'tiktok', name: 'TikTok', icon: TikTok, color: '#000000' },
  ];

  const objectives = [
    { id: 'awareness', name: 'Brand Awareness', icon: Visibility },
    { id: 'engagement', name: 'Engagement', icon: TrendingUp },
    { id: 'traffic', name: 'Website Traffic', icon: Share },
    { id: 'conversions', name: 'Conversions', icon: Target },
    { id: 'leads', name: 'Lead Generation', icon: People },
  ];

  const getPlatformIcon = (platformId: string) => {
    const platform = platforms.find(p => p.id === platformId);
    if (!platform) return null;
    const IconComponent = platform.icon;
    return <IconComponent sx={{ color: platform.color, fontSize: 20 }} />;
  };

  const getStatusColor = (status: Campaign['status']) => {
    switch (status) {
      case 'active': return 'success';
      case 'paused': return 'warning';
      case 'completed': return 'info';
      case 'scheduled': return 'primary';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: Campaign['status']) => {
    switch (status) {
      case 'active': return <PlayArrow />;
      case 'paused': return <Pause />;
      case 'completed': return <CheckCircle />;
      case 'scheduled': return <Schedule />;
      default: return <Edit />;
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const handleCreateCampaign = () => {
    const campaign: Campaign = {
      ...newCampaign,
      id: Date.now().toString(),
      status: 'draft',
      startDate: new Date(),
      endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
      spent: 0,
      content: { posts: [], templates: [] },
      metrics: {
        reach: 0,
        impressions: 0,
        engagement: 0,
        clicks: 0,
        conversions: 0,
        cost: 0,
        roi: 0,
      },
      createdAt: new Date(),
      updatedAt: new Date(),
    } as Campaign;

    setCampaigns([...campaigns, campaign]);
    setCreateDialogOpen(false);
    setNewCampaign({
      name: '',
      description: '',
      platforms: [],
      budget: 1000,
      objective: 'awareness',
      targetAudience: {
        ageRange: [18, 65],
        gender: ['male', 'female'],
        interests: [],
        locations: [],
      },
      quantumOptimization: {
        enabled: true,
        optimizationGoal: 'maximize_engagement',
        predictedPerformance: 0,
        recommendations: [],
      },
      automation: {
        autoPost: false,
        autoOptimize: false,
        autoScale: false,
        triggers: [],
      },
    });
    setActiveStep(0);
  };

  const handleCampaignAction = (campaignId: string, action: 'play' | 'pause' | 'stop' | 'delete') => {
    setCampaigns(campaigns.map(campaign => {
      if (campaign.id === campaignId) {
        switch (action) {
          case 'play':
            return { ...campaign, status: 'active' as const };
          case 'pause':
            return { ...campaign, status: 'paused' as const };
          case 'stop':
            return { ...campaign, status: 'completed' as const };
          default:
            return campaign;
        }
      }
      return campaign;
    }));

    if (action === 'delete') {
      setCampaigns(campaigns.filter(c => c.id !== campaignId));
    }
  };

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  const campaignSteps = [
    'Basic Information',
    'Target Audience',
    'Platforms & Budget',
    'Quantum Optimization',
    'Automation Settings',
  ];

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Campaign Manager
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button variant="outlined" startIcon={<Download />}>
              Export
            </Button>
            <Button variant="outlined" startIcon={<Refresh />}>
              Refresh
            </Button>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setCreateDialogOpen(true)}
            >
              Create Campaign
            </Button>
          </Box>
        </Box>

        {/* Campaign Overview Cards */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Campaign color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Active Campaigns</Typography>
                </Box>
                <Typography variant="h4">
                  {campaigns.filter(c => c.status === 'active').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {campaigns.filter(c => c.status === 'scheduled').length} scheduled
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <AttachMoney color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Total Budget</Typography>
                </Box>
                <Typography variant="h4">
                  {formatCurrency(campaigns.reduce((sum, c) => sum + c.budget, 0))}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {formatCurrency(campaigns.reduce((sum, c) => sum + c.spent, 0))} spent
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <People color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Total Reach</Typography>
                </Box>
                <Typography variant="h4">
                  {formatNumber(campaigns.reduce((sum, c) => sum + c.metrics.reach, 0))}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp color="success" fontSize="small" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    +18.3% this month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Psychology color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Quantum ROI</Typography>
                </Box>
                <Typography variant="h4" color="success.main">
                  {(campaigns.reduce((sum, c) => sum + c.metrics.roi, 0) / campaigns.length).toFixed(1)}x
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  410.7x faster optimization
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Paper sx={{ width: '100%', mb: 3 }}>
          <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
            <Tab label="All Campaigns" />
            <Tab label="Performance" />
            <Tab label="Quantum Insights" />
            <Tab label="Automation" />
          </Tabs>
        </Paper>

        {/* All Campaigns Tab */}
        <TabPanel value={activeTab} index={0}>
          <Grid container spacing={3}>
            {campaigns.map((campaign) => (
              <Grid item xs={12} lg={6} key={campaign.id}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Box>
                        <Typography variant="h6" gutterBottom>
                          {campaign.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {campaign.description}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                          {campaign.platforms.map((platform) => (
                            <Tooltip key={platform} title={platform}>
                              <Avatar sx={{ width: 24, height: 24 }}>
                                {getPlatformIcon(platform)}
                              </Avatar>
                            </Tooltip>
                          ))}
                        </Box>
                      </Box>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Chip
                          label={campaign.status}
                          color={getStatusColor(campaign.status)}
                          icon={getStatusIcon(campaign.status)}
                          size="small"
                        />
                        <IconButton
                          size="small"
                          onClick={() => {
                            setSelectedCampaign(campaign);
                            setEditDialogOpen(true);
                          }}
                        >
                          <Edit fontSize="small" />
                        </IconButton>
                      </Box>
                    </Box>
                    
                    <Grid container spacing={2} sx={{ mb: 2 }}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Budget</Typography>
                        <Typography variant="h6">{formatCurrency(campaign.budget)}</Typography>
                        <LinearProgress
                          variant="determinate"
                          value={(campaign.spent / campaign.budget) * 100}
                          sx={{ mt: 1 }}
                        />
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Reach</Typography>
                        <Typography variant="h6">{formatNumber(campaign.metrics.reach)}</Typography>
                        <Typography variant="body2" color="success.main">
                          ROI: {campaign.metrics.roi}x
                        </Typography>
                      </Grid>
                    </Grid>
                    
                    {campaign.quantumOptimization.enabled && (
                      <Alert severity="info" icon={<Psychology />} sx={{ mb: 2 }}>
                        <Typography variant="body2">
                          Quantum Optimization: {campaign.quantumOptimization.predictedPerformance}% predicted performance
                        </Typography>
                      </Alert>
                    )}
                    
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      {campaign.status === 'active' ? (
                        <Button
                          size="small"
                          startIcon={<Pause />}
                          onClick={() => handleCampaignAction(campaign.id, 'pause')}
                        >
                          Pause
                        </Button>
                      ) : campaign.status === 'paused' ? (
                        <Button
                          size="small"
                          startIcon={<PlayArrow />}
                          onClick={() => handleCampaignAction(campaign.id, 'play')}
                        >
                          Resume
                        </Button>
                      ) : campaign.status === 'scheduled' ? (
                        <Button
                          size="small"
                          startIcon={<PlayArrow />}
                          onClick={() => handleCampaignAction(campaign.id, 'play')}
                        >
                          Start Now
                        </Button>
                      ) : null}
                      
                      <Button
                        size="small"
                        startIcon={<Analytics />}
                        onClick={() => setSelectedCampaign(campaign)}
                      >
                        View Details
                      </Button>
                      
                      <Button
                        size="small"
                        color="error"
                        startIcon={<Delete />}
                        onClick={() => handleCampaignAction(campaign.id, 'delete')}
                      >
                        Delete
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Performance Tab */}
        <TabPanel value={activeTab} index={1}>
          <Grid container spacing={3}>
            <Grid item xs={12} lg={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Campaign Performance Over Time</Typography>
                  <ResponsiveContainer width="100%" height={400}>
                    <AreaChart data={Array.from({ length: 30 }, (_, i) => ({
                      date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toLocaleDateString(),
                      reach: Math.floor(Math.random() * 10000) + 5000,
                      engagement: Math.floor(Math.random() * 2000) + 1000,
                      conversions: Math.floor(Math.random() * 100) + 50,
                    }))}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis />
                      <RechartsTooltip />
                      <Area type="monotone" dataKey="reach" stackId="1" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                      <Area type="monotone" dataKey="engagement" stackId="1" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                      <Area type="monotone" dataKey="conversions" stackId="1" stroke="#ffc658" fill="#ffc658" fillOpacity={0.6} />
                    </AreaChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} lg={4}>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Budget Distribution</Typography>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie
                        data={campaigns}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="budget"
                        label={({ name, value }) => `${name}: ${formatCurrency(value)}`}
                      >
                        {campaigns.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Platform Performance</Typography>
                  <List>
                    {platforms.slice(0, 4).map((platform, index) => (
                      <React.Fragment key={platform.id}>
                        <ListItem>
                          <ListItemAvatar>
                            <Avatar sx={{ bgcolor: platform.color }}>
                              {getPlatformIcon(platform.id)}
                            </Avatar>
                          </ListItemAvatar>
                          <ListItemText
                            primary={platform.name}
                            secondary={
                              <LinearProgress
                                variant="determinate"
                                value={Math.random() * 100}
                                sx={{ mt: 1 }}
                              />
                            }
                          />
                          <Typography variant="body2">
                            {(Math.random() * 5 + 1).toFixed(1)}x ROI
                          </Typography>
                        </ListItem>
                        {index < 3 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Quantum Insights Tab */}
        <TabPanel value={activeTab} index={2}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Alert severity="info" icon={<Psychology />} sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Quantum-Enhanced Campaign Intelligence
                </Typography>
                <Typography variant="body2">
                  Our quantum algorithms analyze campaign performance patterns and predict optimal strategies 
                  with 410.7x faster processing than traditional methods.
                </Typography>
              </Alert>
            </Grid>
            
            {campaigns.map((campaign) => (
              <Grid item xs={12} md={6} key={campaign.id}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Psychology color="primary" />
                      <Typography variant="h6" sx={{ ml: 1 }}>{campaign.name}</Typography>
                    </Box>
                    
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        Quantum Performance Score
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <LinearProgress
                          variant="determinate"
                          value={campaign.quantumOptimization.predictedPerformance}
                          sx={{ flexGrow: 1, mr: 1 }}
                          color="primary"
                        />
                        <Typography variant="body2">
                          {campaign.quantumOptimization.predictedPerformance}%
                        </Typography>
                      </Box>
                    </Box>
                    
                    <Typography variant="subtitle2" gutterBottom>
                      Quantum Recommendations:
                    </Typography>
                    <List dense>
                      {campaign.quantumOptimization.recommendations.map((rec, index) => (
                        <ListItem key={index}>
                          <ListItemText
                            primary={rec}
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Automation Tab */}
        <TabPanel value={activeTab} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Alert severity="success" icon={<AutoAwesome />} sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Quantum-Powered Automation
                </Typography>
                <Typography variant="body2">
                  Leverage quantum computing for intelligent campaign automation, real-time optimization, 
                  and predictive scaling based on performance patterns.
                </Typography>
              </Alert>
            </Grid>
            
            {campaigns.map((campaign) => (
              <Grid item xs={12} md={6} key={campaign.id}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>{campaign.name}</Typography>
                    
                    <Box sx={{ mb: 2 }}>
                      <FormControlLabel
                        control={
                          <Switch
                            checked={campaign.automation.autoPost}
                            onChange={(e) => {
                              setCampaigns(campaigns.map(c => 
                                c.id === campaign.id 
                                  ? { ...c, automation: { ...c.automation, autoPost: e.target.checked } }
                                  : c
                              ));
                            }}
                          />
                        }
                        label="Auto-Post Content"
                      />
                    </Box>
                    
                    <Box sx={{ mb: 2 }}>
                      <FormControlLabel
                        control={
                          <Switch
                            checked={campaign.automation.autoOptimize}
                            onChange={(e) => {
                              setCampaigns(campaigns.map(c => 
                                c.id === campaign.id 
                                  ? { ...c, automation: { ...c.automation, autoOptimize: e.target.checked } }
                                  : c
                              ));
                            }}
                          />
                        }
                        label="Quantum Auto-Optimization"
                      />
                    </Box>
                    
                    <Box sx={{ mb: 2 }}>
                      <FormControlLabel
                        control={
                          <Switch
                            checked={campaign.automation.autoScale}
                            onChange={(e) => {
                              setCampaigns(campaigns.map(c => 
                                c.id === campaign.id 
                                  ? { ...c, automation: { ...c.automation, autoScale: e.target.checked } }
                                  : c
                              ));
                            }}
                          />
                        }
                        label="Auto-Scale Budget"
                      />
                    </Box>
                    
                    <Divider sx={{ my: 2 }} />
                    
                    <Typography variant="subtitle2" gutterBottom>
                      Automation Status:
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                      {campaign.automation.autoPost && (
                        <Chip label="Auto-Posting" color="success" size="small" />
                      )}
                      {campaign.automation.autoOptimize && (
                        <Chip label="Quantum Optimization" color="primary" size="small" />
                      )}
                      {campaign.automation.autoScale && (
                        <Chip label="Auto-Scaling" color="warning" size="small" />
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Create Campaign Dialog */}
        <Dialog
          open={createDialogOpen}
          onClose={() => setCreateDialogOpen(false)}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle>Create New Campaign</DialogTitle>
          <DialogContent>
            <Stepper activeStep={activeStep} orientation="vertical">
              {campaignSteps.map((label, index) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                  <StepContent>
                    {index === 0 && (
                      <Box sx={{ mt: 2 }}>
                        <TextField
                          fullWidth
                          label="Campaign Name"
                          value={newCampaign.name}
                          onChange={(e) => setNewCampaign({ ...newCampaign, name: e.target.value })}
                          sx={{ mb: 2 }}
                        />
                        <TextField
                          fullWidth
                          label="Description"
                          multiline
                          rows={3}
                          value={newCampaign.description}
                          onChange={(e) => setNewCampaign({ ...newCampaign, description: e.target.value })}
                          sx={{ mb: 2 }}
                        />
                        <FormControl fullWidth sx={{ mb: 2 }}>
                          <InputLabel>Objective</InputLabel>
                          <Select
                            value={newCampaign.objective}
                            onChange={(e) => setNewCampaign({ ...newCampaign, objective: e.target.value as any })}
                          >
                            {objectives.map((obj) => (
                              <MenuItem key={obj.id} value={obj.id}>
                                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                  <obj.icon sx={{ mr: 1 }} />
                                  {obj.name}
                                </Box>
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      </Box>
                    )}
                    
                    {index === 1 && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Age Range: {newCampaign.targetAudience?.ageRange?.[0]} - {newCampaign.targetAudience?.ageRange?.[1]}
                        </Typography>
                        <Slider
                          value={newCampaign.targetAudience?.ageRange || [18, 65]}
                          onChange={(e, value) => setNewCampaign({
                            ...newCampaign,
                            targetAudience: {
                              ...newCampaign.targetAudience!,
                              ageRange: value as [number, number]
                            }
                          })}
                          valueLabelDisplay="auto"
                          min={13}
                          max={80}
                          sx={{ mb: 3 }}
                        />
                        <TextField
                          fullWidth
                          label="Interests (comma-separated)"
                          value={newCampaign.targetAudience?.interests?.join(', ') || ''}
                          onChange={(e) => setNewCampaign({
                            ...newCampaign,
                            targetAudience: {
                              ...newCampaign.targetAudience!,
                              interests: e.target.value.split(',').map(s => s.trim())
                            }
                          })}
                          sx={{ mb: 2 }}
                        />
                        <TextField
                          fullWidth
                          label="Locations (comma-separated)"
                          value={newCampaign.targetAudience?.locations?.join(', ') || ''}
                          onChange={(e) => setNewCampaign({
                            ...newCampaign,
                            targetAudience: {
                              ...newCampaign.targetAudience!,
                              locations: e.target.value.split(',').map(s => s.trim())
                            }
                          })}
                        />
                      </Box>
                    )}
                    
                    {index === 2 && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Select Platforms:
                        </Typography>
                        <Grid container spacing={1} sx={{ mb: 3 }}>
                          {platforms.map((platform) => (
                            <Grid item key={platform.id}>
                              <Chip
                                label={platform.name}
                                icon={getPlatformIcon(platform.id)}
                                clickable
                                color={newCampaign.platforms?.includes(platform.id) ? 'primary' : 'default'}
                                onClick={() => {
                                  const platforms = newCampaign.platforms || [];
                                  const newPlatforms = platforms.includes(platform.id)
                                    ? platforms.filter(p => p !== platform.id)
                                    : [...platforms, platform.id];
                                  setNewCampaign({ ...newCampaign, platforms: newPlatforms });
                                }}
                              />
                            </Grid>
                          ))}
                        </Grid>
                        <TextField
                          fullWidth
                          label="Budget ($)"
                          type="number"
                          value={newCampaign.budget}
                          onChange={(e) => setNewCampaign({ ...newCampaign, budget: Number(e.target.value) })}
                        />
                      </Box>
                    )}
                    
                    {index === 3 && (
                      <Box sx={{ mt: 2 }}>
                        <FormControlLabel
                          control={
                            <Switch
                              checked={newCampaign.quantumOptimization?.enabled}
                              onChange={(e) => setNewCampaign({
                                ...newCampaign,
                                quantumOptimization: {
                                  ...newCampaign.quantumOptimization!,
                                  enabled: e.target.checked
                                }
                              })}
                            />
                          }
                          label="Enable Quantum Optimization"
                        />
                        {newCampaign.quantumOptimization?.enabled && (
                          <FormControl fullWidth sx={{ mt: 2 }}>
                            <InputLabel>Optimization Goal</InputLabel>
                            <Select
                              value={newCampaign.quantumOptimization?.optimizationGoal}
                              onChange={(e) => setNewCampaign({
                                ...newCampaign,
                                quantumOptimization: {
                                  ...newCampaign.quantumOptimization!,
                                  optimizationGoal: e.target.value
                                }
                              })}
                            >
                              <MenuItem value="maximize_engagement">Maximize Engagement</MenuItem>
                              <MenuItem value="maximize_reach">Maximize Reach</MenuItem>
                              <MenuItem value="maximize_conversions">Maximize Conversions</MenuItem>
                              <MenuItem value="minimize_cost">Minimize Cost</MenuItem>
                            </Select>
                          </FormControl>
                        )}
                      </Box>
                    )}
                    
                    {index === 4 && (
                      <Box sx={{ mt: 2 }}>
                        <FormControlLabel
                          control={
                            <Switch
                              checked={newCampaign.automation?.autoPost}
                              onChange={(e) => setNewCampaign({
                                ...newCampaign,
                                automation: {
                                  ...newCampaign.automation!,
                                  autoPost: e.target.checked
                                }
                              })}
                            />
                          }
                          label="Auto-Post Content"
                        />
                        <FormControlLabel
                          control={
                            <Switch
                              checked={newCampaign.automation?.autoOptimize}
                              onChange={(e) => setNewCampaign({
                                ...newCampaign,
                                automation: {
                                  ...newCampaign.automation!,
                                  autoOptimize: e.target.checked
                                }
                              })}
                            />
                          }
                          label="Quantum Auto-Optimization"
                        />
                        <FormControlLabel
                          control={
                            <Switch
                              checked={newCampaign.automation?.autoScale}
                              onChange={(e) => setNewCampaign({
                                ...newCampaign,
                                automation: {
                                  ...newCampaign.automation!,
                                  autoScale: e.target.checked
                                }
                              })}
                            />
                          }
                          label="Auto-Scale Budget"
                        />
                      </Box>
                    )}
                    
                    <Box sx={{ mb: 2, mt: 2 }}>
                      <Button
                        disabled={activeStep === 0}
                        onClick={() => setActiveStep(activeStep - 1)}
                        sx={{ mr: 1 }}
                      >
                        Back
                      </Button>
                      <Button
                        variant="contained"
                        onClick={() => {
                          if (activeStep === campaignSteps.length - 1) {
                            handleCreateCampaign();
                          } else {
                            setActiveStep(activeStep + 1);
                          }
                        }}
                      >
                        {activeStep === campaignSteps.length - 1 ? 'Create Campaign' : 'Continue'}
                      </Button>
                    </Box>
                  </StepContent>
                </Step>
              ))}
            </Stepper>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setCreateDialogOpen(false)}>Cancel</Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default CampaignManager;