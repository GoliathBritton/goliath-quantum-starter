import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { QRCodeSVG } from 'qrcode.react';

interface ReferralData {
  referralCode: string;
  totalReferrals: number;
  activeReferrals: number;
  quantumCreditsEarned: number;
  founderStatus: boolean;
  referralLink: string;
  leaderboardRank: number;
  achievements: Achievement[];
}

interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  unlocked: boolean;
  unlockedAt?: Date;
  reward: string;
}

interface ReferralSystemProps {
  userId: string;
  onReferralUpdate: (data: ReferralData) => void;
  daysUntilLaunch: number;
}

const ACHIEVEMENTS: Achievement[] = [
  {
    id: 'first_referral',
    name: 'Quantum Catalyst',
    description: 'Make your first referral',
    icon: '⚡',
    unlocked: false,
    reward: '+50 Quantum Credits'
  },
  {
    id: 'five_referrals',
    name: 'Entanglement Master',
    description: 'Refer 5 quantum pioneers',
    icon: '🌌',
    unlocked: false,
    reward: 'QHC Founder Status + 250 QC'
  },
  {
    id: 'ten_referrals',
    name: 'Nexus Architect',
    description: 'Build a network of 10 members',
    icon: '🏗️',
    unlocked: false,
    reward: 'Lifetime Premium + 500 QC'
  },
  {
    id: 'twenty_referrals',
    name: 'Quantum Overlord',
    description: 'Command 20 quantum agents',
    icon: '👑',
    unlocked: false,
    reward: 'Exclusive Council Seat + 1000 QC'
  },
  {
    id: 'social_amplifier',
    name: 'Reality Broadcaster',
    description: 'Share on 3 social platforms',
    icon: '📡',
    unlocked: false,
    reward: '+100 Quantum Credits'
  },
  {
    id: 'speed_demon',
    name: 'Quantum Velocity',
    description: 'Get 3 referrals in 24 hours',
    icon: '⚡',
    unlocked: false,
    reward: 'Speed Bonus + 200 QC'
  }
];

const FOUNDER_BENEFITS = [
  'Lifetime 50% discount on all premium features',
  'Exclusive access to Quantum High Council events',
  'Priority customer support with dedicated quantum specialist',
  'Early access to all new AI agents and features',
  'Custom quantum signature and profile badge',
  'Invitation to annual Quantum Nexus summit',
  'Access to founder-only Discord channels',
  'Quarterly strategy calls with the development team'
];

export const ReferralSystem: React.FC<ReferralSystemProps> = ({
  userId,
  onReferralUpdate,
  daysUntilLaunch
}) => {
  const [referralData, setReferralData] = useState<ReferralData>({
    referralCode: '',
    totalReferrals: 0,
    activeReferrals: 0,
    quantumCreditsEarned: 0,
    founderStatus: false,
    referralLink: '',
    leaderboardRank: 0,
    achievements: ACHIEVEMENTS
  });
  
  const [showQRCode, setShowQRCode] = useState(false);
  const [showFounderBenefits, setShowFounderBenefits] = useState(false);
  const [copiedLink, setCopiedLink] = useState(false);
  const [selectedAchievement, setSelectedAchievement] = useState<string | null>(null);
  const [leaderboard, setLeaderboard] = useState<any[]>([]);

  useEffect(() => {
    // Generate referral code and link
    const code = generateReferralCode(userId);
    const link = `https://quantum-nexus.ai/join?ref=${code}`;
    
    setReferralData(prev => ({
      ...prev,
      referralCode: code,
      referralLink: link
    }));

    // Load referral data from localStorage or API
    loadReferralData();
    loadLeaderboard();
  }, [userId]);

  useEffect(() => {
    // Check for founder status (5+ referrals)
    if (referralData.totalReferrals >= 5 && !referralData.founderStatus) {
      setReferralData(prev => ({ ...prev, founderStatus: true }));
      unlockAchievement('five_referrals');
    }
  }, [referralData.totalReferrals]);

  const generateReferralCode = (userId: string): string => {
    // Generate a unique referral code based on user ID
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = 'QHC';
    for (let i = 0; i < 5; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  };

  const loadReferralData = () => {
    // Simulate loading from API/localStorage
    const saved = localStorage.getItem(`referralData_${userId}`);
    if (saved) {
      const data = JSON.parse(saved);
      setReferralData(prev => ({ ...prev, ...data }));
    }
  };

  const loadLeaderboard = () => {
    // Simulate leaderboard data
    const mockLeaderboard = [
      { rank: 1, name: 'QuantumMaster', referrals: 47, credits: 4700, avatar: '🚀' },
      { rank: 2, name: 'NexusBuilder', referrals: 32, credits: 3200, avatar: '⚡' },
      { rank: 3, name: 'CosmicCoder', referrals: 28, credits: 2800, avatar: '🌌' },
      { rank: 4, name: 'You', referrals: referralData.totalReferrals, credits: referralData.quantumCreditsEarned, avatar: '👤' },
      { rank: 5, name: 'DigitalShaman', referrals: 19, credits: 1900, avatar: '🔮' }
    ];
    setLeaderboard(mockLeaderboard);
  };

  const copyReferralLink = async () => {
    try {
      await navigator.clipboard.writeText(referralData.referralLink);
      setCopiedLink(true);
      setTimeout(() => setCopiedLink(false), 2000);
    } catch (err) {
      console.error('Failed to copy link:', err);
    }
  };

  const shareOnSocial = (platform: string) => {
    const text = encodeURIComponent(
      `🚀 Join me in the Quantum High Council! Experience the future of AI agents and quantum computing. Use my exclusive invite link to get started with bonus credits! #QuantumNexus #AI #Future`
    );
    const url = encodeURIComponent(referralData.referralLink);
    
    let shareUrl = '';
    switch (platform) {
      case 'twitter':
        shareUrl = `https://twitter.com/intent/tweet?text=${text}&url=${url}`;
        break;
      case 'linkedin':
        shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
        break;
      case 'facebook':
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
        break;
    }
    
    if (shareUrl) {
      window.open(shareUrl, '_blank', 'width=600,height=400');
      // Track social share for achievements
      trackSocialShare(platform);
    }
  };

  const trackSocialShare = (platform: string) => {
    const shares = JSON.parse(localStorage.getItem('socialShares') || '[]');
    if (!shares.includes(platform)) {
      shares.push(platform);
      localStorage.setItem('socialShares', JSON.stringify(shares));
      
      if (shares.length >= 3) {
        unlockAchievement('social_amplifier');
      }
    }
  };

  const unlockAchievement = (achievementId: string) => {
    setReferralData(prev => ({
      ...prev,
      achievements: prev.achievements.map(achievement => 
        achievement.id === achievementId 
          ? { ...achievement, unlocked: true, unlockedAt: new Date() }
          : achievement
      )
    }));
    
    // Show achievement notification
    const achievement = ACHIEVEMENTS.find(a => a.id === achievementId);
    if (achievement) {
      // You could add a toast notification here
      console.log(`Achievement unlocked: ${achievement.name}!`);
    }
  };

  const getProgressToFounder = () => {
    const needed = Math.max(0, 5 - referralData.totalReferrals);
    return {
      current: referralData.totalReferrals,
      needed,
      percentage: Math.min(100, (referralData.totalReferrals / 5) * 100)
    };
  };

  const founderProgress = getProgressToFounder();

  return (
    <div className="referral-system">
      <div className="referral-header">
        <div className="header-content">
          <h2 className="referral-title">
            <span className="quantum-text">Quantum Referrals</span>
            {referralData.founderStatus && (
              <span className="founder-badge">👑 QHC Founder</span>
            )}
          </h2>
          <div className="referral-stats">
            <div className="stat">
              <span className="stat-value">{referralData.totalReferrals}</span>
              <span className="stat-label">Total Referrals</span>
            </div>
            <div className="stat">
              <span className="stat-value">{referralData.quantumCreditsEarned}</span>
              <span className="stat-label">Credits Earned</span>
            </div>
            <div className="stat">
              <span className="stat-value">#{referralData.leaderboardRank || 'Unranked'}</span>
              <span className="stat-label">Leaderboard</span>
            </div>
          </div>
        </div>
      </div>

      {!referralData.founderStatus && (
        <div className="founder-progress">
          <div className="progress-header">
            <h3>Path to QHC Founder Status</h3>
            <span>{founderProgress.current}/5 referrals</span>
          </div>
          <div className="progress-bar">
            <motion.div
              className="progress-fill"
              initial={{ width: 0 }}
              animate={{ width: `${founderProgress.percentage}%` }}
              transition={{ duration: 1, ease: 'easeOut' }}
            />
          </div>
          <p className="progress-text">
            {founderProgress.needed > 0 
              ? `${founderProgress.needed} more referrals to unlock Founder Status!`
              : 'Congratulations! You\'ve earned Founder Status!'
            }
          </p>
          <button 
            className="benefits-btn"
            onClick={() => setShowFounderBenefits(!showFounderBenefits)}
          >
            View Founder Benefits
          </button>
        </div>
      )}

      <AnimatePresence>
        {showFounderBenefits && (
          <motion.div
            className="founder-benefits"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h4>QHC Founder Benefits</h4>
            <div className="benefits-grid">
              {FOUNDER_BENEFITS.map((benefit, index) => (
                <motion.div
                  key={index}
                  className="benefit-item"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <span className="benefit-icon">✨</span>
                  <span className="benefit-text">{benefit}</span>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="referral-tools">
        <div className="referral-link-section">
          <h3>Your Quantum Invitation</h3>
          <div className="referral-code">
            <span className="code-label">Referral Code:</span>
            <span className="code-value">{referralData.referralCode}</span>
          </div>
          
          <div className="link-container">
            <input 
              type="text" 
              value={referralData.referralLink} 
              readOnly 
              className="referral-input"
            />
            <button 
              className={`copy-btn ${copiedLink ? 'copied' : ''}`}
              onClick={copyReferralLink}
            >
              {copiedLink ? '✓ Copied!' : 'Copy Link'}
            </button>
          </div>

          <div className="share-buttons">
            <button 
              className="share-btn twitter"
              onClick={() => shareOnSocial('twitter')}
            >
              Share on Twitter
            </button>
            <button 
              className="share-btn linkedin"
              onClick={() => shareOnSocial('linkedin')}
            >
              Share on LinkedIn
            </button>
            <button 
              className="share-btn facebook"
              onClick={() => shareOnSocial('facebook')}
            >
              Share on Facebook
            </button>
            <button 
              className="qr-btn"
              onClick={() => setShowQRCode(!showQRCode)}
            >
              {showQRCode ? 'Hide QR' : 'Show QR'}
            </button>
          </div>

          <AnimatePresence>
            {showQRCode && (
              <motion.div
                className="qr-code-container"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.3 }}
              >
                <QRCodeSVG 
                  value={referralData.referralLink}
                  size={200}
                  bgColor="#000000"
                  fgColor="#00fff6"
                  level="M"
                  includeMargin
                />
                <p>Scan to join the Quantum High Council</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <div className="achievements-section">
        <h3>Quantum Achievements</h3>
        <div className="achievements-grid">
          {referralData.achievements.map((achievement, index) => (
            <motion.div
              key={achievement.id}
              className={`achievement-card ${
                achievement.unlocked ? 'unlocked' : 'locked'
              } ${
                selectedAchievement === achievement.id ? 'selected' : ''
              }`}
              onClick={() => setSelectedAchievement(
                selectedAchievement === achievement.id ? null : achievement.id
              )}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
            >
              <div className="achievement-icon">{achievement.icon}</div>
              <div className="achievement-info">
                <h4 className="achievement-name">{achievement.name}</h4>
                <p className="achievement-description">{achievement.description}</p>
                {achievement.unlocked && (
                  <div className="achievement-reward">{achievement.reward}</div>
                )}
              </div>
              {achievement.unlocked && (
                <div className="achievement-checkmark">✓</div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      <div className="leaderboard-section">
        <h3>Quantum Leaderboard</h3>
        <div className="leaderboard">
          {leaderboard.map((entry, index) => (
            <motion.div
              key={entry.rank}
              className={`leaderboard-entry ${
                entry.name === 'You' ? 'current-user' : ''
              }`}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="rank">#{entry.rank}</div>
              <div className="avatar">{entry.avatar}</div>
              <div className="user-info">
                <span className="username">{entry.name}</span>
                <span className="user-stats">
                  {entry.referrals} referrals • {entry.credits} QC
                </span>
              </div>
              {entry.rank <= 3 && (
                <div className="trophy">
                  {entry.rank === 1 ? '🥇' : entry.rank === 2 ? '🥈' : '🥉'}
                </div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      <style jsx>{`
        .referral-system {
          background: rgba(0, 0, 0, 0.8);
          border-radius: 20px;
          padding: 2rem;
          border: 2px solid rgba(0, 255, 246, 0.3);
          backdrop-filter: blur(10px);
          font-family: 'Orbitron', monospace;
        }

        .referral-header {
          margin-bottom: 2rem;
        }

        .header-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .referral-title {
          display: flex;
          align-items: center;
          gap: 1rem;
          margin: 0;
        }

        .quantum-text {
          font-size: 2rem;
          font-weight: 900;
          background: linear-gradient(45deg, #00fff6, #8000ff);
          background-clip: text;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          text-shadow: 0 0 20px rgba(0, 255, 246, 0.5);
        }

        .founder-badge {
          background: linear-gradient(45deg, #ff6b00, #ffaa00);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 600;
          box-shadow: 0 0 20px rgba(255, 107, 0, 0.5);
        }

        .referral-stats {
          display: flex;
          gap: 2rem;
        }

        .stat {
          text-align: center;
        }

        .stat-value {
          display: block;
          font-size: 1.8rem;
          font-weight: 900;
          color: #00fff6;
          text-shadow: 0 0 15px #00fff6;
        }

        .stat-label {
          color: rgba(255, 255, 255, 0.7);
          font-size: 0.9rem;
        }

        .founder-progress {
          background: rgba(255, 107, 0, 0.1);
          border: 1px solid rgba(255, 107, 0, 0.3);
          border-radius: 15px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }

        .progress-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        .progress-header h3 {
          color: #ff6b00;
          margin: 0;
        }

        .progress-bar {
          height: 20px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
          overflow: hidden;
          margin-bottom: 1rem;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #ff6b00, #ffaa00);
          border-radius: 10px;
          box-shadow: 0 0 20px rgba(255, 107, 0, 0.5);
        }

        .progress-text {
          color: rgba(255, 255, 255, 0.8);
          margin: 0 0 1rem 0;
        }

        .benefits-btn {
          background: linear-gradient(45deg, #ff6b00, #ffaa00);
          border: none;
          border-radius: 10px;
          padding: 0.8rem 1.5rem;
          color: white;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .benefits-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(255, 107, 0, 0.3);
        }

        .founder-benefits {
          background: rgba(255, 107, 0, 0.05);
          border-radius: 15px;
          padding: 1.5rem;
          margin-bottom: 2rem;
        }

        .founder-benefits h4 {
          color: #ff6b00;
          margin-bottom: 1rem;
          text-align: center;
        }

        .benefits-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1rem;
        }

        .benefit-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 0.8rem;
          background: rgba(0, 0, 0, 0.3);
          border-radius: 10px;
          border: 1px solid rgba(255, 107, 0, 0.2);
        }

        .benefit-icon {
          font-size: 1.2rem;
        }

        .benefit-text {
          color: rgba(255, 255, 255, 0.9);
          font-size: 0.9rem;
        }

        .referral-tools {
          margin-bottom: 2rem;
        }

        .referral-link-section h3 {
          color: #00fff6;
          margin-bottom: 1rem;
        }

        .referral-code {
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .code-label {
          color: rgba(255, 255, 255, 0.7);
        }

        .code-value {
          font-size: 1.2rem;
          font-weight: 700;
          color: #00fff6;
          background: rgba(0, 255, 246, 0.1);
          padding: 0.5rem 1rem;
          border-radius: 8px;
          border: 1px solid rgba(0, 255, 246, 0.3);
        }

        .link-container {
          display: flex;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .referral-input {
          flex: 1;
          background: rgba(0, 0, 0, 0.6);
          border: 1px solid rgba(0, 255, 246, 0.3);
          border-radius: 8px;
          padding: 0.8rem;
          color: white;
          font-family: 'Orbitron', monospace;
        }

        .copy-btn {
          background: linear-gradient(45deg, #00fff6, #8000ff);
          border: none;
          border-radius: 8px;
          padding: 0.8rem 1.5rem;
          color: white;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          min-width: 120px;
        }

        .copy-btn.copied {
          background: linear-gradient(45deg, #00ff00, #00aa00);
        }

        .copy-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(0, 255, 246, 0.3);
        }

        .share-buttons {
          display: flex;
          gap: 1rem;
          flex-wrap: wrap;
        }

        .share-btn, .qr-btn {
          padding: 0.8rem 1.5rem;
          border: none;
          border-radius: 8px;
          color: white;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .share-btn.twitter {
          background: linear-gradient(45deg, #1da1f2, #0d8bd9);
        }

        .share-btn.linkedin {
          background: linear-gradient(45deg, #0077b5, #005885);
        }

        .share-btn.facebook {
          background: linear-gradient(45deg, #1877f2, #166fe5);
        }

        .qr-btn {
          background: linear-gradient(45deg, #8000ff, #6000cc);
        }

        .share-btn:hover, .qr-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
        }

        .qr-code-container {
          text-align: center;
          margin-top: 1rem;
          padding: 1rem;
          background: rgba(0, 255, 246, 0.1);
          border-radius: 15px;
          border: 1px solid rgba(0, 255, 246, 0.3);
        }

        .qr-code-container p {
          color: #00fff6;
          margin-top: 1rem;
          font-weight: 600;
        }

        .achievements-section {
          margin-bottom: 2rem;
        }

        .achievements-section h3 {
          color: #00fff6;
          margin-bottom: 1rem;
        }

        .achievements-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1rem;
        }

        .achievement-card {
          background: rgba(0, 0, 0, 0.6);
          border: 2px solid rgba(255, 255, 255, 0.2);
          border-radius: 15px;
          padding: 1.5rem;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .achievement-card.unlocked {
          border-color: #00fff6;
          box-shadow: 0 0 20px rgba(0, 255, 246, 0.3);
        }

        .achievement-card.locked {
          opacity: 0.6;
        }

        .achievement-card:hover {
          transform: translateY(-2px);
        }

        .achievement-icon {
          font-size: 2rem;
          filter: drop-shadow(0 0 10px #00fff6);
        }

        .achievement-info {
          flex: 1;
        }

        .achievement-name {
          color: #00fff6;
          margin: 0 0 0.5rem 0;
          font-size: 1.1rem;
        }

        .achievement-description {
          color: rgba(255, 255, 255, 0.7);
          margin: 0 0 0.5rem 0;
          font-size: 0.9rem;
        }

        .achievement-reward {
          color: #ff6b00;
          font-weight: 600;
          font-size: 0.8rem;
        }

        .achievement-checkmark {
          position: absolute;
          top: 10px;
          right: 10px;
          color: #00ff00;
          font-size: 1.2rem;
          font-weight: 900;
        }

        .leaderboard-section h3 {
          color: #00fff6;
          margin-bottom: 1rem;
        }

        .leaderboard {
          background: rgba(0, 0, 0, 0.6);
          border-radius: 15px;
          padding: 1rem;
          border: 1px solid rgba(0, 255, 246, 0.3);
        }

        .leaderboard-entry {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          transition: all 0.3s ease;
        }

        .leaderboard-entry:last-child {
          border-bottom: none;
        }

        .leaderboard-entry.current-user {
          background: rgba(0, 255, 246, 0.1);
          border-radius: 10px;
          border: 1px solid rgba(0, 255, 246, 0.3);
        }

        .leaderboard-entry:hover {
          background: rgba(255, 255, 255, 0.05);
        }

        .rank {
          font-size: 1.2rem;
          font-weight: 700;
          color: #00fff6;
          min-width: 40px;
        }

        .avatar {
          font-size: 1.5rem;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          background: rgba(0, 255, 246, 0.2);
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .user-info {
          flex: 1;
        }

        .username {
          display: block;
          color: white;
          font-weight: 600;
          margin-bottom: 0.2rem;
        }

        .user-stats {
          color: rgba(255, 255, 255, 0.7);
          font-size: 0.8rem;
        }

        .trophy {
          font-size: 1.5rem;
        }

        @media (max-width: 768px) {
          .header-content {
            flex-direction: column;
            text-align: center;
          }

          .referral-stats {
            justify-content: center;
          }

          .link-container {
            flex-direction: column;
          }

          .share-buttons {
            justify-content: center;
          }

          .achievements-grid {
            grid-template-columns: 1fr;
          }

          .achievement-card {
            flex-direction: column;
            text-align: center;
          }
        }
      `}</style>
    </div>
  );
};

export default ReferralSystem;