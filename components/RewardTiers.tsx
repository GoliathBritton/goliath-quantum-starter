import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface RewardTier {
  id: string;
  name: string;
  daysFromLaunch: number;
  quantumCredits: number;
  rewards: string[];
  unlocked: boolean;
  claimed: boolean;
  icon: string;
  color: string;
  glowColor: string;
}

interface RewardTiersProps {
  daysUntilLaunch: number;
  userCredits: number;
  onClaimReward: (tierId: string) => void;
  onEarnCredits: (amount: number) => void;
}

const REWARD_TIERS: RewardTier[] = [
  {
    id: 'genesis',
    name: 'Genesis Initiate',
    daysFromLaunch: 30,
    quantumCredits: 100,
    rewards: [
      'Free Quantum Agent Templates',
      'Early Access Badge',
      'Quantum Starter Pack'
    ],
    unlocked: false,
    claimed: false,
    icon: '⚛️',
    color: '#00fff6',
    glowColor: 'rgba(0, 255, 246, 0.5)'
  },
  {
    id: 'entangled',
    name: 'Entangled Pioneer',
    daysFromLaunch: 14,
    quantumCredits: 250,
    rewards: [
      'Premium Trial Extension (30 days)',
      'Quantum Workflow Templates',
      'Priority Support Access'
    ],
    unlocked: false,
    claimed: false,
    icon: '🌌',
    color: '#8000ff',
    glowColor: 'rgba(128, 0, 255, 0.5)'
  },
  {
    id: 'nexus',
    name: 'Nexus Guardian',
    daysFromLaunch: 7,
    quantumCredits: 500,
    rewards: [
      'Quantum Glyphs NFT Collection',
      'Advanced AI Agent Access',
      'Exclusive Training Sessions'
    ],
    unlocked: false,
    claimed: false,
    icon: '🔮',
    color: '#0080ff',
    glowColor: 'rgba(0, 128, 255, 0.5)'
  },
  {
    id: 'council',
    name: 'High Council Founder',
    daysFromLaunch: 0,
    quantumCredits: 1000,
    rewards: [
      'QHC Private Event Access',
      'Secret Product Demo',
      'Lifetime Founder Status',
      'Quantum Nexus Beta Access'
    ],
    unlocked: false,
    claimed: false,
    icon: '👑',
    color: '#ff6b00',
    glowColor: 'rgba(255, 107, 0, 0.5)'
  }
];

const CREDIT_ACTIONS = [
  { action: 'Daily Check-in', credits: 10, cooldown: 24 * 60 * 60 * 1000 },
  { action: 'Share on Social', credits: 25, cooldown: 12 * 60 * 60 * 1000 },
  { action: 'Invite Friend', credits: 100, cooldown: 0 },
  { action: 'Complete Profile', credits: 50, cooldown: 0 },
  { action: 'Join Discord', credits: 75, cooldown: 0 }
];

export const RewardTiers: React.FC<RewardTiersProps> = ({
  daysUntilLaunch,
  userCredits,
  onClaimReward,
  onEarnCredits
}) => {
  const [tiers, setTiers] = useState<RewardTier[]>(REWARD_TIERS);
  const [selectedTier, setSelectedTier] = useState<string | null>(null);
  const [showCreditActions, setShowCreditActions] = useState(false);
  const [actionCooldowns, setActionCooldowns] = useState<Record<string, number>>({});

  useEffect(() => {
    // Update tier unlock status based on days until launch
    const updatedTiers = tiers.map(tier => ({
      ...tier,
      unlocked: daysUntilLaunch <= tier.daysFromLaunch
    }));
    setTiers(updatedTiers);
  }, [daysUntilLaunch]);

  useEffect(() => {
    // Load cooldowns from localStorage
    const savedCooldowns = localStorage.getItem('quantumCreditCooldowns');
    if (savedCooldowns) {
      setActionCooldowns(JSON.parse(savedCooldowns));
    }
  }, []);

  const handleClaimReward = (tierId: string) => {
    const tier = tiers.find(t => t.id === tierId);
    if (tier && tier.unlocked && !tier.claimed) {
      setTiers(prev => prev.map(t => 
        t.id === tierId ? { ...t, claimed: true } : t
      ));
      onClaimReward(tierId);
      onEarnCredits(tier.quantumCredits);
    }
  };

  const handleEarnCredits = (action: string, credits: number, cooldown: number) => {
    const now = Date.now();
    const lastAction = actionCooldowns[action] || 0;
    
    if (now - lastAction >= cooldown) {
      onEarnCredits(credits);
      const newCooldowns = { ...actionCooldowns, [action]: now };
      setActionCooldowns(newCooldowns);
      localStorage.setItem('quantumCreditCooldowns', JSON.stringify(newCooldowns));
    }
  };

  const isActionAvailable = (action: string, cooldown: number) => {
    const now = Date.now();
    const lastAction = actionCooldowns[action] || 0;
    return now - lastAction >= cooldown;
  };

  const getTimeUntilAvailable = (action: string, cooldown: number) => {
    const now = Date.now();
    const lastAction = actionCooldowns[action] || 0;
    const timeLeft = cooldown - (now - lastAction);
    return Math.max(0, timeLeft);
  };

  const formatTime = (ms: number) => {
    const hours = Math.floor(ms / (1000 * 60 * 60));
    const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));
    return `${hours}h ${minutes}m`;
  };

  return (
    <div className="reward-tiers">
      <div className="reward-header">
        <h2 className="reward-title">
          <span className="quantum-text">Quantum Credits</span>
          <span className="credits-display">{userCredits.toLocaleString()}</span>
        </h2>
        <button 
          className="earn-credits-btn"
          onClick={() => setShowCreditActions(!showCreditActions)}
        >
          Earn More Credits
        </button>
      </div>

      <AnimatePresence>
        {showCreditActions && (
          <motion.div
            className="credit-actions"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
          >
            <h3>Earn Quantum Credits</h3>
            <div className="actions-grid">
              {CREDIT_ACTIONS.map((creditAction, index) => {
                const available = isActionAvailable(creditAction.action, creditAction.cooldown);
                const timeLeft = getTimeUntilAvailable(creditAction.action, creditAction.cooldown);
                
                return (
                  <motion.button
                    key={creditAction.action}
                    className={`credit-action ${available ? 'available' : 'cooldown'}`}
                    onClick={() => available && handleEarnCredits(creditAction.action, creditAction.credits, creditAction.cooldown)}
                    disabled={!available}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    whileHover={available ? { scale: 1.05 } : {}}
                    whileTap={available ? { scale: 0.95 } : {}}
                  >
                    <div className="action-info">
                      <span className="action-name">{creditAction.action}</span>
                      <span className="action-credits">+{creditAction.credits} QC</span>
                    </div>
                    {!available && timeLeft > 0 && (
                      <div className="cooldown-timer">
                        {formatTime(timeLeft)}
                      </div>
                    )}
                  </motion.button>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="tiers-container">
        <h3 className="tiers-title">Reward Milestones</h3>
        <div className="tiers-grid">
          {tiers.map((tier, index) => (
            <motion.div
              key={tier.id}
              className={`tier-card ${
                tier.unlocked ? 'unlocked' : 'locked'
              } ${
                tier.claimed ? 'claimed' : ''
              } ${
                selectedTier === tier.id ? 'selected' : ''
              }`}
              onClick={() => setSelectedTier(selectedTier === tier.id ? null : tier.id)}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
              style={{
                '--tier-color': tier.color,
                '--tier-glow': tier.glowColor
              } as React.CSSProperties}
            >
              <div className="tier-header">
                <div className="tier-icon">{tier.icon}</div>
                <div className="tier-info">
                  <h4 className="tier-name">{tier.name}</h4>
                  <div className="tier-timing">
                    {tier.daysFromLaunch === 0 ? 'Launch Day' : `${tier.daysFromLaunch} days before launch`}
                  </div>
                </div>
                <div className="tier-status">
                  {tier.claimed ? (
                    <span className="status-claimed">✓ Claimed</span>
                  ) : tier.unlocked ? (
                    <span className="status-available">Available</span>
                  ) : (
                    <span className="status-locked">🔒 Locked</span>
                  )}
                </div>
              </div>

              <div className="tier-credits">
                <span className="credits-amount">{tier.quantumCredits}</span>
                <span className="credits-label">Quantum Credits</span>
              </div>

              <AnimatePresence>
                {selectedTier === tier.id && (
                  <motion.div
                    className="tier-details"
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="rewards-list">
                      <h5>Rewards:</h5>
                      <ul>
                        {tier.rewards.map((reward, idx) => (
                          <li key={idx}>{reward}</li>
                        ))}
                      </ul>
                    </div>
                    
                    {tier.unlocked && !tier.claimed && (
                      <motion.button
                        className="claim-btn"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleClaimReward(tier.id);
                        }}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        Claim Rewards
                      </motion.button>
                    )}
                  </motion.div>
                )}
              </AnimatePresence>

              {tier.unlocked && !tier.claimed && (
                <div className="tier-glow"></div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      <div className="progress-bar">
        <div className="progress-header">
          <span>Launch Progress</span>
          <span>{Math.max(0, 30 - daysUntilLaunch)}/30 days</span>
        </div>
        <div className="progress-track">
          <motion.div
            className="progress-fill"
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(100, ((30 - daysUntilLaunch) / 30) * 100)}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
          />
          {tiers.map((tier, index) => {
            const position = ((30 - tier.daysFromLaunch) / 30) * 100;
            return (
              <div
                key={tier.id}
                className={`progress-milestone ${
                  tier.unlocked ? 'unlocked' : 'locked'
                }`}
                style={{ left: `${position}%` }}
              >
                <div className="milestone-icon">{tier.icon}</div>
                <div className="milestone-tooltip">{tier.name}</div>
              </div>
            );
          })}
        </div>
      </div>

      <style jsx>{`
        .reward-tiers {
          background: rgba(0, 0, 0, 0.8);
          border-radius: 20px;
          padding: 2rem;
          border: 2px solid rgba(0, 255, 246, 0.3);
          backdrop-filter: blur(10px);
          font-family: 'Orbitron', monospace;
        }

        .reward-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
        }

        .reward-title {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
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

        .credits-display {
          font-size: 1.5rem;
          color: #00fff6;
          font-weight: 700;
          text-shadow: 0 0 15px #00fff6;
        }

        .earn-credits-btn {
          background: linear-gradient(45deg, #00fff6, #8000ff);
          border: none;
          border-radius: 10px;
          padding: 0.8rem 1.5rem;
          color: white;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .earn-credits-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px rgba(0, 255, 246, 0.3);
        }

        .credit-actions {
          background: rgba(0, 255, 246, 0.1);
          border-radius: 15px;
          padding: 1.5rem;
          margin-bottom: 2rem;
          border: 1px solid rgba(0, 255, 246, 0.3);
        }

        .credit-actions h3 {
          color: #00fff6;
          margin-bottom: 1rem;
          text-align: center;
        }

        .actions-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
        }

        .credit-action {
          background: rgba(0, 0, 0, 0.6);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 10px;
          padding: 1rem;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
        }

        .credit-action.available {
          border-color: #00fff6;
          box-shadow: 0 0 10px rgba(0, 255, 246, 0.3);
        }

        .credit-action.available:hover {
          background: rgba(0, 255, 246, 0.1);
          transform: translateY(-2px);
        }

        .credit-action.cooldown {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .action-info {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .action-name {
          color: white;
          font-weight: 600;
        }

        .action-credits {
          color: #00fff6;
          font-weight: 700;
        }

        .cooldown-timer {
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background: rgba(255, 107, 0, 0.9);
          color: white;
          padding: 0.3rem 0.8rem;
          border-radius: 15px;
          font-size: 0.8rem;
          font-weight: 600;
        }

        .tiers-container {
          margin-bottom: 2rem;
        }

        .tiers-title {
          color: #00fff6;
          font-size: 1.5rem;
          margin-bottom: 1.5rem;
          text-align: center;
        }

        .tiers-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
        }

        .tier-card {
          background: rgba(0, 0, 0, 0.6);
          border: 2px solid rgba(255, 255, 255, 0.2);
          border-radius: 15px;
          padding: 1.5rem;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
        }

        .tier-card.unlocked {
          border-color: var(--tier-color);
          box-shadow: 0 0 20px var(--tier-glow);
        }

        .tier-card.claimed {
          background: rgba(0, 255, 246, 0.1);
          border-color: #00fff6;
        }

        .tier-card.locked {
          opacity: 0.6;
        }

        .tier-card:hover {
          transform: translateY(-5px);
        }

        .tier-header {
          display: flex;
          align-items: center;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .tier-icon {
          font-size: 2rem;
          filter: drop-shadow(0 0 10px var(--tier-color));
        }

        .tier-info {
          flex: 1;
        }

        .tier-name {
          color: var(--tier-color);
          margin: 0;
          font-size: 1.2rem;
          font-weight: 700;
        }

        .tier-timing {
          color: rgba(255, 255, 255, 0.7);
          font-size: 0.9rem;
        }

        .tier-status {
          font-size: 0.8rem;
          font-weight: 600;
        }

        .status-claimed {
          color: #00fff6;
        }

        .status-available {
          color: #00ff00;
        }

        .status-locked {
          color: rgba(255, 255, 255, 0.5);
        }

        .tier-credits {
          text-align: center;
          margin-bottom: 1rem;
        }

        .credits-amount {
          display: block;
          font-size: 2rem;
          font-weight: 900;
          color: var(--tier-color);
          text-shadow: 0 0 15px var(--tier-glow);
        }

        .credits-label {
          color: rgba(255, 255, 255, 0.7);
          font-size: 0.9rem;
        }

        .tier-details {
          border-top: 1px solid rgba(255, 255, 255, 0.2);
          padding-top: 1rem;
        }

        .rewards-list h5 {
          color: #00fff6;
          margin-bottom: 0.5rem;
        }

        .rewards-list ul {
          list-style: none;
          padding: 0;
          margin: 0;
        }

        .rewards-list li {
          color: rgba(255, 255, 255, 0.8);
          padding: 0.3rem 0;
          border-left: 2px solid var(--tier-color);
          padding-left: 1rem;
          margin-bottom: 0.5rem;
        }

        .claim-btn {
          width: 100%;
          background: linear-gradient(45deg, var(--tier-color), #8000ff);
          border: none;
          border-radius: 10px;
          padding: 0.8rem;
          color: white;
          font-weight: 600;
          cursor: pointer;
          margin-top: 1rem;
          transition: all 0.3s ease;
        }

        .claim-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 20px var(--tier-glow);
        }

        .tier-glow {
          position: absolute;
          top: -50%;
          left: -50%;
          width: 200%;
          height: 200%;
          background: radial-gradient(circle, var(--tier-glow) 0%, transparent 70%);
          animation: tierGlow 3s ease-in-out infinite;
          z-index: -1;
        }

        .progress-bar {
          background: rgba(0, 0, 0, 0.6);
          border-radius: 15px;
          padding: 1.5rem;
          border: 1px solid rgba(0, 255, 246, 0.3);
        }

        .progress-header {
          display: flex;
          justify-content: space-between;
          color: #00fff6;
          margin-bottom: 1rem;
          font-weight: 600;
        }

        .progress-track {
          position: relative;
          height: 20px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 10px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #00fff6, #8000ff);
          border-radius: 10px;
          box-shadow: 0 0 20px rgba(0, 255, 246, 0.5);
        }

        .progress-milestone {
          position: absolute;
          top: -15px;
          transform: translateX(-50%);
          z-index: 2;
        }

        .milestone-icon {
          width: 30px;
          height: 30px;
          border-radius: 50%;
          background: rgba(0, 0, 0, 0.8);
          border: 2px solid #00fff6;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1rem;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .progress-milestone.unlocked .milestone-icon {
          background: #00fff6;
          box-shadow: 0 0 15px rgba(0, 255, 246, 0.7);
        }

        .progress-milestone.locked .milestone-icon {
          border-color: rgba(255, 255, 255, 0.3);
          opacity: 0.5;
        }

        .milestone-tooltip {
          position: absolute;
          bottom: 40px;
          left: 50%;
          transform: translateX(-50%);
          background: rgba(0, 0, 0, 0.9);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 8px;
          font-size: 0.8rem;
          white-space: nowrap;
          opacity: 0;
          pointer-events: none;
          transition: opacity 0.3s ease;
        }

        .progress-milestone:hover .milestone-tooltip {
          opacity: 1;
        }

        @keyframes tierGlow {
          0%, 100% { opacity: 0.3; }
          50% { opacity: 0.7; }
        }

        @media (max-width: 768px) {
          .reward-header {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
          }

          .tiers-grid {
            grid-template-columns: 1fr;
          }

          .actions-grid {
            grid-template-columns: 1fr;
          }

          .tier-header {
            flex-direction: column;
            text-align: center;
            gap: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default RewardTiers;