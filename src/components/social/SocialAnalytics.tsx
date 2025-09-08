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
  Divider,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  Visibility,
  ThumbUp,
  Comment,
  Share,
  People,
  Analytics,
  Download,
  Refresh,
  Psychology,
  Instagram,
  Facebook,
  Twitter,
  LinkedIn,
  YouTube,
  TikTok,
  CalendarToday,
  Schedule,
  Campaign,
  Star,
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
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ComposedChart,
} from 'recharts';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import socialMediaService, { AnalyticsData } from '../../services/socialMediaService';

interface EngagementMetrics {
  platform: string;
  likes: number;
  comments: number;
  shares: number;
  views: number;
  followers: number;
  engagementRate: number;
  reach: number;
  impressions: number;
  growth: number;
}

interface PostPerformance {
  id: string;
  platform: string;
  content: string;
  publishedTime: Date;
  likes: number;
  comments: number;
  shares: number;
  views: number;
  engagementRate: number;
  reach: number;
  score: number;
}

interface AudienceInsight {
  platform: string;
  demographics: {
    ageGroups: { range: string; percentage: number }[];
    gender: { male: number; female: number; other: number };
    locations: { country: string; percentage: number }[];
    interests: { category: string; percentage: number }[];
  };
  activeHours: { hour: number; engagement: number }[];
  bestPostingTimes: Date[];
}

const SocialAnalytics: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [selectedPlatform, setSelectedPlatform] = useState('all');
  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
    end: new Date(),
  });
  const [period, setPeriod] = useState<'day' | 'week' | 'month'>('month');

  const [metrics, setMetrics] = useState<EngagementMetrics[]>([
    {
      platform: 'instagram',
      likes: 15420,
      comments: 892,
      shares: 445,
      views: 125000,
      followers: 18500,
      engagementRate: 4.2,
      reach: 45000,
      impressions: 120000,
      growth: 12.5,
    },
    {
      platform: 'twitter',
      likes: 8750,
      comments: 456,
      shares: 1200,
      views: 85000,
      followers: 12300,
      engagementRate: 3.8,
      reach: 28000,
      impressions: 85000,
      growth: 8.3,
    },
    {
      platform: 'linkedin',
      likes: 3200,
      comments: 234,
      shares: 567,
      views: 35000,
      followers: 5600,
      engagementRate: 6.1,
      reach: 12000,
      impressions: 35000,
      growth: 15.2,
    },
    {
      platform: 'facebook',
      likes: 12100,
      comments: 678,
      shares: 890,
      views: 95000,
      followers: 15800,
      engagementRate: 2.9,
      reach: 35000,
      impressions: 95000,
      growth: 5.7,
    },
  ]);

  const [topPosts, setTopPosts] = useState<PostPerformance[]>([
    {
      id: '1',
      platform: 'instagram',
      content: 'Revolutionizing business intelligence with quantum computing! 🚀 #QuantumAI #NQBA',
      publishedTime: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
      likes: 1245,
      comments: 89,
      shares: 156,
      views: 8500,
      engagementRate: 5.8,
      reach: 12000,
      score: 92,
    },
    {
      id: '2',
      platform: 'twitter',
      content: 'Our quantum advantage just hit 410.7x speedup! The future of AI is here. #QuantumComputing',
      publishedTime: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
      likes: 892,
      comments: 45,
      shares: 234,
      views: 6500,
      engagementRate: 4.2,
      reach: 9500,
      score: 87,
    },
  ]);

  const [audienceInsights, setAudienceInsights] = useState<AudienceInsight[]>([
    {
      platform: 'instagram',
      demographics: {
        ageGroups: [
          { range: '18-24', percentage: 25 },
          { range: '25-34', percentage: 35 },
          { range: '35-44', percentage: 25 },
          { range: '45+', percentage: 15 },
        ],
        gender: { male: 55, female: 42, other: 3 },
        locations: [
          { country: 'United States', percentage: 45 },
          { country: 'Canada', percentage: 15 },
          { country: 'United Kingdom', percentage: 12 },
          { country: 'Germany', percentage: 10 },
          { country: 'Others', percentage: 18 },
        ],
        interests: [
          { category: 'Technology', percentage: 65 },
          { category: 'Business', percentage: 45 },
          { category: 'Innovation', percentage: 38 },
          { category: 'AI/ML', percentage: 52 },
        ],
      },
      activeHours: Array.from({ length: 24 }, (_, i) => ({
        hour: i,
        engagement: Math.random() * 100,
      })),
      bestPostingTimes: [
        new Date(2024, 0, 1, 9, 0),
        new Date(2024, 0, 1, 14, 0),
        new Date(2024, 0, 1, 19, 0),
      ],
    },
  ]);

  const [timeSeriesData, setTimeSeriesData] = useState(
    Array.from({ length: 30 }, (_, i) => ({
      date: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toLocaleDateString(),
      engagement: Math.floor(Math.random() * 1000) + 500,
      reach: Math.floor(Math.random() * 5000) + 2000,
      followers: 18500 + Math.floor(Math.random() * 200) - 100,
      impressions: Math.floor(Math.random() * 10000) + 5000,
    }))
  );

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

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const calculateTotalMetrics = () => {
    const filteredMetrics = selectedPlatform === 'all' 
      ? metrics 
      : metrics.filter(m => m.platform === selectedPlatform);
    
    return filteredMetrics.reduce(
      (totals, metric) => ({
        followers: totals.followers + metric.followers,
        engagement: totals.engagement + metric.likes + metric.comments + metric.shares,
        reach: totals.reach + metric.reach,
        impressions: totals.impressions + metric.impressions,
      }),
      { followers: 0, engagement: 0, reach: 0, impressions: 0 }
    );
  };

  const totalMetrics = calculateTotalMetrics();

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Social Media Analytics
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <FormControl size="small" sx={{ minWidth: 120 }}>
              <InputLabel>Platform</InputLabel>
              <Select
                value={selectedPlatform}
                onChange={(e) => setSelectedPlatform(e.target.value)}
              >
                <MenuItem value="all">All Platforms</MenuItem>
                {platforms.map((platform) => (
                  <MenuItem key={platform.id} value={platform.id}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {getPlatformIcon(platform.id)}
                      <Typography sx={{ ml: 1 }}>{platform.name}</Typography>
                    </Box>
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl size="small" sx={{ minWidth: 100 }}>
              <InputLabel>Period</InputLabel>
              <Select
                value={period}
                onChange={(e) => setPeriod(e.target.value as any)}
              >
                <MenuItem value="day">Daily</MenuItem>
                <MenuItem value="week">Weekly</MenuItem>
                <MenuItem value="month">Monthly</MenuItem>
              </Select>
            </FormControl>
            <Button variant="outlined" startIcon={<Download />}>
              Export
            </Button>
            <Button variant="outlined" startIcon={<Refresh />}>
              Refresh
            </Button>
          </Box>
        </Box>

        {/* Key Metrics Cards */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <People color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Total Followers</Typography>
                </Box>
                <Typography variant="h4">{formatNumber(totalMetrics.followers)}</Typography>
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
                  <Typography variant="h6" sx={{ ml: 1 }}>Total Engagement</Typography>
                </Box>
                <Typography variant="h4">{formatNumber(totalMetrics.engagement)}</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp color="success" fontSize="small" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    +8.3% this week
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Visibility color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Total Reach</Typography>
                </Box>
                <Typography variant="h4">{formatNumber(totalMetrics.reach)}</Typography>
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
                  <Analytics color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Impressions</Typography>
                </Box>
                <Typography variant="h4">{formatNumber(totalMetrics.impressions)}</Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                  <TrendingUp color="success" fontSize="small" />
                  <Typography variant="body2" color="success.main" sx={{ ml: 0.5 }}>
                    +15.7% this month
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Paper sx={{ width: '100%', mb: 3 }}>
          <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
            <Tab label="Overview" />
            <Tab label="Platform Performance" />
            <Tab label="Top Posts" />
            <Tab label="Audience Insights" />
            <Tab label="Quantum Analytics" />
          </Tabs>
        </Paper>

        {/* Overview Tab */}
        <TabPanel value={activeTab} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} lg={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Engagement Over Time</Typography>
                  <ResponsiveContainer width="100%" height={400}>
                    <ComposedChart data={timeSeriesData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="date" />
                      <YAxis yAxisId="left" />
                      <YAxis yAxisId="right" orientation="right" />
                      <RechartsTooltip />
                      <Area yAxisId="left" type="monotone" dataKey="reach" stackId="1" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                      <Bar yAxisId="right" dataKey="engagement" fill="#82ca9d" />
                      <Line yAxisId="left" type="monotone" dataKey="followers" stroke="#ff7300" strokeWidth={2} />
                    </ComposedChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} lg={4}>
              <Card sx={{ mb: 3 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Platform Distribution</Typography>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie
                        data={metrics}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="followers"
                        label={({ platform, value }) => `${platform}: ${formatNumber(value)}`}
                      >
                        {metrics.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={getPlatformColor(entry.platform)} />
                        ))}
                      </Pie>
                      <RechartsTooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
              
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Engagement Rate by Platform</Typography>
                  <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={metrics}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="platform" />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="engagementRate" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Platform Performance Tab */}
        <TabPanel value={activeTab} index={1}>
          <Grid container spacing={3}>
            {metrics.map((metric) => (
              <Grid item xs={12} md={6} lg={4} key={metric.platform}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ bgcolor: getPlatformColor(metric.platform), mr: 2 }}>
                        {getPlatformIcon(metric.platform)}
                      </Avatar>
                      <Box>
                        <Typography variant="h6" sx={{ textTransform: 'capitalize' }}>
                          {metric.platform}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {formatNumber(metric.followers)} followers
                        </Typography>
                      </Box>
                    </Box>
                    
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Likes</Typography>
                        <Typography variant="h6">{formatNumber(metric.likes)}</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Comments</Typography>
                        <Typography variant="h6">{formatNumber(metric.comments)}</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Shares</Typography>
                        <Typography variant="h6">{formatNumber(metric.shares)}</Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">Reach</Typography>
                        <Typography variant="h6">{formatNumber(metric.reach)}</Typography>
                      </Grid>
                    </Grid>
                    
                    <Box sx={{ mt: 2 }}>
                      <Typography variant="body2" color="text.secondary">Engagement Rate</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <LinearProgress
                          variant="determinate"
                          value={metric.engagementRate}
                          sx={{ flexGrow: 1, mr: 1 }}
                        />
                        <Typography variant="body2">{metric.engagementRate}%</Typography>
                      </Box>
                    </Box>
                    
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 2 }}>
                      <TrendingUp color={metric.growth > 0 ? 'success' : 'error'} fontSize="small" />
                      <Typography 
                        variant="body2" 
                        color={metric.growth > 0 ? 'success.main' : 'error.main'}
                        sx={{ ml: 0.5 }}
                      >
                        {metric.growth > 0 ? '+' : ''}{metric.growth}% growth
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Top Posts Tab */}
        <TabPanel value={activeTab} index={2}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Top Performing Posts</Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Platform</TableCell>
                      <TableCell>Content</TableCell>
                      <TableCell>Published</TableCell>
                      <TableCell align="right">Likes</TableCell>
                      <TableCell align="right">Comments</TableCell>
                      <TableCell align="right">Shares</TableCell>
                      <TableCell align="right">Engagement Rate</TableCell>
                      <TableCell align="right">Score</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {topPosts.map((post) => (
                      <TableRow key={post.id}>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            {getPlatformIcon(post.platform)}
                            <Typography sx={{ ml: 1, textTransform: 'capitalize' }}>
                              {post.platform}
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" sx={{ maxWidth: 300 }}>
                            {post.content.substring(0, 80)}...
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {post.publishedTime.toLocaleDateString()}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">{formatNumber(post.likes)}</TableCell>
                        <TableCell align="right">{formatNumber(post.comments)}</TableCell>
                        <TableCell align="right">{formatNumber(post.shares)}</TableCell>
                        <TableCell align="right">{post.engagementRate}%</TableCell>
                        <TableCell align="right">
                          <Chip
                            label={post.score}
                            color={post.score >= 90 ? 'success' : post.score >= 70 ? 'warning' : 'default'}
                            size="small"
                          />
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </TabPanel>

        {/* Audience Insights Tab */}
        <TabPanel value={activeTab} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Age Demographics</Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={audienceInsights[0]?.demographics.ageGroups || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="range" />
                      <YAxis />
                      <RechartsTooltip />
                      <Bar dataKey="percentage" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Geographic Distribution</Typography>
                  <List>
                    {audienceInsights[0]?.demographics.locations.map((location, index) => (
                      <React.Fragment key={location.country}>
                        <ListItem>
                          <ListItemText
                            primary={location.country}
                            secondary={
                              <LinearProgress
                                variant="determinate"
                                value={location.percentage}
                                sx={{ mt: 1 }}
                              />
                            }
                          />
                          <Typography variant="body2">{location.percentage}%</Typography>
                        </ListItem>
                        {index < audienceInsights[0].demographics.locations.length - 1 && <Divider />}
                      </React.Fragment>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Audience Activity</Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <LineChart data={audienceInsights[0]?.activeHours || []}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="hour" />
                      <YAxis />
                      <RechartsTooltip />
                      <Line type="monotone" dataKey="engagement" stroke="#8884d8" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Interest Categories</Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart data={audienceInsights[0]?.demographics.interests || []}>
                      <PolarGrid />
                      <PolarAngleAxis dataKey="category" />
                      <PolarRadiusAxis />
                      <Radar
                        name="Interest"
                        dataKey="percentage"
                        stroke="#8884d8"
                        fill="#8884d8"
                        fillOpacity={0.6}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Quantum Analytics Tab */}
        <TabPanel value={activeTab} index={4}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Alert severity="info" icon={<Psychology />} sx={{ mb: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Quantum-Enhanced Analytics
                </Typography>
                <Typography variant="body2">
                  Our quantum computing algorithms analyze complex patterns in your social media data to provide 
                  unprecedented insights and predictions with 410.7x faster processing than traditional methods.
                </Typography>
              </Alert>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Psychology color="primary" />
                    <Typography variant="h6" sx={{ ml: 1 }}>Quantum Advantage</Typography>
                  </Box>
                  <Typography variant="h3" color="primary">410.7x</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Faster analytics processing
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={95}
                    sx={{ mt: 2 }}
                    color="primary"
                  />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <TrendingUp color="success" />
                    <Typography variant="h6" sx={{ ml: 1 }}>Prediction Accuracy</Typography>
                  </Box>
                  <Typography variant="h3" color="success.main">94.2%</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Engagement prediction accuracy
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={94.2}
                    sx={{ mt: 2 }}
                    color="success"
                  />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Schedule color="warning" />
                    <Typography variant="h6" sx={{ ml: 1 }}>Optimal Timing</Typography>
                  </Box>
                  <Typography variant="h3" color="warning.main">+28%</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Engagement boost from quantum timing
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={78}
                    sx={{ mt: 2 }}
                    color="warning"
                  />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Quantum Pattern Analysis
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Advanced quantum algorithms identify hidden patterns in your social media performance
                  </Typography>
                  <Grid container spacing={2} sx={{ mt: 2 }}>
                    <Grid item xs={12} md={6}>
                      <Paper sx={{ p: 2, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
                        <Typography variant="subtitle1" gutterBottom>
                          🔮 Quantum Insight: Optimal Posting Windows
                        </Typography>
                        <Typography variant="body2">
                          Our quantum analysis reveals that posts published between 2-4 PM on weekdays 
                          achieve 34% higher engagement rates due to quantum-detected audience behavior patterns.
                        </Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Paper sx={{ p: 2, bgcolor: 'success.light', color: 'success.contrastText' }}>
                        <Typography variant="subtitle1" gutterBottom>
                          ⚡ Quantum Prediction: Viral Content Probability
                        </Typography>
                        <Typography variant="body2">
                          Content featuring quantum computing topics has a 67% probability of achieving 
                          viral status based on quantum sentiment analysis and engagement modeling.
                        </Typography>
                      </Paper>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>
      </Box>
    </LocalizationProvider>
  );
};

export default SocialAnalytics;