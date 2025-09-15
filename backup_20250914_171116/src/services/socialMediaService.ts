import axios from 'axios';

interface SocialPlatformConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  scopes: string[];
}

interface SocialAccount {
  id: string;
  platform: 'instagram' | 'facebook' | 'twitter' | 'linkedin' | 'youtube' | 'tiktok';
  username: string;
  displayName: string;
  followers: number;
  isConnected: boolean;
  accessToken?: string;
  refreshToken?: string;
  expiresAt?: Date;
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

interface PostCreationData {
  content: string;
  platforms: string[];
  scheduledTime?: Date;
  media?: File[];
  hashtags?: string[];
}

interface AnalyticsData {
  platform: string;
  followers: number;
  engagement: number;
  reach: number;
  impressions: number;
  growth: number;
  period: 'day' | 'week' | 'month';
}

class SocialMediaService {
  private baseURL = process.env.REACT_APP_API_URL || 'http://localhost:3001';
  private platforms: Record<string, SocialPlatformConfig> = {
    instagram: {
      clientId: process.env.REACT_APP_INSTAGRAM_CLIENT_ID || '',
      clientSecret: process.env.REACT_APP_INSTAGRAM_CLIENT_SECRET || '',
      redirectUri: `${window.location.origin}/auth/instagram/callback`,
      scopes: ['user_profile', 'user_media', 'instagram_basic', 'instagram_content_publish']
    },
    facebook: {
      clientId: process.env.REACT_APP_FACEBOOK_CLIENT_ID || '',
      clientSecret: process.env.REACT_APP_FACEBOOK_CLIENT_SECRET || '',
      redirectUri: `${window.location.origin}/auth/facebook/callback`,
      scopes: ['pages_manage_posts', 'pages_read_engagement', 'pages_show_list', 'publish_to_groups']
    },
    twitter: {
      clientId: process.env.REACT_APP_TWITTER_CLIENT_ID || '',
      clientSecret: process.env.REACT_APP_TWITTER_CLIENT_SECRET || '',
      redirectUri: `${window.location.origin}/auth/twitter/callback`,
      scopes: ['tweet.read', 'tweet.write', 'users.read', 'follows.read']
    },
    linkedin: {
      clientId: process.env.REACT_APP_LINKEDIN_CLIENT_ID || '',
      clientSecret: process.env.REACT_APP_LINKEDIN_CLIENT_SECRET || '',
      redirectUri: `${window.location.origin}/auth/linkedin/callback`,
      scopes: ['r_liteprofile', 'r_emailaddress', 'w_member_social', 'r_organization_social']
    },
    youtube: {
      clientId: process.env.REACT_APP_YOUTUBE_CLIENT_ID || '',
      clientSecret: process.env.REACT_APP_YOUTUBE_CLIENT_SECRET || '',
      redirectUri: `${window.location.origin}/auth/youtube/callback`,
      scopes: ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']
    },
    tiktok: {
      clientId: process.env.REACT_APP_TIKTOK_CLIENT_ID || '',
      clientSecret: process.env.REACT_APP_TIKTOK_CLIENT_SECRET || '',
      redirectUri: `${window.location.origin}/auth/tiktok/callback`,
      scopes: ['user.info.basic', 'video.list', 'video.upload']
    }
  };

  // OAuth Authentication
  async initiateOAuth(platform: string): Promise<string> {
    const config = this.platforms[platform];
    if (!config) {
      throw new Error(`Platform ${platform} not supported`);
    }

    const authUrl = this.buildAuthUrl(platform, config);
    return authUrl;
  }

  private buildAuthUrl(platform: string, config: SocialPlatformConfig): string {
    const state = this.generateState();
    localStorage.setItem(`oauth_state_${platform}`, state);

    switch (platform) {
      case 'instagram':
      case 'facebook':
        return `https://www.facebook.com/v18.0/dialog/oauth?` +
          `client_id=${config.clientId}&` +
          `redirect_uri=${encodeURIComponent(config.redirectUri)}&` +
          `scope=${config.scopes.join(',')}&` +
          `response_type=code&` +
          `state=${state}`;
      
      case 'twitter':
        return `https://twitter.com/i/oauth2/authorize?` +
          `response_type=code&` +
          `client_id=${config.clientId}&` +
          `redirect_uri=${encodeURIComponent(config.redirectUri)}&` +
          `scope=${encodeURIComponent(config.scopes.join(' '))}&` +
          `state=${state}&` +
          `code_challenge=challenge&` +
          `code_challenge_method=plain`;
      
      case 'linkedin':
        return `https://www.linkedin.com/oauth/v2/authorization?` +
          `response_type=code&` +
          `client_id=${config.clientId}&` +
          `redirect_uri=${encodeURIComponent(config.redirectUri)}&` +
          `scope=${encodeURIComponent(config.scopes.join(' '))}&` +
          `state=${state}`;
      
      case 'youtube':
        return `https://accounts.google.com/o/oauth2/v2/auth?` +
          `response_type=code&` +
          `client_id=${config.clientId}&` +
          `redirect_uri=${encodeURIComponent(config.redirectUri)}&` +
          `scope=${encodeURIComponent(config.scopes.join(' '))}&` +
          `access_type=offline&` +
          `state=${state}`;
      
      case 'tiktok':
        return `https://www.tiktok.com/auth/authorize/?` +
          `client_key=${config.clientId}&` +
          `scope=${config.scopes.join(',')}&` +
          `response_type=code&` +
          `redirect_uri=${encodeURIComponent(config.redirectUri)}&` +
          `state=${state}`;
      
      default:
        throw new Error(`OAuth URL building not implemented for ${platform}`);
    }
  }

  private generateState(): string {
    return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
  }

  // Handle OAuth callback
  async handleOAuthCallback(platform: string, code: string, state: string): Promise<SocialAccount> {
    const storedState = localStorage.getItem(`oauth_state_${platform}`);
    if (storedState !== state) {
      throw new Error('Invalid OAuth state');
    }

    try {
      const response = await axios.post(`${this.baseURL}/api/social/oauth/callback`, {
        platform,
        code,
        state
      });

      const account: SocialAccount = response.data;
      this.storeAccountTokens(account);
      return account;
    } catch (error) {
      console.error('OAuth callback error:', error);
      throw new Error('Failed to complete OAuth authentication');
    }
  }

  private storeAccountTokens(account: SocialAccount): void {
    if (account.accessToken) {
      localStorage.setItem(`${account.platform}_access_token`, account.accessToken);
    }
    if (account.refreshToken) {
      localStorage.setItem(`${account.platform}_refresh_token`, account.refreshToken);
    }
    if (account.expiresAt) {
      localStorage.setItem(`${account.platform}_expires_at`, account.expiresAt.toISOString());
    }
  }

  // Account Management
  async getConnectedAccounts(): Promise<SocialAccount[]> {
    try {
      const response = await axios.get(`${this.baseURL}/api/social/accounts`);
      return response.data;
    } catch (error) {
      console.error('Error fetching accounts:', error);
      return [];
    }
  }

  async disconnectAccount(accountId: string): Promise<void> {
    try {
      await axios.delete(`${this.baseURL}/api/social/accounts/${accountId}`);
      // Clear stored tokens
      const account = await this.getAccountById(accountId);
      if (account) {
        localStorage.removeItem(`${account.platform}_access_token`);
        localStorage.removeItem(`${account.platform}_refresh_token`);
        localStorage.removeItem(`${account.platform}_expires_at`);
      }
    } catch (error) {
      console.error('Error disconnecting account:', error);
      throw error;
    }
  }

  async getAccountById(accountId: string): Promise<SocialAccount | null> {
    try {
      const response = await axios.get(`${this.baseURL}/api/social/accounts/${accountId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching account:', error);
      return null;
    }
  }

  // Post Management
  async createPost(postData: PostCreationData): Promise<SocialPost[]> {
    try {
      const formData = new FormData();
      formData.append('content', postData.content);
      formData.append('platforms', JSON.stringify(postData.platforms));
      
      if (postData.scheduledTime) {
        formData.append('scheduledTime', postData.scheduledTime.toISOString());
      }
      
      if (postData.hashtags) {
        formData.append('hashtags', JSON.stringify(postData.hashtags));
      }
      
      if (postData.media) {
        postData.media.forEach((file, index) => {
          formData.append(`media_${index}`, file);
        });
      }

      const response = await axios.post(`${this.baseURL}/api/social/posts`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      return response.data;
    } catch (error) {
      console.error('Error creating post:', error);
      throw error;
    }
  }

  async getPosts(filters?: {
    platform?: string;
    status?: string;
    dateFrom?: Date;
    dateTo?: Date;
  }): Promise<SocialPost[]> {
    try {
      const params = new URLSearchParams();
      if (filters?.platform) params.append('platform', filters.platform);
      if (filters?.status) params.append('status', filters.status);
      if (filters?.dateFrom) params.append('dateFrom', filters.dateFrom.toISOString());
      if (filters?.dateTo) params.append('dateTo', filters.dateTo.toISOString());

      const response = await axios.get(`${this.baseURL}/api/social/posts?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching posts:', error);
      return [];
    }
  }

  async updatePost(postId: string, updates: Partial<SocialPost>): Promise<SocialPost> {
    try {
      const response = await axios.put(`${this.baseURL}/api/social/posts/${postId}`, updates);
      return response.data;
    } catch (error) {
      console.error('Error updating post:', error);
      throw error;
    }
  }

  async deletePost(postId: string): Promise<void> {
    try {
      await axios.delete(`${this.baseURL}/api/social/posts/${postId}`);
    } catch (error) {
      console.error('Error deleting post:', error);
      throw error;
    }
  }

  async publishScheduledPost(postId: string): Promise<SocialPost> {
    try {
      const response = await axios.post(`${this.baseURL}/api/social/posts/${postId}/publish`);
      return response.data;
    } catch (error) {
      console.error('Error publishing post:', error);
      throw error;
    }
  }

  // Analytics
  async getAnalytics(platform?: string, period: 'day' | 'week' | 'month' = 'month'): Promise<AnalyticsData[]> {
    try {
      const params = new URLSearchParams();
      if (platform) params.append('platform', platform);
      params.append('period', period);

      const response = await axios.get(`${this.baseURL}/api/social/analytics?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching analytics:', error);
      return [];
    }
  }

  async getPostAnalytics(postId: string): Promise<SocialPost> {
    try {
      const response = await axios.get(`${this.baseURL}/api/social/posts/${postId}/analytics`);
      return response.data;
    } catch (error) {
      console.error('Error fetching post analytics:', error);
      throw error;
    }
  }

  // Content Suggestions
  async getContentSuggestions(platform: string, topic?: string): Promise<string[]> {
    try {
      const params = new URLSearchParams();
      params.append('platform', platform);
      if (topic) params.append('topic', topic);

      const response = await axios.get(`${this.baseURL}/api/social/content/suggestions?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching content suggestions:', error);
      return [];
    }
  }

  async generateHashtags(content: string, platform: string): Promise<string[]> {
    try {
      const response = await axios.post(`${this.baseURL}/api/social/content/hashtags`, {
        content,
        platform
      });
      return response.data;
    } catch (error) {
      console.error('Error generating hashtags:', error);
      return [];
    }
  }

  // Quantum-Enhanced Features
  async optimizePostTiming(platform: string, content: string): Promise<Date[]> {
    try {
      const response = await axios.post(`${this.baseURL}/api/social/quantum/optimize-timing`, {
        platform,
        content
      });
      return response.data.map((time: string) => new Date(time));
    } catch (error) {
      console.error('Error optimizing post timing:', error);
      return [];
    }
  }

  async predictEngagement(platform: string, content: string, scheduledTime: Date): Promise<{
    expectedLikes: number;
    expectedComments: number;
    expectedShares: number;
    expectedReach: number;
    confidence: number;
  }> {
    try {
      const response = await axios.post(`${this.baseURL}/api/social/quantum/predict-engagement`, {
        platform,
        content,
        scheduledTime: scheduledTime.toISOString()
      });
      return response.data;
    } catch (error) {
      console.error('Error predicting engagement:', error);
      return {
        expectedLikes: 0,
        expectedComments: 0,
        expectedShares: 0,
        expectedReach: 0,
        confidence: 0
      };
    }
  }

  async generateQuantumContent(topic: string, platform: string, tone: 'professional' | 'casual' | 'humorous' = 'professional'): Promise<string> {
    try {
      const response = await axios.post(`${this.baseURL}/api/social/quantum/generate-content`, {
        topic,
        platform,
        tone
      });
      return response.data.content;
    } catch (error) {
      console.error('Error generating quantum content:', error);
      return '';
    }
  }

  // Utility Methods
  isTokenExpired(platform: string): boolean {
    const expiresAt = localStorage.getItem(`${platform}_expires_at`);
    if (!expiresAt) return true;
    
    return new Date(expiresAt) <= new Date();
  }

  async refreshAccessToken(platform: string): Promise<string | null> {
    const refreshToken = localStorage.getItem(`${platform}_refresh_token`);
    if (!refreshToken) return null;

    try {
      const response = await axios.post(`${this.baseURL}/api/social/oauth/refresh`, {
        platform,
        refreshToken
      });

      const { accessToken, expiresAt } = response.data;
      localStorage.setItem(`${platform}_access_token`, accessToken);
      localStorage.setItem(`${platform}_expires_at`, expiresAt);
      
      return accessToken;
    } catch (error) {
      console.error('Error refreshing token:', error);
      return null;
    }
  }

  formatNumber(num: number): string {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  }

  getPlatformLimits(platform: string): {
    maxTextLength: number;
    maxImages: number;
    maxVideos: number;
    supportedFormats: string[];
  } {
    const limits = {
      instagram: {
        maxTextLength: 2200,
        maxImages: 10,
        maxVideos: 1,
        supportedFormats: ['jpg', 'jpeg', 'png', 'mp4', 'mov']
      },
      facebook: {
        maxTextLength: 63206,
        maxImages: 10,
        maxVideos: 1,
        supportedFormats: ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi']
      },
      twitter: {
        maxTextLength: 280,
        maxImages: 4,
        maxVideos: 1,
        supportedFormats: ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov']
      },
      linkedin: {
        maxTextLength: 3000,
        maxImages: 9,
        maxVideos: 1,
        supportedFormats: ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov']
      },
      youtube: {
        maxTextLength: 5000,
        maxImages: 1,
        maxVideos: 1,
        supportedFormats: ['mp4', 'mov', 'avi', 'wmv', 'flv', 'webm']
      },
      tiktok: {
        maxTextLength: 150,
        maxImages: 0,
        maxVideos: 1,
        supportedFormats: ['mp4', 'mov']
      }
    };

    return limits[platform as keyof typeof limits] || {
      maxTextLength: 1000,
      maxImages: 1,
      maxVideos: 1,
      supportedFormats: ['jpg', 'jpeg', 'png', 'mp4']
    };
  }
}

export default new SocialMediaService();
export type { SocialAccount, SocialPost, PostCreationData, AnalyticsData };