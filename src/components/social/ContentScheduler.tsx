import React, { useState, useEffect } from 'react';
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
  Chip,
  Avatar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  Switch,
  FormControlLabel,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Divider,
  Alert,
  LinearProgress,
  Fab,
} from '@mui/material';
import {
  Add,
  Schedule,
  Edit,
  Delete,
  PlayArrow,
  Pause,
  ExpandMore,
  CalendarToday,
  AutoAwesome,
  TrendingUp,
  Psychology,
  Instagram,
  Facebook,
  Twitter,
  LinkedIn,
  YouTube,
  TikTok,
  Image,
  VideoFile,
  Analytics,
  Campaign,
} from '@mui/icons-material';
import { DateTimePicker } from '@mui/x-date-pickers/DateTimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import socialMediaService, { SocialPost, PostCreationData } from '../../services/socialMediaService';

interface ScheduledCampaign {
  id: string;
  name: string;
  description: string;
  startDate: Date;
  endDate: Date;
  posts: SocialPost[];
  isActive: boolean;
  platforms: string[];
  frequency: 'daily' | 'weekly' | 'monthly';
  quantumOptimized: boolean;
}

interface ContentTemplate {
  id: string;
  name: string;
  content: string;
  platforms: string[];
  hashtags: string[];
  category: string;
}

const ContentScheduler: React.FC = () => {
  const [campaigns, setCampaigns] = useState<ScheduledCampaign[]>([
    {
      id: '1',
      name: 'Quantum AI Launch Campaign',
      description: 'Promote our quantum computing platform across all channels',
      startDate: new Date(),
      endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
      posts: [],
      isActive: true,
      platforms: ['instagram', 'twitter', 'linkedin'],
      frequency: 'daily',
      quantumOptimized: true,
    },
  ]);

  const [templates, setTemplates] = useState<ContentTemplate[]>([
    {
      id: '1',
      name: 'Product Feature Highlight',
      content: 'Discover the power of quantum computing with NQBA! 🚀 Our latest feature delivers {feature_name} with unprecedented speed and accuracy. #QuantumAI #Innovation',
      platforms: ['instagram', 'twitter', 'linkedin'],
      hashtags: ['#QuantumAI', '#Innovation', '#TechNews'],
      category: 'Product',
    },
    {
      id: '2',
      name: 'Industry Insight',
      content: 'The future of {industry} is being shaped by quantum computing. Here\'s how NQBA is leading the transformation... 💡 #FutureOfTech #QuantumComputing',
      platforms: ['linkedin', 'twitter'],
      hashtags: ['#FutureOfTech', '#QuantumComputing', '#Industry'],
      category: 'Educational',
    },
  ]);

  const [schedulerDialog, setSchedulerDialog] = useState(false);
  const [campaignDialog, setCampaignDialog] = useState(false);
  const [templateDialog, setTemplateDialog] = useState(false);
  const [selectedCampaign, setSelectedCampaign] = useState<ScheduledCampaign | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<ContentTemplate | null>(null);

  const [newPost, setNewPost] = useState<PostCreationData>({
    content: '',
    platforms: [],
    scheduledTime: new Date(),
    hashtags: [],
  });

  const [newCampaign, setNewCampaign] = useState({
    name: '',
    description: '',
    startDate: new Date(),
    endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
    platforms: [] as string[],
    frequency: 'daily' as 'daily' | 'weekly' | 'monthly',
    quantumOptimized: true,
  });

  const [newTemplate, setNewTemplate] = useState({
    name: '',
    content: '',
    platforms: [] as string[],
    hashtags: [] as string[],
    category: '',
  });

  const [optimizedTimes, setOptimizedTimes] = useState<Date[]>([]);
  const [engagementPrediction, setEngagementPrediction] = useState<any>(null);
  const [isOptimizing, setIsOptimizing] = useState(false);

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

  const handleOptimizePosting = async () => {
    if (!newPost.content || newPost.platforms.length === 0) return;

    setIsOptimizing(true);
    try {
      // Get optimized posting times
      const times = await socialMediaService.optimizePostTiming(
        newPost.platforms[0],
        newPost.content
      );
      setOptimizedTimes(times);

      // Get engagement prediction
      const prediction = await socialMediaService.predictEngagement(
        newPost.platforms[0],
        newPost.content,
        newPost.scheduledTime || new Date()
      );
      setEngagementPrediction(prediction);
    } catch (error) {
      console.error('Error optimizing post:', error);
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleCreatePost = async () => {
    try {
      await socialMediaService.createPost(newPost);
      setSchedulerDialog(false);
      setNewPost({
        content: '',
        platforms: [],
        scheduledTime: new Date(),
        hashtags: [],
      });
      setOptimizedTimes([]);
      setEngagementPrediction(null);
    } catch (error) {
      console.error('Error creating post:', error);
    }
  };

  const handleCreateCampaign = () => {
    const campaign: ScheduledCampaign = {
      id: Date.now().toString(),
      ...newCampaign,
      posts: [],
      isActive: true,
    };
    setCampaigns([...campaigns, campaign]);
    setCampaignDialog(false);
    setNewCampaign({
      name: '',
      description: '',
      startDate: new Date(),
      endDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
      platforms: [],
      frequency: 'daily',
      quantumOptimized: true,
    });
  };

  const handleCreateTemplate = () => {
    const template: ContentTemplate = {
      id: Date.now().toString(),
      ...newTemplate,
    };
    setTemplates([...templates, template]);
    setTemplateDialog(false);
    setNewTemplate({
      name: '',
      content: '',
      platforms: [],
      hashtags: [],
      category: '',
    });
  };

  const handleUseTemplate = (template: ContentTemplate) => {
    setNewPost({
      ...newPost,
      content: template.content,
      platforms: template.platforms,
      hashtags: template.hashtags,
    });
    setTemplateDialog(false);
  };

  const toggleCampaign = (campaignId: string) => {
    setCampaigns(campaigns.map(campaign => 
      campaign.id === campaignId 
        ? { ...campaign, isActive: !campaign.isActive }
        : campaign
    ));
  };

  const generateQuantumContent = async (topic: string, platform: string) => {
    try {
      const content = await socialMediaService.generateQuantumContent(topic, platform);
      setNewPost({ ...newPost, content });
    } catch (error) {
      console.error('Error generating content:', error);
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Box sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Content Scheduler
          </Typography>
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="outlined"
              startIcon={<Campaign />}
              onClick={() => setCampaignDialog(true)}
            >
              New Campaign
            </Button>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setSchedulerDialog(true)}
            >
              Schedule Post
            </Button>
          </Box>
        </Box>

        <Grid container spacing={3}>
          {/* Active Campaigns */}
          <Grid item xs={12} lg={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Active Campaigns
                </Typography>
                {campaigns.map((campaign) => (
                  <Accordion key={campaign.id}>
                    <AccordionSummary expandIcon={<ExpandMore />}>
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <Box sx={{ flexGrow: 1 }}>
                          <Typography variant="subtitle1">{campaign.name}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {campaign.description}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {campaign.quantumOptimized && (
                            <Chip
                              icon={<Psychology />}
                              label="Quantum Optimized"
                              size="small"
                              color="primary"
                            />
                          )}
                          <Chip
                            label={campaign.isActive ? 'Active' : 'Paused'}
                            color={campaign.isActive ? 'success' : 'default'}
                            size="small"
                          />
                          <Switch
                            checked={campaign.isActive}
                            onChange={() => toggleCampaign(campaign.id)}
                            size="small"
                          />
                        </Box>
                      </Box>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Grid container spacing={2}>
                        <Grid item xs={12} md={6}>
                          <Typography variant="body2" gutterBottom>
                            <strong>Duration:</strong> {campaign.startDate.toLocaleDateString()} - {campaign.endDate.toLocaleDateString()}
                          </Typography>
                          <Typography variant="body2" gutterBottom>
                            <strong>Frequency:</strong> {campaign.frequency}
                          </Typography>
                          <Typography variant="body2" gutterBottom>
                            <strong>Platforms:</strong>
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                            {campaign.platforms.map((platform) => (
                              <Avatar key={platform} sx={{ width: 24, height: 24 }}>
                                {getPlatformIcon(platform)}
                              </Avatar>
                            ))}
                          </Box>
                        </Grid>
                        <Grid item xs={12} md={6}>
                          <Typography variant="body2" gutterBottom>
                            <strong>Scheduled Posts:</strong> {campaign.posts.length}
                          </Typography>
                          <LinearProgress
                            variant="determinate"
                            value={(campaign.posts.filter(p => p.status === 'published').length / Math.max(campaign.posts.length, 1)) * 100}
                            sx={{ mt: 1 }}
                          />
                          <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
                            <Button size="small" startIcon={<Edit />}>
                              Edit
                            </Button>
                            <Button size="small" startIcon={<Analytics />}>
                              Analytics
                            </Button>
                          </Box>
                        </Grid>
                      </Grid>
                    </AccordionDetails>
                  </Accordion>
                ))}
              </CardContent>
            </Card>
          </Grid>

          {/* Quick Actions & Templates */}
          <Grid item xs={12} lg={4}>
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Quick Actions
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Button
                    variant="outlined"
                    startIcon={<AutoAwesome />}
                    onClick={() => generateQuantumContent('quantum computing', 'instagram')}
                  >
                    Generate AI Content
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<TrendingUp />}
                    onClick={handleOptimizePosting}
                  >
                    Optimize Timing
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<CalendarToday />}
                    onClick={() => setTemplateDialog(true)}
                  >
                    Browse Templates
                  </Button>
                </Box>
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Content Templates
                </Typography>
                <List>
                  {templates.slice(0, 3).map((template) => (
                    <React.Fragment key={template.id}>
                      <ListItem>
                        <ListItemText
                          primary={template.name}
                          secondary={template.category}
                        />
                        <ListItemSecondaryAction>
                          <IconButton
                            edge="end"
                            onClick={() => handleUseTemplate(template)}
                          >
                            <PlayArrow />
                          </IconButton>
                        </ListItemSecondaryAction>
                      </ListItem>
                      <Divider />
                    </React.Fragment>
                  ))}
                </List>
                <Button
                  fullWidth
                  variant="text"
                  onClick={() => setTemplateDialog(true)}
                  sx={{ mt: 1 }}
                >
                  View All Templates
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Schedule Post Dialog */}
        <Dialog open={schedulerDialog} onClose={() => setSchedulerDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>Schedule New Post</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={4}
                  label="Post Content"
                  value={newPost.content}
                  onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
                />
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Platforms</InputLabel>
                  <Select
                    multiple
                    value={newPost.platforms}
                    onChange={(e) => setNewPost({ ...newPost, platforms: e.target.value as string[] })}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as string[]).map((value) => (
                          <Chip key={value} label={value} size="small" />
                        ))}
                      </Box>
                    )}
                  >
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
              </Grid>
              
              <Grid item xs={12} md={6}>
                <DateTimePicker
                  label="Schedule Time"
                  value={newPost.scheduledTime}
                  onChange={(newValue) => setNewPost({ ...newPost, scheduledTime: newValue || new Date() })}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Hashtags (comma separated)"
                  value={newPost.hashtags?.join(', ') || ''}
                  onChange={(e) => setNewPost({ 
                    ...newPost, 
                    hashtags: e.target.value.split(',').map(tag => tag.trim()).filter(tag => tag)
                  })}
                />
              </Grid>

              {/* Quantum Optimization Results */}
              {optimizedTimes.length > 0 && (
                <Grid item xs={12}>
                  <Alert severity="info" icon={<Psychology />}>
                    <Typography variant="subtitle2" gutterBottom>
                      Quantum-Optimized Posting Times:
                    </Typography>
                    {optimizedTimes.slice(0, 3).map((time, index) => (
                      <Chip
                        key={index}
                        label={time.toLocaleString()}
                        size="small"
                        sx={{ mr: 1, mb: 1 }}
                        onClick={() => setNewPost({ ...newPost, scheduledTime: time })}
                      />
                    ))}
                  </Alert>
                </Grid>
              )}

              {engagementPrediction && (
                <Grid item xs={12}>
                  <Alert severity="success" icon={<TrendingUp />}>
                    <Typography variant="subtitle2" gutterBottom>
                      Predicted Engagement (Confidence: {(engagementPrediction.confidence * 100).toFixed(1)}%):
                    </Typography>
                    <Typography variant="body2">
                      Likes: {engagementPrediction.expectedLikes} | 
                      Comments: {engagementPrediction.expectedComments} | 
                      Shares: {engagementPrediction.expectedShares} | 
                      Reach: {engagementPrediction.expectedReach}
                    </Typography>
                  </Alert>
                </Grid>
              )}
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSchedulerDialog(false)}>Cancel</Button>
            <Button onClick={handleOptimizePosting} disabled={isOptimizing}>
              {isOptimizing ? 'Optimizing...' : 'Optimize'}
            </Button>
            <Button onClick={handleCreatePost} variant="contained">
              Schedule Post
            </Button>
          </DialogActions>
        </Dialog>

        {/* Campaign Dialog */}
        <Dialog open={campaignDialog} onClose={() => setCampaignDialog(false)} maxWidth="sm" fullWidth>
          <DialogTitle>Create New Campaign</DialogTitle>
          <DialogContent>
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Campaign Name"
                  value={newCampaign.name}
                  onChange={(e) => setNewCampaign({ ...newCampaign, name: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  label="Description"
                  value={newCampaign.description}
                  onChange={(e) => setNewCampaign({ ...newCampaign, description: e.target.value })}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <DateTimePicker
                  label="Start Date"
                  value={newCampaign.startDate}
                  onChange={(newValue) => setNewCampaign({ ...newCampaign, startDate: newValue || new Date() })}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <DateTimePicker
                  label="End Date"
                  value={newCampaign.endDate}
                  onChange={(newValue) => setNewCampaign({ ...newCampaign, endDate: newValue || new Date() })}
                  slotProps={{ textField: { fullWidth: true } }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Frequency</InputLabel>
                  <Select
                    value={newCampaign.frequency}
                    onChange={(e) => setNewCampaign({ ...newCampaign, frequency: e.target.value as any })}
                  >
                    <MenuItem value="daily">Daily</MenuItem>
                    <MenuItem value="weekly">Weekly</MenuItem>
                    <MenuItem value="monthly">Monthly</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={newCampaign.quantumOptimized}
                      onChange={(e) => setNewCampaign({ ...newCampaign, quantumOptimized: e.target.checked })}
                    />
                  }
                  label="Quantum Optimization"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>Platforms</InputLabel>
                  <Select
                    multiple
                    value={newCampaign.platforms}
                    onChange={(e) => setNewCampaign({ ...newCampaign, platforms: e.target.value as string[] })}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as string[]).map((value) => (
                          <Chip key={value} label={value} size="small" />
                        ))}
                      </Box>
                    )}
                  >
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
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setCampaignDialog(false)}>Cancel</Button>
            <Button onClick={handleCreateCampaign} variant="contained">
              Create Campaign
            </Button>
          </DialogActions>
        </Dialog>

        {/* Template Dialog */}
        <Dialog open={templateDialog} onClose={() => setTemplateDialog(false)} maxWidth="md" fullWidth>
          <DialogTitle>Content Templates</DialogTitle>
          <DialogContent>
            <Grid container spacing={2}>
              {templates.map((template) => (
                <Grid item xs={12} md={6} key={template.id}>
                  <Card variant="outlined">
                    <CardContent>
                      <Typography variant="h6" gutterBottom>{template.name}</Typography>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {template.category}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 2 }}>
                        {template.content.substring(0, 100)}...
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                        {template.platforms.map((platform) => (
                          <Avatar key={platform} sx={{ width: 24, height: 24 }}>
                            {getPlatformIcon(platform)}
                          </Avatar>
                        ))}
                      </Box>
                      <Button
                        fullWidth
                        variant="outlined"
                        onClick={() => handleUseTemplate(template)}
                      >
                        Use Template
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setTemplateDialog(false)}>Close</Button>
            <Button variant="contained">
              Create New Template
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </LocalizationProvider>
  );
};

export default ContentScheduler;