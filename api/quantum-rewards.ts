// Next.js API Routes for Quantum High Council Reward System
// This file contains all the backend endpoints for tracking rewards, referrals, and user progress

import { NextApiRequest, NextApiResponse } from 'next';

// Types
interface User {
  id: string;
  email: string;
  username: string;
  joinedAt: Date;
  quantumCredits: number;
  tier: 'genesis' | 'entangled' | 'nexus' | 'founder';
  referralCode: string;
  referredBy?: string;
  lastCheckIn?: Date;
  achievements: string[];
  glyphsUnlocked: string[];
  totalReferrals: number;
  isFounder: boolean;
}

interface RewardAction {
  id: string;
  userId: string;
  action: 'daily_checkin' | 'social_share' | 'friend_invite' | 'glyph_unlock' | 'milestone_reach';
  credits: number;
  timestamp: Date;
  metadata?: any;
}

interface ReferralReward {
  id: string;
  referrerId: string;
  refereeId: string;
  credits: number;
  tier: string;
  timestamp: Date;
}

// Mock database - Replace with your actual database
class QuantumDatabase {
  private users: Map<string, User> = new Map();
  private rewards: RewardAction[] = [];
  private referrals: ReferralReward[] = [];
  private cooldowns: Map<string, Date> = new Map();

  // User management
  async createUser(userData: Partial<User>): Promise<User> {
    const user: User = {
      id: userData.id || this.generateId(),
      email: userData.email || '',
      username: userData.username || '',
      joinedAt: new Date(),
      quantumCredits: 100, // Starting credits
      tier: 'genesis',
      referralCode: this.generateReferralCode(),
      achievements: [],
      glyphsUnlocked: [],
      totalReferrals: 0,
      isFounder: false,
      ...userData
    };
    
    this.users.set(user.id, user);
    return user;
  }

  async getUser(userId: string): Promise<User | null> {
    return this.users.get(userId) || null;
  }

  async updateUser(userId: string, updates: Partial<User>): Promise<User | null> {
    const user = this.users.get(userId);
    if (!user) return null;
    
    const updatedUser = { ...user, ...updates };
    this.users.set(userId, updatedUser);
    return updatedUser;
  }

  async getUserByReferralCode(code: string): Promise<User | null> {
    for (const user of this.users.values()) {
      if (user.referralCode === code) return user;
    }
    return null;
  }

  // Reward management
  async addReward(reward: Omit<RewardAction, 'id' | 'timestamp'>): Promise<RewardAction> {
    const newReward: RewardAction = {
      ...reward,
      id: this.generateId(),
      timestamp: new Date()
    };
    
    this.rewards.push(newReward);
    
    // Update user credits
    const user = await this.getUser(reward.userId);
    if (user) {
      await this.updateUser(user.id, {
        quantumCredits: user.quantumCredits + reward.credits
      });
    }
    
    return newReward;
  }

  async getUserRewards(userId: string): Promise<RewardAction[]> {
    return this.rewards.filter(r => r.userId === userId);
  }

  // Referral management
  async createReferral(referrerId: string, refereeId: string): Promise<ReferralReward | null> {
    const referrer = await this.getUser(referrerId);
    const referee = await this.getUser(refereeId);
    
    if (!referrer || !referee) return null;
    
    // Calculate referral rewards based on tier
    const baseReward = 50;
    const tierMultiplier = {
      genesis: 1,
      entangled: 1.5,
      nexus: 2,
      founder: 3
    };
    
    const credits = Math.floor(baseReward * tierMultiplier[referrer.tier]);
    
    const referral: ReferralReward = {
      id: this.generateId(),
      referrerId,
      refereeId,
      credits,
      tier: referrer.tier,
      timestamp: new Date()
    };
    
    this.referrals.push(referral);
    
    // Update referrer
    await this.updateUser(referrerId, {
      quantumCredits: referrer.quantumCredits + credits,
      totalReferrals: referrer.totalReferrals + 1
    });
    
    // Check for founder status (5+ referrals)
    if (referrer.totalReferrals + 1 >= 5) {
      await this.updateUser(referrerId, {
        isFounder: true,
        tier: 'founder'
      });
    }
    
    return referral;
  }

  // Cooldown management
  async checkCooldown(userId: string, action: string): Promise<boolean> {
    const key = `${userId}:${action}`;
    const lastAction = this.cooldowns.get(key);
    
    if (!lastAction) return true;
    
    const now = new Date();
    const cooldownPeriod = this.getCooldownPeriod(action);
    
    return (now.getTime() - lastAction.getTime()) >= cooldownPeriod;
  }

  async setCooldown(userId: string, action: string): Promise<void> {
    const key = `${userId}:${action}`;
    this.cooldowns.set(key, new Date());
  }

  private getCooldownPeriod(action: string): number {
    const periods = {
      daily_checkin: 24 * 60 * 60 * 1000, // 24 hours
      social_share: 60 * 60 * 1000, // 1 hour
      friend_invite: 5 * 60 * 1000, // 5 minutes
    };
    return periods[action as keyof typeof periods] || 0;
  }

  private generateId(): string {
    return Math.random().toString(36).substr(2, 9);
  }

  private generateReferralCode(): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = 'QHC';
    for (let i = 0; i < 5; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }

  // Leaderboard
  async getLeaderboard(limit: number = 10): Promise<User[]> {
    return Array.from(this.users.values())
      .sort((a, b) => b.quantumCredits - a.quantumCredits)
      .slice(0, limit);
  }
}

// Initialize database
const db = new QuantumDatabase();

// API Handlers
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { method, query } = req;
  const endpoint = query.endpoint as string;

  try {
    switch (method) {
      case 'GET':
        return await handleGet(req, res, endpoint);
      case 'POST':
        return await handlePost(req, res, endpoint);
      case 'PUT':
        return await handlePut(req, res, endpoint);
      default:
        return res.status(405).json({ error: 'Method not allowed' });
    }
  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}

async function handleGet(req: NextApiRequest, res: NextApiResponse, endpoint: string) {
  const { userId, referralCode } = req.query;

  switch (endpoint) {
    case 'user':
      if (!userId) return res.status(400).json({ error: 'User ID required' });
      const user = await db.getUser(userId as string);
      if (!user) return res.status(404).json({ error: 'User not found' });
      return res.json(user);

    case 'rewards':
      if (!userId) return res.status(400).json({ error: 'User ID required' });
      const rewards = await db.getUserRewards(userId as string);
      return res.json(rewards);

    case 'leaderboard':
      const leaderboard = await db.getLeaderboard();
      return res.json(leaderboard);

    case 'referral-user':
      if (!referralCode) return res.status(400).json({ error: 'Referral code required' });
      const referrer = await db.getUserByReferralCode(referralCode as string);
      if (!referrer) return res.status(404).json({ error: 'Invalid referral code' });
      return res.json({ username: referrer.username, tier: referrer.tier });

    default:
      return res.status(404).json({ error: 'Endpoint not found' });
  }
}

async function handlePost(req: NextApiRequest, res: NextApiResponse, endpoint: string) {
  const { body } = req;

  switch (endpoint) {
    case 'user':
      const newUser = await db.createUser(body);
      return res.status(201).json(newUser);

    case 'daily-checkin':
      const { userId } = body;
      if (!userId) return res.status(400).json({ error: 'User ID required' });
      
      const canCheckIn = await db.checkCooldown(userId, 'daily_checkin');
      if (!canCheckIn) {
        return res.status(429).json({ error: 'Already checked in today' });
      }
      
      const checkInReward = await db.addReward({
        userId,
        action: 'daily_checkin',
        credits: 10
      });
      
      await db.setCooldown(userId, 'daily_checkin');
      return res.json(checkInReward);

    case 'social-share':
      const { userId: shareUserId, platform } = body;
      if (!shareUserId) return res.status(400).json({ error: 'User ID required' });
      
      const canShare = await db.checkCooldown(shareUserId, 'social_share');
      if (!canShare) {
        return res.status(429).json({ error: 'Share cooldown active' });
      }
      
      const shareReward = await db.addReward({
        userId: shareUserId,
        action: 'social_share',
        credits: 5,
        metadata: { platform }
      });
      
      await db.setCooldown(shareUserId, 'social_share');
      return res.json(shareReward);

    case 'referral':
      const { referrerId, refereeId } = body;
      if (!referrerId || !refereeId) {
        return res.status(400).json({ error: 'Referrer and referee IDs required' });
      }
      
      const referral = await db.createReferral(referrerId, refereeId);
      if (!referral) {
        return res.status(400).json({ error: 'Invalid referral' });
      }
      
      return res.json(referral);

    case 'glyph-unlock':
      const { userId: glyphUserId, glyphId } = body;
      if (!glyphUserId || !glyphId) {
        return res.status(400).json({ error: 'User ID and glyph ID required' });
      }
      
      const user = await db.getUser(glyphUserId);
      if (!user) return res.status(404).json({ error: 'User not found' });
      
      if (user.glyphsUnlocked.includes(glyphId)) {
        return res.status(400).json({ error: 'Glyph already unlocked' });
      }
      
      const glyphReward = await db.addReward({
        userId: glyphUserId,
        action: 'glyph_unlock',
        credits: 25,
        metadata: { glyphId }
      });
      
      await db.updateUser(glyphUserId, {
        glyphsUnlocked: [...user.glyphsUnlocked, glyphId]
      });
      
      return res.json(glyphReward);

    default:
      return res.status(404).json({ error: 'Endpoint not found' });
  }
}

async function handlePut(req: NextApiRequest, res: NextApiResponse, endpoint: string) {
  const { body } = req;

  switch (endpoint) {
    case 'user':
      const { userId, ...updates } = body;
      if (!userId) return res.status(400).json({ error: 'User ID required' });
      
      const updatedUser = await db.updateUser(userId, updates);
      if (!updatedUser) return res.status(404).json({ error: 'User not found' });
      
      return res.json(updatedUser);

    default:
      return res.status(404).json({ error: 'Endpoint not found' });
  }
}

// Utility functions for client-side usage
export const QuantumRewardsAPI = {
  // User management
  async createUser(userData: Partial<User>) {
    const response = await fetch('/api/quantum-rewards?endpoint=user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return response.json();
  },

  async getUser(userId: string) {
    const response = await fetch(`/api/quantum-rewards?endpoint=user&userId=${userId}`);
    return response.json();
  },

  async updateUser(userId: string, updates: Partial<User>) {
    const response = await fetch('/api/quantum-rewards?endpoint=user', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, ...updates })
    });
    return response.json();
  },

  // Rewards
  async dailyCheckIn(userId: string) {
    const response = await fetch('/api/quantum-rewards?endpoint=daily-checkin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId })
    });
    return response.json();
  },

  async socialShare(userId: string, platform: string) {
    const response = await fetch('/api/quantum-rewards?endpoint=social-share', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, platform })
    });
    return response.json();
  },

  async unlockGlyph(userId: string, glyphId: string) {
    const response = await fetch('/api/quantum-rewards?endpoint=glyph-unlock', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, glyphId })
    });
    return response.json();
  },

  // Referrals
  async createReferral(referrerId: string, refereeId: string) {
    const response = await fetch('/api/quantum-rewards?endpoint=referral', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ referrerId, refereeId })
    });
    return response.json();
  },

  async getReferralUser(referralCode: string) {
    const response = await fetch(`/api/quantum-rewards?endpoint=referral-user&referralCode=${referralCode}`);
    return response.json();
  },

  // Leaderboard
  async getLeaderboard() {
    const response = await fetch('/api/quantum-rewards?endpoint=leaderboard');
    return response.json();
  },

  // User rewards
  async getUserRewards(userId: string) {
    const response = await fetch(`/api/quantum-rewards?endpoint=rewards&userId=${userId}`);
    return response.json();
  }
};

// Export types for client-side usage
export type { User, RewardAction, ReferralReward };