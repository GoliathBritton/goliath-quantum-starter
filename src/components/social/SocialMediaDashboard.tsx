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
  LinearProgress,
  IconButton,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  Switch,
  FormControlLabel,
  Tabs,
  Tab,
  Paper,
} from '@mui/material';
import {
  Instagram,
  Facebook,
  Twitter,
  LinkedIn,
  YouTube,
  TikTok,
  Add,
  MoreVert,
  Schedule,
  Analytics,
  Settings,
  Refresh,
  Campaign,
  TrendingUp,
  People,
  Visibility,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';

interface SocialAccount {
  id: string;
  platform: 'instagram' | 'facebook' | 'twitter' | 'linkedin' | 'youtube' | 'tiktok';
  username: string;
  displayName: string;
  followers: number;
  isConnected: boolean;
  lastSync: Date;
  avatar?: string;
}

interface SocialPost {
  id: string;
  platform: string;
  content: string;
  scheduledTime?: Date;
  publishedTime?: Date;
  status: 'draft' | 'scheduled' | 'published' | 'failed';
  engagement: {
    likes: number;
    comments: number;
    shares: number;
    views: number;
  };
  media?: {
    type: 'image' | 'video';
    url: string;
    thumbnail?: string;
  }[];
}

interface AnalyticsData {
  platform: string;
  followers: number;
  engagement: number;
  reach: number;
  impressions: number;
  growth: number;
}

const SocialMediaDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [accounts, setAccounts] = useState<SocialAccount[]>([
    {
      id: '1',
      platform: 'instagram',
      username: '@nqba_platform',
      displayName: 'NQBA Platform',
      followers: 15420,
      isConnected: true,
      lastSync: new Date(),
    },
    {
      id: '2',
      platform: 'twitter',
      username: '@NQBAPlatform',
      displayName: 'NQBA Platform',
      followers: 8750,
      isConnected: true,
      lastSync: new Date(),
    },
    {
      id: '3',
      platform: 'linkedin',
      username: 'nqba-platform',
      displayName: 'NQBA Platform',
      followers: 3200,
      isConnected: true,
      lastSync: new Date(),
    },
    {
      id: '4',
      platform: 'facebook',
      username: 'NQBAPlatform',
      displayName: 'NQBA Platform',
      followers: 12100,
      isConnected: false,
      lastSync: new Date(),
    },
  ]);

  const [posts, setPosts] = useState<SocialPost[]>([
    {
      id: '1',
      platform: 'instagram',
      content: 'Revolutionizing business intelligence with quantum computing! 🚀 #QuantumAI #NQBA',
      publishedTime: new Date(Date.now() - 2 * 60 * 60 * 1000),
      status: 'published',
      engagement: { likes: 245, comments: 18, shares: 32, views: 1250 },
    },
    {
      id: '2',
      platform: 'twitter',
      content: 'Our quantum advantage just hit 410.7x speedup! The future of AI is here. #QuantumComputing',
      scheduledTime: new Date(Date.now() + 2 * 60 * 60 * 1000),
      status: 'scheduled',
      engagement: { likes: 0, comments: 0, shares: 0, views: 0 },
    },
  ]);

  const [analyticsData] = useState<AnalyticsData[]>([
    { platform: 'Instagram', followers: 15420, engagement: 4.2, reach: 45000, impressions: 120000, growth: 12.5 },
    { platform: 'Twitter', followers: 8750, engagement: 3.8, reach: 28000, impressions: 85000, growth: 8.3 },
    { platform: 'LinkedIn', followers: 3200, engagement: 6.1, reach: 12000, impressions: 35000, growth: 15.2 },
    { platform: 'Facebook', followers: 12100, engagement: 2.9, reach: 35000, impressions: 95000, growth: 5.7 },
  ]);

  const [newPostDialog, setNewPostDialog] = useState(false);
  const [newPost, setNewPost] = useState({
    content: '',
    platforms: [] as string[],
    scheduledTime: '',
    media: [] as File[],
  });

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'instagram': return <Instagram />;
      case 'facebook': return <Facebook />;
      case 'twitter': return <Twitter />;
      case 'linkedin': return <LinkedIn />;
      case 'youtube': return <YouTube />;
      case 'tiktok': return <TikTok />;
      default: return null;
    }
  };

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case 'instagram': return '#E4405F';
      case 'facebook': return '#1877F2';
      case 'twitter': return '#1DA1F2';
      case 'linkedin': return '#0A66C2';
      case 'youtube': return '#FF0000';
      case 'tiktok': return '#000000';
      default: return '#666666';
    }
  };

  const handleConnectAccount = (platform: string) => {
    // Simulate OAuth connection
    console.log(`Connecting to ${platform}...`);
    // In real implementation, this would open OAuth flow
  };

  const handleCreatePost = () => {
    const post: SocialPost = {
      id: Date.now().toString(),
      platform: newPost.platforms[0] || 'instagram',
      content: newPost.content,
      scheduledTime: newPost.scheduledTime ? new Date(newPost.scheduledTime) : undefined,
      status: newPost.scheduledTime ? 'scheduled' : 'published',
      engagement: { likes: 0, comments: 0, shares: 0, views: 0 },
    };
    
    setPosts([...posts, post]);
    setNewPostDialog(false);
    setNewPost({ content: '', platforms: [], scheduledTime: '', media: [] });
  };

  const formatNumber = (num: number) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Social Media Management
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setNewPostDialog(true)}
          >
            Create Post
          </Button>
          <Button
            variant="outlined"
            startIcon={<Analytics />}
          >
            Analytics
          </Button>
        </Box>
      </Box>

      <Paper sx={{ width: '100%', mb: 3 }}>
        <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
          <Tab label="Overview" />
          <Tab label="Posts" />
          <Tab label="Analytics" />
          <Tab label="Accounts" />
        </Tabs>
      </Paper>

      {/* Overview Tab */}
      <TabPanel value={activeTab} index={0}>
        <Grid container spacing={3}>
          {/* Quick Stats */}
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <People color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Total Followers</Typography>
                </Box>
                <Typography variant="h4">
                  {formatNumber(accounts.reduce((sum, acc) => sum + acc.followers, 0))}
                </Typography>
                <Typography variant="body2" color="success.main">
                  +12.5% this month
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <TrendingUp color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Engagement Rate</Typography>
                </Box>
                <Typography variant="h4">4.2%</Typography>
                <Typography variant="body2" color="success.main">
                  +0.8% this week
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Visibility color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Total Reach</Typography>
                </Box>
                <Typography variant="h4">{formatNumber(120000)}</Typography>
                <Typography variant="body2" color="success.main">
                  +18.3% this month
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Schedule color="primary" />
                  <Typography variant="h6" sx={{ ml: 1 }}>Scheduled Posts</Typography>
                </Box>
                <Typography variant="h4">
                  {posts.filter(p => p.status === 'scheduled').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Next in 2 hours
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {/* Connected Accounts */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Connected Accounts</Typography>
                <Grid container spacing={2}>
                  {accounts.map((account) => (
                    <Grid item xs={12} sm={6} md={3} key={account.id}>
                      <Card variant="outlined">
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Avatar sx={{ bgcolor: getPlatformColor(account.platform), mr: 2 }}>
                              {getPlatformIcon(account.platform)}
                            </Avatar>
                            <Box>
                              <Typography variant="subtitle1">{account.displayName}</Typography>
                              <Typography variant="body2" color="text.secondary">
                                {account.username}
                              </Typography>
                            </Box>
                          </Box>
                          <Typography variant="h6">{formatNumber(account.followers)} followers</Typography>
                          <Chip 
                            label={account.isConnected ? 'Connected' : 'Disconnected'}
                            color={account.isConnected ? 'success' : 'error'}
                            size="small"
                            sx={{ mt: 1 }}
                          />
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Posts Tab */}
      <TabPanel value={activeTab} index={1}>
        <Grid container spacing={3}>
          {posts.map((post) => (
            <Grid item xs={12} md={6} key={post.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar sx={{ bgcolor: getPlatformColor(post.platform), mr: 2 }}>
                        {getPlatformIcon(post.platform)}
                      </Avatar>
                      <Box>
                        <Typography variant="subtitle1" sx={{ textTransform: 'capitalize' }}>
                          {post.platform}
                        </Typography>
                        <Chip 
                          label={post.status}
                          color={post.status === 'published' ? 'success' : post.status === 'scheduled' ? 'warning' : 'default'}
                          size="small"
                        />
                      </Box>
                    </Box>
                    <IconButton>
                      <MoreVert />
                    </IconButton>
                  </Box>
                  
                  <Typography variant="body1" sx={{ mb: 2 }}>
                    {post.content}
                  </Typography>
                  
                  {post.status === 'published' && (
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
                      <Typography variant="body2">❤️ {post.engagement.likes}</Typography>
                      <Typography variant="body2">💬 {post.engagement.comments}</Typography>
                      <Typography variant="body2">🔄 {post.engagement.shares}</Typography>
                      <Typography variant="body2">👁️ {post.engagement.views}</Typography>
                    </Box>
                  )}
                  
                  {post.scheduledTime && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                      Scheduled for: {post.scheduledTime.toLocaleString()}
                    </Typography>
                  )}
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      {/* Analytics Tab */}
      <TabPanel value={activeTab} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Engagement Over Time</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={analyticsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="platform" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="engagement" stroke="#8884d8" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Platform Distribution</Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={analyticsData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="followers"
                      label={({ platform, value }) => `${platform}: ${formatNumber(value)}`}
                    >
                      {analyticsData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={getPlatformColor(entry.platform.toLowerCase())} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Accounts Tab */}
      <TabPanel value={activeTab} index={3}>
        <Grid container spacing={3}>
          {accounts.map((account) => (
            <Grid item xs={12} md={6} key={account.id}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar sx={{ bgcolor: getPlatformColor(account.platform), mr: 2, width: 56, height: 56 }}>
                        {getPlatformIcon(account.platform)}
                      </Avatar>
                      <Box>
                        <Typography variant="h6">{account.displayName}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {account.username}
                        </Typography>
                        <Typography variant="h6" sx={{ mt: 1 }}>
                          {formatNumber(account.followers)} followers
                        </Typography>
                      </Box>
                    </Box>
                    <IconButton>
                      <Settings />
                    </IconButton>
                  </Box>
                  
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
                    <Chip 
                      label={account.isConnected ? 'Connected' : 'Disconnected'}
                      color={account.isConnected ? 'success' : 'error'}
                    />
                    <Button
                      variant={account.isConnected ? 'outlined' : 'contained'}
                      onClick={() => handleConnectAccount(account.platform)}
                    >
                      {account.isConnected ? 'Reconnect' : 'Connect'}
                    </Button>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Last sync: {account.lastSync.toLocaleString()}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      {/* Create Post Dialog */}
      <Dialog open={newPostDialog} onClose={() => setNewPostDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Post</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            multiline
            rows={4}
            label="Post Content"
            value={newPost.content}
            onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
            sx={{ mb: 2, mt: 1 }}
          />
          
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Platforms</InputLabel>
            <Select
              multiple
              value={newPost.platforms}
              onChange={(e) => setNewPost({ ...newPost, platforms: e.target.value as string[] })}
            >
              {accounts.filter(acc => acc.isConnected).map((account) => (
                <MenuItem key={account.platform} value={account.platform}>
                  <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {getPlatformIcon(account.platform)}
                    <Typography sx={{ ml: 1, textTransform: 'capitalize' }}>
                      {account.platform}
                    </Typography>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          
          <TextField
            fullWidth
            type="datetime-local"
            label="Schedule Time (Optional)"
            value={newPost.scheduledTime}
            onChange={(e) => setNewPost({ ...newPost, scheduledTime: e.target.value })}
            InputLabelProps={{ shrink: true }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewPostDialog(false)}>Cancel</Button>
          <Button onClick={handleCreatePost} variant="contained">
            {newPost.scheduledTime ? 'Schedule Post' : 'Publish Now'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SocialMediaDashboard;