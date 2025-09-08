import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  TextField,
  Chip,
  Avatar,
  Rating,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tabs,
  Tab,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Slider,
  Switch,
  FormControlLabel,
  Autocomplete,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Divider,
  IconButton,
  Tooltip,
  Badge,
  LinearProgress,
  Alert,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterIcon,
  Star as StarIcon,
  Download as DownloadIcon,
  ShoppingCart as CartIcon,
  Verified as VerifiedIcon,
  Code as CodeIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
  TrendingUp as TrendingIcon,
  Category as CategoryIcon,
  Person as PersonIcon,
  AttachMoney as MoneyIcon,
  Timeline as TimelineIcon,
  Assessment as AssessmentIcon,
  Favorite as FavoriteIcon,
  Share as ShareIcon,
  Info as InfoIcon,
  Close as CloseIcon,
  Add as AddIcon,
  Edit as EditIcon,
} from '@mui/icons-material';
import { LineChart, Line, AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer } from 'recharts';
import QuantumMarketplaceService, {
  QuantumAlgorithm,
  SearchFilters,
  SearchResult,
  MarketplaceAnalytics,
  Developer,
  Review,
  AlgorithmCategory,
} from '../../services/quantumMarketplaceService';

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
      id={`marketplace-tabpanel-${index}`}
      aria-labelledby={`marketplace-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const QuantumMarketplaceDashboard: React.FC = () => {
  const [marketplaceService] = useState(() => new QuantumMarketplaceService());
  const [activeTab, setActiveTab] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult | null>(null);
  const [filters, setFilters] = useState<SearchFilters>({});
  const [showFilters, setShowFilters] = useState(false);
  const [selectedAlgorithm, setSelectedAlgorithm] = useState<QuantumAlgorithm | null>(null);
  const [showAlgorithmDetails, setShowAlgorithmDetails] = useState(false);
  const [analytics, setAnalytics] = useState<MarketplaceAnalytics | null>(null);
  const [categories, setCategories] = useState<AlgorithmCategory[]>([]);
  const [featuredAlgorithms, setFeaturedAlgorithms] = useState<QuantumAlgorithm[]>([]);
  const [loading, setLoading] = useState(false);
  const [cart, setCart] = useState<string[]>([]);
  const [favorites, setFavorites] = useState<string[]>([]);
  const [showPurchaseDialog, setShowPurchaseDialog] = useState(false);
  const [showReviewDialog, setShowReviewDialog] = useState(false);
  const [newReview, setNewReview] = useState({
    rating: 5,
    title: '',
    content: '',
    pros: [''],
    cons: [''],
  });

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [analyticsData, categoriesData, featuredData] = await Promise.all([
        Promise.resolve(marketplaceService.getMarketplaceAnalytics()),
        Promise.resolve(marketplaceService.getCategories()),
        Promise.resolve(marketplaceService.getFeaturedAlgorithms()),
      ]);

      setAnalytics(analyticsData);
      setCategories(categoriesData);
      setFeaturedAlgorithms(featuredData);

      // Load initial search results
      const initialResults = await marketplaceService.searchAlgorithms('', {}, 1, 12);
      setSearchResults(initialResults);
    } catch (error) {
      console.error('Error loading marketplace data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const results = await marketplaceService.searchAlgorithms(searchQuery, filters, 1, 12);
      setSearchResults(results);
    } catch (error) {
      console.error('Error searching algorithms:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters: Partial<SearchFilters>) => {
    const updatedFilters = { ...filters, ...newFilters };
    setFilters(updatedFilters);
  };

  const handleAlgorithmClick = (algorithm: QuantumAlgorithm) => {
    setSelectedAlgorithm(algorithm);
    setShowAlgorithmDetails(true);
  };

  const handleAddToCart = (algorithmId: string) => {
    if (!cart.includes(algorithmId)) {
      setCart([...cart, algorithmId]);
    }
  };

  const handleToggleFavorite = (algorithmId: string) => {
    if (favorites.includes(algorithmId)) {
      setFavorites(favorites.filter(id => id !== algorithmId));
    } else {
      setFavorites([...favorites, algorithmId]);
    }
  };

  const handlePurchase = async (algorithm: QuantumAlgorithm) => {
    try {
      await marketplaceService.purchaseAlgorithm(algorithm.id, 'user_001', 'credit_card');
      setShowPurchaseDialog(false);
      // Show success message
    } catch (error) {
      console.error('Error purchasing algorithm:', error);
    }
  };

  const handleSubmitReview = async () => {
    if (!selectedAlgorithm) return;

    try {
      await marketplaceService.addReview(selectedAlgorithm.id, {
        userId: 'user_001',
        username: 'Current User',
        rating: newReview.rating,
        title: newReview.title,
        content: newReview.content,
        pros: newReview.pros.filter(p => p.trim()),
        cons: newReview.cons.filter(c => c.trim()),
        helpful: 0,
        verified: true,
      });

      setShowReviewDialog(false);
      setNewReview({
        rating: 5,
        title: '',
        content: '',
        pros: [''],
        cons: [''],
      });
    } catch (error) {
      console.error('Error submitting review:', error);
    }
  };

  const renderOverviewTab = () => (
    <Grid container spacing={3}>
      {/* Hero Section */}
      <Grid item xs={12}>
        <Card sx={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', mb: 3 }}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h3" gutterBottom>
              Quantum Algorithm Marketplace
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9, mb: 3 }}>
              Discover, purchase, and deploy cutting-edge quantum algorithms
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Chip
                icon={<CodeIcon />}
                label={`${analytics?.totalAlgorithms || 0} Algorithms`}
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
              <Chip
                icon={<PersonIcon />}
                label={`${analytics?.totalDevelopers || 0} Developers`}
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
              <Chip
                icon={<DownloadIcon />}
                label={`${analytics?.totalDownloads || 0} Downloads`}
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
            </Box>
          </CardContent>
        </Card>
      </Grid>

      {/* Search Bar */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2, mb: 3 }}>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <TextField
              fullWidth
              placeholder="Search quantum algorithms..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              InputProps={{
                startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
              }}
            />
            <Button
              variant="contained"
              onClick={handleSearch}
              sx={{ minWidth: 120 }}
            >
              Search
            </Button>
            <Button
              variant="outlined"
              startIcon={<FilterIcon />}
              onClick={() => setShowFilters(!showFilters)}
            >
              Filters
            </Button>
          </Box>

          {/* Filters Panel */}
          {showFilters && (
            <Box sx={{ mt: 3, p: 3, bgcolor: 'grey.50', borderRadius: 1 }}>
              <Grid container spacing={3}>
                <Grid item xs={12} md={3}>
                  <FormControl fullWidth>
                    <InputLabel>Category</InputLabel>
                    <Select
                      value={filters.category || ''}
                      onChange={(e) => handleFilterChange({ category: e.target.value })}
                    >
                      <MenuItem value="">All Categories</MenuItem>
                      {categories.map((category) => (
                        <MenuItem key={category.id} value={category.id}>
                          {category.name}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography gutterBottom>Price Range</Typography>
                  <Slider
                    value={[filters.priceRange?.min || 0, filters.priceRange?.max || 1000]}
                    onChange={(_, value) => {
                      const [min, max] = value as number[];
                      handleFilterChange({ priceRange: { min, max } });
                    }}
                    valueLabelDisplay="auto"
                    min={0}
                    max={1000}
                  />
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography gutterBottom>Minimum Rating</Typography>
                  <Rating
                    value={filters.rating || 0}
                    onChange={(_, value) => handleFilterChange({ rating: value || 0 })}
                  />
                </Grid>
                <Grid item xs={12} md={3}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={filters.verified || false}
                        onChange={(e) => handleFilterChange({ verified: e.target.checked })}
                      />
                    }
                    label="Verified Only"
                  />
                </Grid>
              </Grid>
            </Box>
          )}
        </Paper>
      </Grid>

      {/* Featured Algorithms */}
      <Grid item xs={12}>
        <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <StarIcon color="primary" />
          Featured Algorithms
        </Typography>
        <Grid container spacing={2}>
          {featuredAlgorithms.slice(0, 4).map((algorithm) => (
            <Grid item xs={12} sm={6} md={3} key={algorithm.id}>
              <Card sx={{ height: '100%', cursor: 'pointer' }} onClick={() => handleAlgorithmClick(algorithm)}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Typography variant="h6" noWrap>
                      {algorithm.name}
                    </Typography>
                    {algorithm.verified && (
                      <VerifiedIcon color="primary" fontSize="small" />
                    )}
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2, height: 40, overflow: 'hidden' }}>
                    {algorithm.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Rating value={algorithm.rating} readOnly size="small" />
                    <Typography variant="h6" color="primary">
                      ${algorithm.pricing.price}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Grid>

      {/* Search Results */}
      {searchResults && (
        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
            Search Results ({searchResults.total})
          </Typography>
          {loading && <LinearProgress sx={{ mb: 2 }} />}
          <Grid container spacing={2}>
            {searchResults.algorithms.map((algorithm) => (
              <Grid item xs={12} sm={6} md={4} key={algorithm.id}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                      <Typography variant="h6" noWrap>
                        {algorithm.name}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        {algorithm.verified && <VerifiedIcon color="primary" fontSize="small" />}
                        {algorithm.featured && <StarIcon color="warning" fontSize="small" />}
                      </Box>
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2, height: 60, overflow: 'hidden' }}>
                      {algorithm.description}
                    </Typography>
                    
                    <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                      {algorithm.tags.slice(0, 3).map((tag) => (
                        <Chip key={tag} label={tag} size="small" variant="outlined" />
                      ))}
                    </Box>
                    
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                      <Rating value={algorithm.rating} readOnly size="small" />
                      <Typography variant="body2" color="text.secondary">
                        {algorithm.downloads} downloads
                      </Typography>
                    </Box>
                    
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <Typography variant="h6" color="primary">
                        {algorithm.pricing.type === 'free' ? 'Free' : `$${algorithm.pricing.price}`}
                      </Typography>
                      <Box sx={{ display: 'flex', gap: 1 }}>
                        <IconButton
                          size="small"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleToggleFavorite(algorithm.id);
                          }}
                          color={favorites.includes(algorithm.id) ? 'error' : 'default'}
                        >
                          <FavoriteIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                          size="small"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleAddToCart(algorithm.id);
                          }}
                        >
                          <CartIcon fontSize="small" />
                        </IconButton>
                      </Box>
                    </Box>
                  </CardContent>
                  <CardActions>
                    <Button
                      size="small"
                      onClick={() => handleAlgorithmClick(algorithm)}
                    >
                      View Details
                    </Button>
                    <Button
                      size="small"
                      variant="contained"
                      onClick={() => {
                        setSelectedAlgorithm(algorithm);
                        setShowPurchaseDialog(true);
                      }}
                    >
                      {algorithm.pricing.type === 'free' ? 'Download' : 'Purchase'}
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>
      )}
    </Grid>
  );

  const renderAnalyticsTab = () => (
    <Grid container spacing={3}>
      {/* Key Metrics */}
      <Grid item xs={12}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <CodeIcon color="primary" sx={{ fontSize: 40 }} />
                  <Box>
                    <Typography variant="h4">{analytics?.totalAlgorithms || 0}</Typography>
                    <Typography color="text.secondary">Total Algorithms</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <PersonIcon color="primary" sx={{ fontSize: 40 }} />
                  <Box>
                    <Typography variant="h4">{analytics?.totalDevelopers || 0}</Typography>
                    <Typography color="text.secondary">Developers</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <DownloadIcon color="primary" sx={{ fontSize: 40 }} />
                  <Box>
                    <Typography variant="h4">{analytics?.totalDownloads || 0}</Typography>
                    <Typography color="text.secondary">Downloads</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  <MoneyIcon color="primary" sx={{ fontSize: 40 }} />
                  <Box>
                    <Typography variant="h4">${analytics?.totalRevenue || 0}</Typography>
                    <Typography color="text.secondary">Revenue</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Grid>

      {/* Top Categories */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Top Categories
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={analytics?.topCategories || []}
                  dataKey="downloads"
                  nameKey="category"
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  fill="#8884d8"
                  label
                >
                  {(analytics?.topCategories || []).map((_, index) => (
                    <Cell key={`cell-${index}`} fill={`hsl(${index * 45}, 70%, 60%)`} />
                  ))}
                </Pie>
                <RechartsTooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>

      {/* Top Algorithms */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Top Algorithms
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={analytics?.topAlgorithms || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <RechartsTooltip />
                <Bar dataKey="downloads" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>

      {/* Top Developers */}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Top Developers
            </Typography>
            <List>
              {(analytics?.topDevelopers || []).slice(0, 5).map((developer, index) => (
                <React.Fragment key={developer.developerId}>
                  <ListItem>
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'primary.main' }}>
                        {index + 1}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={developer.username}
                      secondary={`${developer.algorithms} algorithms • ${developer.downloads} downloads • ${developer.rating.toFixed(1)} rating`}
                    />
                    <Typography variant="h6" color="primary">
                      ${developer.revenue}
                    </Typography>
                  </ListItem>
                  {index < 4 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );

  const renderCategoriesTab = () => (
    <Grid container spacing={3}>
      {categories.map((category) => {
        const categoryAlgorithms = marketplaceService.getAlgorithmsByCategory(category.id);
        return (
          <Grid item xs={12} sm={6} md={4} key={category.id}>
            <Card sx={{ height: '100%', cursor: 'pointer' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <CategoryIcon color="primary" />
                  <Typography variant="h6">{category.name}</Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {category.description}
                </Typography>
                <Typography variant="body2">
                  {categoryAlgorithms.length} algorithms available
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  size="small"
                  onClick={() => {
                    handleFilterChange({ category: category.id });
                    setActiveTab(0);
                    handleSearch();
                  }}
                >
                  Browse Algorithms
                </Button>
              </CardActions>
            </Card>
          </Grid>
        );
      })}
    </Grid>
  );

  const renderMyLibraryTab = () => (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Alert severity="info">
          This section would show purchased algorithms, favorites, and personal algorithm library.
          In a full implementation, this would connect to user authentication and purchase history.
        </Alert>
      </Grid>
      
      {/* Favorites */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Favorites ({favorites.length})
        </Typography>
        {favorites.length === 0 ? (
          <Typography color="text.secondary">
            No favorites yet. Start exploring algorithms and add them to your favorites!
          </Typography>
        ) : (
          <Grid container spacing={2}>
            {favorites.map((algorithmId) => {
              const algorithm = marketplaceService.getAlgorithm(algorithmId);
              if (!algorithm) return null;
              return (
                <Grid item xs={12} sm={6} md={4} key={algorithmId}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>
                        {algorithm.name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {algorithm.description}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" onClick={() => handleAlgorithmClick(algorithm)}>
                        View Details
                      </Button>
                      <IconButton
                        size="small"
                        onClick={() => handleToggleFavorite(algorithmId)}
                        color="error"
                      >
                        <FavoriteIcon />
                      </IconButton>
                    </CardActions>
                  </Card>
                </Grid>
              );
            })}
          </Grid>
        )}
      </Grid>

      {/* Shopping Cart */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Shopping Cart ({cart.length})
        </Typography>
        {cart.length === 0 ? (
          <Typography color="text.secondary">
            Your cart is empty. Add algorithms to purchase them.
          </Typography>
        ) : (
          <Grid container spacing={2}>
            {cart.map((algorithmId) => {
              const algorithm = marketplaceService.getAlgorithm(algorithmId);
              if (!algorithm) return null;
              return (
                <Grid item xs={12} key={algorithmId}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Box>
                          <Typography variant="h6">{algorithm.name}</Typography>
                          <Typography variant="body2" color="text.secondary">
                            {algorithm.description}
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                          <Typography variant="h6" color="primary">
                            ${algorithm.pricing.price}
                          </Typography>
                          <Button
                            variant="contained"
                            onClick={() => {
                              setSelectedAlgorithm(algorithm);
                              setShowPurchaseDialog(true);
                            }}
                          >
                            Purchase
                          </Button>
                          <IconButton
                            onClick={() => setCart(cart.filter(id => id !== algorithmId))}
                          >
                            <CloseIcon />
                          </IconButton>
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              );
            })}
          </Grid>
        )}
      </Grid>
    </Grid>
  );

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Quantum Algorithm Marketplace
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
          <Tab label="Marketplace" icon={<SearchIcon />} />
          <Tab label="Analytics" icon={<AssessmentIcon />} />
          <Tab label="Categories" icon={<CategoryIcon />} />
          <Tab label="My Library" icon={<PersonIcon />} />
        </Tabs>
      </Box>

      <TabPanel value={activeTab} index={0}>
        {renderOverviewTab()}
      </TabPanel>
      <TabPanel value={activeTab} index={1}>
        {renderAnalyticsTab()}
      </TabPanel>
      <TabPanel value={activeTab} index={2}>
        {renderCategoriesTab()}
      </TabPanel>
      <TabPanel value={activeTab} index={3}>
        {renderMyLibraryTab()}
      </TabPanel>

      {/* Algorithm Details Dialog */}
      <Dialog
        open={showAlgorithmDetails}
        onClose={() => setShowAlgorithmDetails(false)}
        maxWidth="md"
        fullWidth
      >
        {selectedAlgorithm && (
          <>
            <DialogTitle>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="h5">{selectedAlgorithm.name}</Typography>
                  <Typography variant="subtitle1" color="text.secondary">
                    by {selectedAlgorithm.author.displayName}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  {selectedAlgorithm.verified && <VerifiedIcon color="primary" />}
                  {selectedAlgorithm.featured && <StarIcon color="warning" />}
                </Box>
              </Box>
            </DialogTitle>
            <DialogContent>
              <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                  <Typography variant="body1" paragraph>
                    {selectedAlgorithm.description}
                  </Typography>
                  
                  <Typography variant="h6" gutterBottom>
                    Tags
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mb: 3, flexWrap: 'wrap' }}>
                    {selectedAlgorithm.tags.map((tag) => (
                      <Chip key={tag} label={tag} variant="outlined" />
                    ))}
                  </Box>
                  
                  <Typography variant="h6" gutterBottom>
                    Performance Metrics
                  </Typography>
                  <Grid container spacing={2} sx={{ mb: 3 }}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Classical Speedup: {selectedAlgorithm.performance.benchmarks.classicalSpeedup}x
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Quantum Advantage: {selectedAlgorithm.performance.benchmarks.quantumAdvantage}x
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Accuracy: {(selectedAlgorithm.performance.benchmarks.accuracy * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">
                        Qubits Required: {selectedAlgorithm.performance.resourceUsage.qubits}
                      </Typography>
                    </Grid>
                  </Grid>
                  
                  <Typography variant="h6" gutterBottom>
                    Compatibility
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Frameworks: {selectedAlgorithm.compatibility.frameworks.join(', ')}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    Languages: {selectedAlgorithm.compatibility.languages.join(', ')}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography variant="h4" color="primary" gutterBottom>
                        {selectedAlgorithm.pricing.type === 'free' ? 'Free' : `$${selectedAlgorithm.pricing.price}`}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                        <Rating value={selectedAlgorithm.rating} readOnly />
                        <Typography variant="body2" color="text.secondary">
                          ({selectedAlgorithm.reviews.length} reviews)
                        </Typography>
                      </Box>
                      
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        {selectedAlgorithm.downloads} downloads
                      </Typography>
                      
                      <Button
                        fullWidth
                        variant="contained"
                        size="large"
                        sx={{ mb: 2 }}
                        onClick={() => setShowPurchaseDialog(true)}
                      >
                        {selectedAlgorithm.pricing.type === 'free' ? 'Download' : 'Purchase'}
                      </Button>
                      
                      <Button
                        fullWidth
                        variant="outlined"
                        onClick={() => setShowReviewDialog(true)}
                      >
                        Write Review
                      </Button>
                    </CardContent>
                  </Card>
                </Grid>
              </Grid>
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setShowAlgorithmDetails(false)}>Close</Button>
            </DialogActions>
          </>
        )}
      </Dialog>

      {/* Purchase Dialog */}
      <Dialog
        open={showPurchaseDialog}
        onClose={() => setShowPurchaseDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          {selectedAlgorithm?.pricing.type === 'free' ? 'Download Algorithm' : 'Purchase Algorithm'}
        </DialogTitle>
        <DialogContent>
          {selectedAlgorithm && (
            <Box>
              <Typography variant="h6" gutterBottom>
                {selectedAlgorithm.name}
              </Typography>
              <Typography variant="h4" color="primary" gutterBottom>
                {selectedAlgorithm.pricing.type === 'free' ? 'Free' : `$${selectedAlgorithm.pricing.price}`}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {selectedAlgorithm.description}
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowPurchaseDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={() => selectedAlgorithm && handlePurchase(selectedAlgorithm)}
          >
            {selectedAlgorithm?.pricing.type === 'free' ? 'Download' : 'Purchase'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Review Dialog */}
      <Dialog
        open={showReviewDialog}
        onClose={() => setShowReviewDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Write a Review</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <Typography gutterBottom>Rating</Typography>
            <Rating
              value={newReview.rating}
              onChange={(_, value) => setNewReview({ ...newReview, rating: value || 5 })}
              sx={{ mb: 3 }}
            />
            
            <TextField
              fullWidth
              label="Review Title"
              value={newReview.title}
              onChange={(e) => setNewReview({ ...newReview, title: e.target.value })}
              sx={{ mb: 3 }}
            />
            
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Review Content"
              value={newReview.content}
              onChange={(e) => setNewReview({ ...newReview, content: e.target.value })}
              sx={{ mb: 3 }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowReviewDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleSubmitReview}>
            Submit Review
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default QuantumMarketplaceDashboard;