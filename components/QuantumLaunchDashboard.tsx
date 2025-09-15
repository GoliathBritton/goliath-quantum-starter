import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { QuantumCountdown } from './QuantumCountdown';
import { RewardTiers } from './RewardTiers';
import { ReferralSystem } from './ReferralSystem';

interface LaunchDashboardProps {
  userId?: string;
  launchDate?: Date;
  className?: string;
}

interface UserData {
  quantumCredits: number;
  totalReferrals: number;
  founderStatus: boolean;
  achievements: string[];
  lastLogin: Date;
}

const DEFAULT_LAUNCH_DATE = new Date('2025-12-01T00:00:00Z');

export const QuantumLaunchDashboard: React.FC<LaunchDashboardProps> = ({
  userId = 'demo-user',
  launchDate = DEFAULT_LAUNCH_DATE,
  className = ''
}) => {
  const [userData, setUserData] = useState<UserData>({
    quantumCredits: 150,
    totalReferrals: 2,
    founderStatus: false,
    achievements: [],
    lastLogin: new Date()
  });
  
  const [activeTab, setActiveTab] = useState<'countdown' | 'rewards' | 'referrals'>('countdown');
  const [timeRemaining, setTimeRemaining] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0,
    total: 0
  });
  const [isLaunched, setIsLaunched] = useState(false);
  const [showWelcomeAnimation, setShowWelcomeAnimation] = useState(false);
  const [notifications, setNotifications] = useState<any[]>([]);

  useEffect(() => {
    // Load user data from localStorage or API
    loadUserData();
    
    // Check if this is the user's first visit
    const hasVisited = localStorage.getItem(`hasVisited_${userId}`);
    if (!hasVisited) {
      setShowWelcomeAnimation(true);
      localStorage.setItem(`hasVisited_${userId}`, 'true');
      addNotification({
        id: 'welcome',
        type: 'success',
        title: 'Welcome to the Quantum High Council!',
        message: 'Start earning Quantum Credits and invite friends to unlock exclusive rewards.',
        duration: 5000
      });
    }

    // Set up countdown timer
    const timer = setInterval(updateCountdown, 1000);
    updateCountdown(); // Initial call

    return () => clearInterval(timer);
  }, [launchDate]);

  useEffect(() => {
    // Save user data whenever it changes
    saveUserData();
  }, [userData]);

  const loadUserData = () => {
    const saved = localStorage.getItem(`userData_${userId}`);
    if (saved) {
      try {
        const data = JSON.parse(saved);
        setUserData(prev => ({ ...prev, ...data }));
      } catch (error) {
        console.error('Failed to load user data:', error);
      }
    }
  };

  const saveUserData = () => {
    localStorage.setItem(`userData_${userId}`, JSON.stringify(userData));
  };

  const updateCountdown = () => {
    const now = new Date().getTime();
    const launchTime = launchDate.getTime();
    const distance = launchTime - now;

    if (distance < 0) {
      setIsLaunched(true);
      setTimeRemaining({ days: 0, hours: 0, minutes: 0, seconds: 0, total: 0 });
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    setTimeRemaining({ days, hours, minutes, seconds, total: distance });
  };

  const addNotification = (notification: any) => {
    const id = notification.id || Date.now().toString();
    const newNotification = { ...notification, id };
    
    setNotifications(prev => [...prev, newNotification]);
    
    if (notification.duration) {
      setTimeout(() => {
        removeNotification(id);
      }, notification.duration);
    }
  };

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const handleEarnCredits = (amount: number) => {
    setUserData(prev => ({
      ...prev,
      quantumCredits: prev.quantumCredits + amount
    }));
    
    addNotification({
      type: 'success',
      title: 'Quantum Credits Earned!',
      message: `+${amount} Quantum Credits added to your account`,
      duration: 3000
    });
  };

  const handleClaimReward = (tierId: string) => {
    addNotification({
      type: 'success',
      title: 'Reward Claimed!',
      message: `Successfully claimed rewards for ${tierId}`,
      duration: 3000
    });
  };

  const handleReferralUpdate = (data: any) => {
    setUserData(prev => ({
      ...prev,
      totalReferrals: data.totalReferrals,
      founderStatus: data.founderStatus,
      quantumCredits: prev.quantumCredits + (data.quantumCreditsEarned || 0)
    }));
    
    if (data.founderStatus && !userData.founderStatus) {
      addNotification({
        type: 'achievement',
        title: '👑 QHC Founder Status Unlocked!',
        message: 'Congratulations! You\'ve earned lifetime founder benefits.',
        duration: 5000
      });
    }
  };

  const getDaysUntilLaunch = () => {
    return Math.max(0, timeRemaining.days);
  };

  const getTabIcon = (tab: string) => {
    switch (tab) {
      case 'countdown': return '⏰';
      case 'rewards': return '🎁';
      case 'referrals': return '🚀';
      default: return '⚛️';
    }
  };

  return (
    <div className={`quantum-launch-dashboard ${className}`}>
      {/* Notifications */}
      <div className="notifications-container">
        <AnimatePresence>
          {notifications.map((notification) => (
            <motion.div
              key={notification.id}
              className={`notification ${notification.type}`}
              initial={{ opacity: 0, x: 300, scale: 0.8 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={{ opacity: 0, x: 300, scale: 0.8 }}
              transition={{ duration: 0.3 }}
            >
              <div className="notification-content">
                <h4 className="notification-title">{notification.title}</h4>
                <p className="notification-message">{notification.message}</p>
              </div>
              <button 
                className="notification-close"
                onClick={() => removeNotification(notification.id)}
              >
                ×
              </button>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* Welcome Animation */}
      <AnimatePresence>
        {showWelcomeAnimation && (
          <motion.div
            className="welcome-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            <motion.div
              className="welcome-content"
              initial={{ scale: 0.5, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.5, opacity: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <div className="welcome-icon">🌌</div>
              <h2>Welcome to the Quantum Nexus</h2>
              <p>Your journey to the High Council begins now</p>
              <motion.button
                className="welcome-btn"
                onClick={() => setShowWelcomeAnimation(false)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Begin Quantum Journey
              </motion.button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <div className="header-info">
            <h1 className="dashboard-title">
              <span className="quantum-text">Quantum High Council</span>
              <span className="launch-subtitle">Launch Countdown</span>
            </h1>
            <div className="user-status">
              <div className="status-item">
                <span className="status-label">Quantum Credits:</span>
                <span className="status-value">{userData.quantumCredits.toLocaleString()}</span>
              </div>
              <div className="status-item">
                <span className="status-label">Referrals:</span>
                <span className="status-value">{userData.totalReferrals}</span>
              </div>
              {userData.founderStatus && (
                <div className="founder-status">
                  👑 QHC Founder
                </div>
              )}
            </div>
          </div>
          
          <div className="quick-stats">
            <div className="stat-card">
              <div className="stat-icon">⏰</div>
              <div className="stat-info">
                <span className="stat-value">{timeRemaining.days}</span>
                <span className="stat-label">Days Left</span>
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-icon">🎯</div>
              <div className="stat-info">
                <span className="stat-value">{userData.founderStatus ? '✓' : `${Math.max(0, 5 - userData.totalReferrals)}`}</span>
                <span className="stat-label">{userData.founderStatus ? 'Founder' : 'To Founder'}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="dashboard-nav">
        {(['countdown', 'rewards', 'referrals'] as const).map((tab) => (
          <motion.button
            key={tab}
            className={`nav-tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <span className="tab-icon">{getTabIcon(tab)}</span>
            <span className="tab-label">
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </span>
          </motion.button>
        ))}
      </div>

      {/* Content Area */}
      <div className="dashboard-content">
        <AnimatePresence mode="wait">
          {activeTab === 'countdown' && (
            <motion.div
              key="countdown"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <QuantumCountdown 
                launchDate={launchDate}
                isLaunched={isLaunched}
                timeRemaining={timeRemaining}
              />
            </motion.div>
          )}
          
          {activeTab === 'rewards' && (
            <motion.div
              key="rewards"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <RewardTiers
                daysUntilLaunch={getDaysUntilLaunch()}
                userCredits={userData.quantumCredits}
                onClaimReward={handleClaimReward}
                onEarnCredits={handleEarnCredits}
              />
            </motion.div>
          )}
          
          {activeTab === 'referrals' && (
            <motion.div
              key="referrals"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
            >
              <ReferralSystem
                userId={userId}
                onReferralUpdate={handleReferralUpdate}
                daysUntilLaunch={getDaysUntilLaunch()}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer */}
      <div className="dashboard-footer">
        <div className="footer-content">
          <div className="footer-links">
            <a href="#" className="footer-link">Terms & Conditions</a>
            <a href="#" className="footer-link">Privacy Policy</a>
            <a href="#" className="footer-link">Support</a>
          </div>
          <div className="footer-info">
            <p>© 2024 Quantum Nexus. All rights reserved.</p>
            <p>Join the revolution. Shape the future.</p>
          </div>
        </div>
      </div>

      <style jsx>{`
        .quantum-launch-dashboard {
          min-height: 100vh;
          background: 
            radial-gradient(ellipse at top, rgba(0, 255, 246, 0.1) 0%, transparent 50%),
            radial-gradient(ellipse at bottom, rgba(128, 0, 255, 0.1) 0%, transparent 50%),
            linear-gradient(180deg, #000000 0%, #0a0a0a 100%);
          font-family: 'Orbitron', monospace;
          color: white;
          position: relative;
          overflow-x: hidden;
        }

        .notifications-container {
          position: fixed;
          top: 20px;
          right: 20px;
          z-index: 1000;
          display: flex;
          flex-direction: column;
          gap: 1rem;
          max-width: 400px;
        }

        .notification {
          background: rgba(0, 0, 0, 0.9);
          border-radius: 10px;
          padding: 1rem;
          border-left: 4px solid;
          backdrop-filter: blur(10px);
          display: flex;
          align-items: flex-start;
          gap: 1rem;
          box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
        }

        .notification.success {
          border-left-color: #00ff00;
        }

        .notification.achievement {
          border-left-color: #ff6b00;
        }

        .notification-content {
          flex: 1;
        }

        .notification-title {
          margin: 0 0 0.5rem 0;
          font-size: 0.9rem;
          font-weight: 600;
          color: #00fff6;
        }

        .notification-message {
          margin: 0;
          font-size: 0.8rem;
          color: rgba(255, 255, 255, 0.8);
          line-height: 1.4;
        }

        .notification-close {
          background: none;
          border: none;
          color: rgba(255, 255, 255, 0.6);
          font-size: 1.2rem;
          cursor: pointer;
          padding: 0;
          width: 20px;
          height: 20px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .notification-close:hover {
          color: white;
        }

        .welcome-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.9);
          backdrop-filter: blur(10px);
          z-index: 2000;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .welcome-content {
          text-align: center;
          background: rgba(0, 255, 246, 0.1);
          border: 2px solid rgba(0, 255, 246, 0.3);
          border-radius: 20px;
          padding: 3rem;
          max-width: 500px;
          backdrop-filter: blur(10px);
        }

        .welcome-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
          filter: drop-shadow(0 0 20px #00fff6);
        }

        .welcome-content h2 {
          font-size: 2rem;
          margin-bottom: 1rem;
          background: linear-gradient(45deg, #00fff6, #8000ff);
          background-clip: text;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .welcome-content p {
          color: rgba(255, 255, 255, 0.8);
          margin-bottom: 2rem;
          font-size: 1.1rem;
        }

        .welcome-btn {
          background: linear-gradient(45deg, #00fff6, #8000ff);
          border: none;
          border-radius: 10px;
          padding: 1rem 2rem;
          color: white;
          font-weight: 600;
          font-size: 1.1rem;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .dashboard-header {
          padding: 2rem;
          border-bottom: 1px solid rgba(0, 255, 246, 0.2);
        }

        .header-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 2rem;
        }

        .dashboard-title {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
          margin: 0;
        }

        .quantum-text {
          font-size: 2.5rem;
          font-weight: 900;
          background: linear-gradient(45deg, #00fff6, #8000ff);
          background-clip: text;
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          text-shadow: 0 0 30px rgba(0, 255, 246, 0.5);
        }

        .launch-subtitle {
          font-size: 1.2rem;
          color: rgba(255, 255, 255, 0.7);
          font-weight: 400;
        }

        .user-status {
          display: flex;
          gap: 2rem;
          margin-top: 1rem;
          flex-wrap: wrap;
        }

        .status-item {
          display: flex;
          flex-direction: column;
          gap: 0.2rem;
        }

        .status-label {
          color: rgba(255, 255, 255, 0.6);
          font-size: 0.8rem;
        }

        .status-value {
          color: #00fff6;
          font-weight: 700;
          font-size: 1.1rem;
        }

        .founder-status {
          background: linear-gradient(45deg, #ff6b00, #ffaa00);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 600;
          box-shadow: 0 0 20px rgba(255, 107, 0, 0.5);
          align-self: flex-start;
        }

        .quick-stats {
          display: flex;
          gap: 1rem;
        }

        .stat-card {
          background: rgba(0, 255, 246, 0.1);
          border: 1px solid rgba(0, 255, 246, 0.3);
          border-radius: 15px;
          padding: 1rem;
          display: flex;
          align-items: center;
          gap: 1rem;
          min-width: 120px;
        }

        .stat-icon {
          font-size: 1.5rem;
          filter: drop-shadow(0 0 10px #00fff6);
        }

        .stat-info {
          display: flex;
          flex-direction: column;
        }

        .stat-value {
          font-size: 1.5rem;
          font-weight: 700;
          color: #00fff6;
        }

        .stat-label {
          font-size: 0.8rem;
          color: rgba(255, 255, 255, 0.7);
        }

        .dashboard-nav {
          display: flex;
          justify-content: center;
          gap: 1rem;
          padding: 2rem;
          border-bottom: 1px solid rgba(0, 255, 246, 0.2);
        }

        .nav-tab {
          background: rgba(0, 0, 0, 0.6);
          border: 2px solid rgba(255, 255, 255, 0.2);
          border-radius: 15px;
          padding: 1rem 2rem;
          color: rgba(255, 255, 255, 0.7);
          cursor: pointer;
          transition: all 0.3s ease;
          display: flex;
          align-items: center;
          gap: 0.8rem;
          font-weight: 600;
          min-width: 150px;
          justify-content: center;
        }

        .nav-tab.active {
          background: rgba(0, 255, 246, 0.1);
          border-color: #00fff6;
          color: #00fff6;
          box-shadow: 0 0 20px rgba(0, 255, 246, 0.3);
        }

        .nav-tab:hover {
          border-color: #00fff6;
          color: #00fff6;
          transform: translateY(-2px);
        }

        .tab-icon {
          font-size: 1.2rem;
        }

        .dashboard-content {
          padding: 2rem;
          min-height: 600px;
        }

        .dashboard-footer {
          border-top: 1px solid rgba(0, 255, 246, 0.2);
          padding: 2rem;
          margin-top: 2rem;
        }

        .footer-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .footer-links {
          display: flex;
          gap: 2rem;
        }

        .footer-link {
          color: rgba(255, 255, 255, 0.6);
          text-decoration: none;
          font-size: 0.9rem;
          transition: color 0.3s ease;
        }

        .footer-link:hover {
          color: #00fff6;
        }

        .footer-info {
          text-align: right;
        }

        .footer-info p {
          margin: 0;
          color: rgba(255, 255, 255, 0.5);
          font-size: 0.8rem;
          line-height: 1.4;
        }

        @media (max-width: 768px) {
          .header-content {
            flex-direction: column;
            text-align: center;
          }

          .user-status {
            justify-content: center;
          }

          .quick-stats {
            justify-content: center;
            flex-wrap: wrap;
          }

          .dashboard-nav {
            flex-direction: column;
            align-items: center;
          }

          .nav-tab {
            width: 100%;
            max-width: 300px;
          }

          .footer-content {
            flex-direction: column;
            text-align: center;
          }

          .footer-info {
            text-align: center;
          }

          .notifications-container {
            left: 20px;
            right: 20px;
            max-width: none;
          }
        }

        @media (max-width: 480px) {
          .dashboard-header {
            padding: 1rem;
          }

          .dashboard-content {
            padding: 1rem;
          }

          .quantum-text {
            font-size: 2rem;
          }

          .stat-card {
            min-width: 100px;
            padding: 0.8rem;
          }
        }
      `}</style>
    </div>
  );
};

export default QuantumLaunchDashboard;